#!/usr/bin/env python3
"""
Recolha de dados do contador Carlo Gavazzi EM530 via Modbus RTU
Baseado no Node-Red do @PedroFerreira
"""

import time
import json
import logging
from datetime import datetime
from dataclasses import dataclass
from typing import Optional, Dict, Any
import serial
from pymodbus.client.serial import ModbusSerialClient
from pymodbus.exceptions import ModbusException, ConnectionException

# Configuração do registo de eventos
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class ConfiguracaoContador:
    """Configuração do contador"""
    id_contador: int
    id_unidade: int
    nome_contador: str
    id_empresa: str


@dataclass
class ConfiguracaoModbus:
    """Configuração da ligação Modbus"""
    porta: str = "/dev/ttyAMA0"
    velocidade: int = 9600
    bits_dados: int = 8
    paridade: str = 'N'
    bits_paragem: int = 1
    timeout: float = 2.0


class GestorErrosModbus:
    """Gestor de erros Modbus baseado no subflow Node-RED"""

    def __init__(self, nome_contador: str, id_empresa: str):
        self.nome_contador = nome_contador
        self.id_empresa = id_empresa
        self.contagem_erros = 0
        self.ultimo_estado_erro = False

    def processar_erro(self, tem_erro: bool) -> Optional[Dict[str, Any]]:
        """
        Processa erro seguindo a lógica do Node-RED:
        - Incrementa contador se há erro
        - Reinicia se não há erro
        - Considera erro apenas se contagem > 2
        """
        if tem_erro:
            self.contagem_erros += 1
        else:
            self.contagem_erros = 0

        estado_erro_actual = self.contagem_erros > 2

        # Reportar por exceção - só reporta se mudou de estado
        if estado_erro_actual != self.ultimo_estado_erro:
            self.ultimo_estado_erro = estado_erro_actual
            return self._criar_mensagem_erro(estado_erro_actual)

        return None

    def _criar_mensagem_erro(self, e_erro: bool) -> Dict[str, Any]:
        """Cria mensagem de erro baseada no Node-RED"""
        timestamp = datetime.now().isoformat()

        if e_erro:
            topico = f"{self.id_empresa} Erro Comunicação {self.nome_contador} INACTIVO"
            mensagem = f"{self.id_empresa} comunicação com o contador {self.nome_contador} está INACTIVA desde {timestamp}"
        else:
            topico = f"{self.id_empresa} Erro Comunicação {self.nome_contador} Restaurado"
            mensagem = f"{self.id_empresa} comunicação com o contador {self.nome_contador} foi restaurada às {timestamp}"

        return {
            "topico": topico,
            "mensagem": mensagem,
            "timestamp": timestamp,
            "estado_erro": e_erro
        }


