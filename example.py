#!/usr/bin/env python3
"""
Example usage of nemotek-counters library

This script demonstrates how to use the library to read data from 
a Carlo Gavazzi EM530 energy meter.
"""

import time
import json
from nemotek_counters.carlo_gavazzi.em530 import (
    ConfiguracaoContador,
    ConfiguracaoModbus, 
    ColectorDadosEM530
)


def exemplo_carlo_gavazzi_em530():
    """Example of using Carlo Gavazzi EM530 counter"""
    print("Nemotek Counters Library - Carlo Gavazzi EM530 Example")
    print("=" * 55)
    
    # Configure the counter
    config_contador = ConfiguracaoContador(
        id_contador=167,
        id_unidade=100,  # Modbus address of the counter
        nome_contador="ContadorTeste",
        id_empresa="MinhaEmpresa"
    )
    
    # Configure Modbus connection (adjust port according to your system)
    config_modbus = ConfiguracaoModbus(
        porta="/dev/ttyNS0",  # Change this to your serial port
        velocidade=9600
    )
    
    # Create the data collector
    colector = ColectorDadosEM530(config_contador, config_modbus)
    
    try:
        # Connect to the device
        print(f"Connecting to counter {config_contador.nome_contador}...")
        if not colector.ligar():
            print("❌ Failed to connect to the counter")
            return
            
        print("✅ Successfully connected!")
        print("\nReading data (press Ctrl+C to stop)...")
        
        # Data collection loop
        while True:
            dados = colector.recolher_dados()
            
            if dados:
                print(f"\n📊 Data collected at {dados['timestamp']}")
                print(f"   Voltage L1: {dados['tensaoL1']}V")
                print(f"   Current L1: {dados['correnteL1']}A") 
                print(f"   Active Power: {dados['potenciaActiva']}kW")
                print(f"   Frequency: {dados['frequencia']}Hz")
                
                # You can process the data here as needed
                # For example: save to database, send via MQTT, etc.
            else:
                print("⚠️  Failed to read data from counter")
                
            # Wait before next reading
            time.sleep(30)
            
    except KeyboardInterrupt:
        print("\n🛑 Stopping data collection...")
    except Exception as e:
        print(f"❌ Error during execution: {e}")
    finally:
        colector.desligar()
        print("🔌 Disconnected from counter")


def mostrar_contadores_disponiveis():
    """Show available counters in the library"""
    print("Nemotek Counters Library - Available Counters")
    print("=" * 45)
    
    counters = {
        "Carlo Gavazzi": ["EM530 (implemented)"],
        "Contrel": ["uD3h (to be implemented)"],
        "Diris": ["A10 (to be implemented)"],
        "Lovato": ["DMG800 (to be implemented)", 
                  "DMG210 (to be implemented)", 
                  "DMG6 (to be implemented)"],
        "RedZ": ["LKM144 (to be implemented)"],
        "Schneider": ["IEM3250 (to be implemented)", 
                     "IEM3155 (to be implemented)"]
    }
    
    for manufacturer, models in counters.items():
        print(f"\n📟 {manufacturer}:")
        for model in models:
            print(f"   • {model}")
    
    print(f"\nTo use a counter:")
    print(f"   from nemotek_counters.carlo_gavazzi import em530")
    print(f"   # Then use the classes and functions from the module")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--list":
        mostrar_contadores_disponiveis()
    else:
        print("Note: This example requires a physical Carlo Gavazzi EM530")
        print("counter connected via Modbus RTU. Adjust the serial port")
        print("configuration in the script according to your setup.\n")
        
        resposta = input("Do you want to continue? (y/N): ")
        if resposta.lower() == 'y':
            exemplo_carlo_gavazzi_em530()
        else:
            print("Example cancelled. Use --list to see available counters.")