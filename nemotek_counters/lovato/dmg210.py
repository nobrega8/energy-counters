#!/usr/bin/env python3
"""
Recolha de dados do contador Lovato DMG210 via Modbus RTU/TCP
Baseado no Node-Red flow fornecido e na implementação do Carlo Gavazzi EM530
"""

import time
import json
import logging
from datetime import datetime
from dataclasses import dataclass
from typing import Optional, Dict, Any
import serial
from pymodbus.client.serial import ModbusSerialClient
from pymodbus.client.tcp import ModbusTcpClient
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
class ConfiguracaoModbusTCP:
    """Configuração da ligação Modbus TCP"""
    host: str = "192.168.1.100"
    porta: int = 502
    timeout: float = 4.0


@dataclass
class ConfiguracaoModbusRTU:
    """Configuração da ligação Modbus RTU"""
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


class ColectorDadosDMG210:
    """Recolha de dados do Lovato DMG210"""

    def __init__(self, config_contador: ConfiguracaoContador, 
                 config_modbus_tcp: Optional[ConfiguracaoModbusTCP] = None,
                 config_modbus_rtu: Optional[ConfiguracaoModbusRTU] = None):
        self.config_contador = config_contador
        self.config_modbus_tcp = config_modbus_tcp
        self.config_modbus_rtu = config_modbus_rtu
        self.cliente = None
        self.tipo_conexao = None
        self.gestor_erros = GestorErrosModbus(
            config_contador.nome_contador,
            config_contador.id_empresa
        )

        # Validar que pelo menos uma configuração foi fornecida
        if not config_modbus_tcp and not config_modbus_rtu:
            raise ValueError("Deve fornecer pelo menos uma configuração Modbus (TCP ou RTU)")

    def ligar(self) -> bool:
        """Estabelece ligação Modbus TCP ou RTU"""
        try:
            # Tentar TCP primeiro, se disponível
            if self.config_modbus_tcp:
                return self._ligar_tcp()
            elif self.config_modbus_rtu:
                return self._ligar_rtu()
            
            return False

        except Exception as e:
            logger.error(f"Erro ao ligar: {e}")
            return False

    def _ligar_tcp(self) -> bool:
        """Estabelece ligação Modbus TCP"""
        try:
            self.cliente = ModbusTcpClient(
                host=self.config_modbus_tcp.host,
                port=self.config_modbus_tcp.porta,
                timeout=self.config_modbus_tcp.timeout
            )

            if self.cliente.connect():
                self.tipo_conexao = "TCP"
                logger.info(f"Ligado ao dispositivo Modbus TCP em {self.config_modbus_tcp.host}:{self.config_modbus_tcp.porta}")
                return True
            else:
                logger.error("Falha ao ligar ao dispositivo Modbus TCP")
                return False

        except Exception as e:
            logger.error(f"Erro ao ligar TCP: {e}")
            # Se TCP falhar, tentar RTU se disponível
            if self.config_modbus_rtu:
                return self._ligar_rtu()
            return False

    def _ligar_rtu(self) -> bool:
        """Estabelece ligação Modbus RTU"""
        try:
            self.cliente = ModbusSerialClient(
                port=self.config_modbus_rtu.porta,
                baudrate=self.config_modbus_rtu.velocidade,
                bytesize=self.config_modbus_rtu.bits_dados,
                parity=self.config_modbus_rtu.paridade,
                stopbits=self.config_modbus_rtu.bits_paragem,
                timeout=self.config_modbus_rtu.timeout
            )

            if self.cliente.connect():
                self.tipo_conexao = "RTU"
                logger.info(f"Ligado ao dispositivo Modbus RTU na porta {self.config_modbus_rtu.porta}")
                return True
            else:
                logger.error("Falha ao ligar ao dispositivo Modbus RTU")
                return False

        except Exception as e:
            logger.error(f"Erro ao ligar RTU: {e}")
            return False

    def desligar(self):
        """Desliga do dispositivo Modbus"""
        if self.cliente:
            self.cliente.close()
            logger.info(f"Desligado do dispositivo Modbus {self.tipo_conexao}")

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
        """Recolhe todos os dados seguindo a sequência do Node-RED DMG210"""
        timestamp = datetime.now().isoformat()

        try:
            # Leitura 1: Endereço 2, 24 registos (dados instantâneos)
            dados01 = self.ler_registos(2, 24)
            if dados01 is None:
                self._processar_erro_comunicacao()
                return None

            # Leitura 2: Endereço 0x32 (50), 38 registos (frequência, equivalentes, THD)
            dados02 = self.ler_registos(0x32, 38)
            if dados02 is None:
                self._processar_erro_comunicacao()
                return None

            # Leitura 3: Endereço 6687, 10 registos (energias)
            dados03 = self.ler_registos(6687, 10)
            if dados03 is None:
                self._processar_erro_comunicacao()
                return None

            # Processa sucesso na comunicação
            msg_erro = self.gestor_erros.processar_erro(False)
            if msg_erro:
                logger.info(f"Comunicação restaurada: {msg_erro['mensagem']}")

            # Formata dados conforme função Node-RED
            dados_formatados = self._formatar_dados(dados01, dados02, dados03, timestamp)
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

    def _formatar_dados(self, dados01: list, dados02: list, dados03: list, timestamp: str) -> Dict[str, Any]:
        """
        Formata os dados conforme a configuração do Node-RED DMG210
        """

        def uint32_from_registers(reg_alto: int, reg_baixo: int) -> int:
            """Converte dois registos de 16 bits num valor uint32 big-endian"""
            return (reg_alto << 16) + reg_baixo

        def int32_from_registers(reg_alto: int, reg_baixo: int) -> int:
            """Converte dois registos de 16 bits num valor int32 big-endian"""
            value = (reg_alto << 16) + reg_baixo
            # Converte para signed int32
            if value > 0x7FFFFFFF:
                value -= 0x100000000
            return value

        return {
            "idEmpresa": self.config_contador.id_empresa,
            "timestamp": timestamp,
            "idContador": str(self.config_contador.id_contador),
            "nomeContador": self.config_contador.nome_contador,

            # Dados instantâneos (dados01) - conforme parser instant
            # Tensões L-N (V) - uint32be scale 0.01
            "vl1": round(uint32_from_registers(dados01[0], dados01[1]) * 0.01, 2),
            "vl2": round(uint32_from_registers(dados01[2], dados01[3]) * 0.01, 2),
            "vl3": round(uint32_from_registers(dados01[4], dados01[5]) * 0.01, 2),

            # Correntes (A) - uint32be scale 0.0001
            "il1": round(uint32_from_registers(dados01[6], dados01[7]) * 0.0001, 4),
            "il2": round(uint32_from_registers(dados01[8], dados01[9]) * 0.0001, 4),
            "il3": round(uint32_from_registers(dados01[10], dados01[11]) * 0.0001, 4),

            # Tensões L-L (V) - uint32be scale 0.01
            "vl12": round(uint32_from_registers(dados01[12], dados01[13]) * 0.01, 2),
            "vl23": round(uint32_from_registers(dados01[14], dados01[15]) * 0.01, 2),
            "vl31": round(uint32_from_registers(dados01[16], dados01[17]) * 0.01, 2),

            # Potências por fase (kW) - int32be scale 0.01
            "p1": round(int32_from_registers(dados01[18], dados01[19]) * 0.01, 2),
            "p2": round(int32_from_registers(dados01[20], dados01[21]) * 0.01, 2),
            "p3": round(int32_from_registers(dados01[22], dados01[23]) * 0.01, 2),

            # Dados equivalentes (dados02) - conforme parser instant
            # Frequência (Hz) - uint32be scale 0.01
            "freq": round(uint32_from_registers(dados02[0], dados02[1]) * 0.01, 2),

            # Valores equivalentes
            "veq": round(uint32_from_registers(dados02[2], dados02[3]) * 0.01, 2),
            "veql": round(uint32_from_registers(dados02[4], dados02[5]) * 0.01, 2),
            "ieq": round(uint32_from_registers(dados02[6], dados02[7]) * 0.0001, 4),

            # Potências equivalentes (kW/kVAr/kVA)
            "peq": round(int32_from_registers(dados02[8], dados02[9]) * 0.01, 2),
            "qeq": round(int32_from_registers(dados02[10], dados02[11]) * 0.01, 2),
            "seq": round(uint32_from_registers(dados02[12], dados02[13]) * 0.01, 2),
            "pfeq": round(uint32_from_registers(dados02[14], dados02[15]) * 0.0001, 4),

            # THD Tensões (%)
            "thdV1": round(uint32_from_registers(dados02[26], dados02[27]) * 0.01, 2),
            "thdV2": round(uint32_from_registers(dados02[28], dados02[29]) * 0.01, 2),
            "thdV3": round(uint32_from_registers(dados02[30], dados02[31]) * 0.01, 2),

            # THD Correntes (%)
            "thdIL1": round(uint32_from_registers(dados02[32], dados02[33]) * 0.01, 2),
            "thdIL2": round(uint32_from_registers(dados02[34], dados02[35]) * 0.01, 2),
            "thdIL3": round(uint32_from_registers(dados02[36], dados02[37]) * 0.01, 2),

            # Energias (dados03) - conforme parser energy
            # int32be scale 0.1
            "energiaActiva": round(int32_from_registers(dados03[0], dados03[1]) * 0.1, 1),
            "energiaReactiva": round(int32_from_registers(dados03[4], dados03[5]) * 0.1, 1),
            "energiaAparente": round(int32_from_registers(dados03[8], dados03[9]) * 0.1, 1),
        }


def principal():
    """Função principal para teste"""
    # Configuração do contador (ajustar conforme necessário)
    config_contador = ConfiguracaoContador(
        id_contador=115,
        id_unidade=81,  # Endereço Modbus do contador
        nome_contador="Geral #115",
        id_empresa="MinhaEmpresa"
    )

    # Configuração Modbus TCP (ajustar conforme necessário)
    config_modbus_tcp = ConfiguracaoModbusTCP(
        host="172.16.5.11",
        porta=502
    )

    # Configuração Modbus RTU (como fallback)
    config_modbus_rtu = ConfiguracaoModbusRTU(
        porta="/dev/ttyNS0",
        velocidade=9600
    )

    # Cria o colector com ambas as configurações
    colector = ColectorDadosDMG210(config_contador, config_modbus_tcp, config_modbus_rtu)

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