class ColectorDadosEM530:
    """Recolha de dados do Carlo Gavazzi EM530"""

    def __init__(self, config_contador: ConfiguracaoContador, config_modbus: ConfiguracaoModbus):
        self.config_contador = config_contador
        self.config_modbus = config_modbus
        self.cliente = None
        self.gestor_erros = GestorErrosModbus(
            config_contador.nome_contador,
            config_contador.id_empresa
        )

    def ligar(self) -> bool:
        """Estabelece ligação Modbus RTU"""
        try:
            self.cliente = ModbusSerialClient(
                method='rtu',
                port=self.config_modbus.porta,
                baudrate=self.config_modbus.velocidade,
                bytesize=self.config_modbus.bits_dados,
                parity=self.config_modbus.paridade,
                stopbits=self.config_modbus.bits_paragem,
                timeout=self.config_modbus.timeout
            )

            if self.cliente.connect():
                logger.info(f"Ligado ao dispositivo Modbus na porta {self.config_modbus.porta}")
                return True
            else:
                logger.error("Falha ao ligar ao dispositivo Modbus")
                return False

        except Exception as e:
            logger.error(f"Erro ao ligar: {e}")
            return False

    def desligar(self):
        """Desliga do dispositivo Modbus"""
        if self.cliente:
            self.cliente.close()
            logger.info("Desligado do dispositivo Modbus")

    def ler_registos(self, endereco: int, quantidade: int) -> Optional[list]:
        """Lê registos Modbus com tratamento de erros"""
        try:
            if not self.cliente or not self.cliente.is_socket_open():
                raise ConnectionException("Cliente não ligado")

            resultado = self.cliente.read_holding_registers(
                address=endereco,
                count=quantidade,
                slave=self.config_contador.id_unidade
            )

            if resultado.isError():
                raise ModbusException(f"Erro na leitura: {resultado}")

            return resultado.registers

        except Exception as e:
            logger.error(f"Erro ao ler registos {endereco}-{endereco + quantidade - 1}: {e}")
            return None

    def recolher_dados(self) -> Optional[Dict[str, Any]]:
        """Recolhe todos os dados seguindo a sequência do Node-RED"""
        timestamp = datetime.now().isoformat()

        try:
            # Leitura 1: Endereço 0x0000, 64 registos (dados principais)
            dados01 = self.ler_registos(0x0000, 64)
            if dados01 is None:
                self._processar_erro_comunicacao()
                return None

            # Leitura 2: Endereço 0x0056, 2 registos (energia aparente)
            dados02 = self.ler_registos(0x0056, 2)
            if dados02 is None:
                self._processar_erro_comunicacao()
                return None

            # Leitura 3: Endereço 0x0082, 6 registos (THD corrente)
            dados03 = self.ler_registos(0x0082, 6)
            if dados03 is None:
                self._processar_erro_comunicacao()
                return None

            # Leitura 4: Endereço 0x0092, 6 registos (THD tensão)
            dados04 = self.ler_registos(0x0092, 6)
            if dados04 is None:
                self._processar_erro_comunicacao()
                return None

            # Processa sucesso na comunicação
            msg_erro = self.gestor_erros.processar_erro(False)
            if msg_erro:
                logger.info(f"Comunicação restaurada: {msg_erro['mensagem']}")

            # Formata dados conforme função Node-RED
            dados_formatados = self._formatar_dados(dados01, dados02, dados03, dados04, timestamp)
            return dados_formatados

        except Exception as e:
            logger.error(f"Erro na recolha de dados: {e}")
            self._processar_erro_comunicacao()
            return None

    def _processar_erro_comunicacao(self):
        """Processa erro de comunicação"""
        msg_erro = self.gestor_erros.processar_erro(True)
        if msg_erro:
            logger.warning(f"Erro de comunicação: {msg_erro['mensagem']}")

    def _formatar_dados(self, dados01: list, dados02: list, dados03: list, dados04: list, timestamp: str) -> Dict[
        str, Any]:
        """
        Formata os dados conforme a função 'Contrel OutputFormatedData' do Node-RED
        """

        def combinar_registos(reg_alto: int, reg_baixo: int) -> int:
            """Combina dois registos de 16 bits num valor de 32 bits"""
            return (reg_alto << 16) + reg_baixo

        return {
            "idEmpresa": self.config_contador.id_empresa,
            "timestamp": timestamp,
            "idContador": str(self.config_contador.id_contador),
            "nomeContador": self.config_contador.nome_contador,

            # Tensões L-N (V)
            "tensaoL1": round(combinar_registos(dados01[1], dados01[0]) * 0.1, 1),
            "tensaoL2": round(combinar_registos(dados01[3], dados01[2]) * 0.1, 1),
            "tensaoL3": round(combinar_registos(dados01[5], dados01[4]) * 0.1, 1),

            # Tensões L-L (V)
            "tensaoL12": round(combinar_registos(dados01[7], dados01[6]) * 0.1, 1),
            "tensaoL23": round(combinar_registos(dados01[9], dados01[8]) * 0.1, 1),
            "tensaoL31": round(combinar_registos(dados01[11], dados01[10]) * 0.1, 1),

            # Correntes (A)
            "correnteL1": round(combinar_registos(dados01[13], dados01[12]) * 0.001, 3),
            "correnteL2": round(combinar_registos(dados01[15], dados01[14]) * 0.001, 3),
            "correnteL3": round(combinar_registos(dados01[17], dados01[16]) * 0.001, 3),

            # Potências por fase (kW)
            "potenciaL1": round(combinar_registos(dados01[19], dados01[18]) * 0.0001, 4),
            "potenciaL2": round(combinar_registos(dados01[21], dados01[20]) * 0.0001, 4),
            "potenciaL3": round(combinar_registos(dados01[23], dados01[22]) * 0.0001, 4),

            # Potências totais
            "potenciaActiva": round(combinar_registos(dados01[41], dados01[40]) * 0.1, 1),  # kW
            "potenciaReactiva": round(combinar_registos(dados01[45], dados01[44]) * 0.1, 1),  # kVAr
            "potenciaAparente": round(combinar_registos(dados01[43], dados01[42]) * 0.1, 1),  # kVA
            "factorPotencia": round(dados01[49] * 0.001, 3),  # Factor de potência

            # Frequência (Hz)
            "frequencia": round(dados01[51] * 0.1, 1),

            # Energias (kWh/kVArh)
            "energiaActiva": round(combinar_registos(dados01[53], dados01[52]) * 0.1, 1),
            "energiaReactiva": round(combinar_registos(dados01[55], dados01[54]) * 0.1, 1),
            "energiaAparente": round(combinar_registos(dados02[1], dados02[0]) * 0.1, 1),

            # THD Correntes (%)
            "thdCorrenteL1": round(combinar_registos(dados03[1], dados03[0]) * 0.01, 2),
            "thdCorrenteL2": round(combinar_registos(dados03[3], dados03[2]) * 0.01, 2),
            "thdCorrenteL3": round(combinar_registos(dados03[5], dados03[4]) * 0.01, 2),

            # THD Tensões (%)
            "thdTensaoL1": round(combinar_registos(dados04[1], dados04[0]) * 0.01, 2),
            "thdTensaoL2": round(combinar_registos(dados04[3], dados04[2]) * 0.01, 2),
            "thdTensaoL3": round(combinar_registos(dados04[5], dados04[4]) * 0.01, 2)
        }


def principal():
    """Função principal"""
    # Configuração do contador (ajustar conforme necessário)
    config_contador = ConfiguracaoContador(
        id_contador=167,
        id_unidade=100,  # Endereço Modbus do contador
        nome_contador="ContadorTeste",
        id_empresa="MinhaEmpresa"
    )

    # Configuração Modbus (ajustar porta série conforme necessário)
    config_modbus = ConfiguracaoModbus(
        porta="/dev/ttyNS0",  # Ajustar conforme o vosso sistema
        velocidade=9600
    )

    # Cria o colector
    colector = ColectorDadosEM530(config_contador, config_modbus)

    try:
        # Liga
        if not colector.ligar():
            logger.error("Falha ao ligar. A encerrar...")
            return

        # Ciclo de recolha
        logger.info("A iniciar recolha de dados...")
        while True:
            dados = colector.recolher_dados()

            if dados:
                # Aqui podeis processar os dados conforme necessário
                # Por exemplo: guardar na base de dados, enviar via MQTT, etc.
                print(json.dumps(dados, indent=2, ensure_ascii=False))

            # Intervalo entre leituras (ajustar conforme necessário)
            time.sleep(30)

    except KeyboardInterrupt:
        logger.info("A parar recolha de dados...")
    except Exception as e:
        logger.error(f"Erro na execução principal: {e}")
    finally:
        colector.desligar()


if __name__ == "__main__":
    principal()