#!/usr/bin/env python3
"""
Data collection from Lovato DMG1 counter via Modbus RTU/TCP
Based on Node-RED flow pattern and existing Lovato implementations
"""

import time
import json
import logging
from datetime import datetime
from typing import Optional, Dict, Any
import serial
from pymodbus.client.serial import ModbusSerialClient
from pymodbus.client.tcp import ModbusTcpClient
from pymodbus.exceptions import ModbusException, ConnectionException

# Import shared configuration classes
from ..common import CounterConfiguration, ModbusTCPConfiguration, ModbusRTUConfiguration

# Event logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ModbusErrorManager:
    """Modbus error manager based on Node-RED subflow"""

    def __init__(self, counter_name: str, company_id: str):
        self.counter_name = counter_name
        self.company_id = company_id
        self.error_count = 0
        self.last_error_state = False

    def process_error(self, has_error: bool) -> Optional[Dict[str, Any]]:
        """
        Process error following Node-RED logic:
        - Increment counter if there's an error
        - Reset if there's no error
        - Consider error only if count > 6 (based on Node-RED flow)
        """
        if has_error:
            self.error_count += 1
        else:
            self.error_count = 0

        current_error_state = self.error_count > 6

        # Report by exception - only report if state changed
        if current_error_state != self.last_error_state:
            self.last_error_state = current_error_state
            return self._create_error_message(current_error_state)

        return None

    def _create_error_message(self, is_error: bool) -> Dict[str, Any]:
        """Create error message based on Node-RED"""
        timestamp = datetime.now().isoformat()

        if is_error:
            topic = f"{self.company_id} Commm Error {self.counter_name} DOWN"
            message = f"{self.company_id}(ip:{getattr(self, '_host_ip', 'unknown')}) comunication with the counter {self.counter_name} is DOWN since {timestamp}"
        else:
            topic = f"{self.company_id} Commm Error {self.counter_name} Restored"
            message = f"{self.company_id} (ip:{getattr(self, '_host_ip', 'unknown')}) comunication with the counter {self.counter_name} has restored at {timestamp}"

        return {
            "topic": topic,
            "message": message,
            "timestamp": timestamp,
            "error_state": is_error
        }

    def set_host_ip(self, host_ip: str):
        """Set host IP for error messages"""
        self._host_ip = host_ip


class DMG1DataCollector:
    """Lovato DMG1 data collection"""

    def __init__(self, counter_config: CounterConfiguration, 
                 connection_config, use_tcp: bool = False):
        """
        Initialize DMG1 data collector
        
        Args:
            counter_config: Counter configuration
            connection_config: TCP or RTU configuration
            use_tcp: True for TCP, False for RTU (DMG1 typically uses RTU)
        """
        self.counter_config = counter_config
        self.connection_config = connection_config
        self.use_tcp = use_tcp
        self.client = None
        self.error_manager = ModbusErrorManager(
            counter_config.counter_name, 
            counter_config.company_id
        )
        
        # Set host IP for error reporting if using TCP
        if hasattr(connection_config, 'host'):
            self.error_manager.set_host_ip(connection_config.host)

    def connect(self) -> bool:
        """Connect to the meter"""
        try:
            if self.use_tcp:
                self.client = ModbusTcpClient(
                    host=self.connection_config.host,
                    port=self.connection_config.port,
                    timeout=self.connection_config.timeout
                )
            else:
                self.client = ModbusSerialClient(
                    port=self.connection_config.port,
                    baudrate=self.connection_config.baudrate,
                    bytesize=self.connection_config.bytesize,
                    parity=self.connection_config.parity,
                    stopbits=self.connection_config.stopbits,
                    timeout=self.connection_config.timeout
                )

            connection = self.client.connect()
            if connection:
                logger.info(f"Connected to DMG1 meter {self.counter_config.counter_name}")
                return True
            else:
                logger.error(f"Failed to connect to DMG1 meter {self.counter_config.counter_name}")
                return False

        except Exception as e:
            logger.error(f"Error connecting to DMG1 meter: {e}")
            return False

    def disconnect(self):
        """Disconnect from the meter"""
        if self.client:
            self.client.close()
            logger.info(f"Disconnected from DMG1 meter {self.counter_config.counter_name}")

    def _read_registers(self, address: int, count: int) -> Optional[list]:
        """Read modbus registers with error handling"""
        try:
            result = self.client.read_holding_registers(
                address=address,
                count=count,
                slave=self.counter_config.unit_id
            )
            
            if result.isError():
                logger.error(f"Modbus error reading registers {address}-{address+count-1}: {result}")
                return None
                
            return result.registers

        except Exception as e:
            logger.error(f"Exception reading registers {address}-{address+count-1}: {e}")
            return None

    def collect_data(self) -> Optional[Dict[str, Any]]:
        """Collect data from DMG1 meter"""
        if not self.client:
            logger.error("Client not connected")
            return None

        try:
            # TODO: Define DMG1 specific register map
            # This is a placeholder implementation - needs actual register map
            # from complete Node-RED flow
            
            # Example register reads (to be updated with actual DMG1 registers)
            voltage_data = self._read_registers(0, 6)        # Placeholder addresses
            current_data = self._read_registers(10, 6)       # Placeholder addresses
            power_data = self._read_registers(20, 8)         # Placeholder addresses
            energy_data = self._read_registers(30, 4)        # Placeholder addresses

            # Check if any read failed
            if any(data is None for data in [voltage_data, current_data, power_data, energy_data]):
                error_msg = self.error_manager.process_error(True)
                if error_msg:
                    logger.warning(f"Modbus communication error: {error_msg}")
                return None

            # Reset error count on successful read
            error_msg = self.error_manager.process_error(False)
            if error_msg:
                logger.info(f"Communication restored: {error_msg}")

            # Parse and format data
            return self._format_data(voltage_data, current_data, power_data, energy_data)

        except Exception as e:
            logger.error(f"Error collecting data from DMG1: {e}")
            error_msg = self.error_manager.process_error(True)
            if error_msg:
                logger.warning(f"Exception in data collection: {error_msg}")
            return None

    def _format_data(self, voltage_data: list, current_data: list, 
                     power_data: list, energy_data: list) -> Dict[str, Any]:
        """Format collected data according to Node-RED format"""
        
        timestamp = datetime.now().isoformat()
        
        # TODO: Parse actual register values according to DMG1 specifications
        # This is a placeholder implementation
        
        # Placeholder values - to be updated with actual parsing
        vl1 = voltage_data[0] if voltage_data else 0
        vl2 = voltage_data[1] if voltage_data else 0
        vl3 = voltage_data[2] if voltage_data else 0
        
        il1 = current_data[0] if current_data else 0
        il2 = current_data[1] if current_data else 0
        il3 = current_data[2] if current_data else 0
        
        p1 = power_data[0] if power_data else 0
        p2 = power_data[1] if power_data else 0
        p3 = power_data[2] if power_data else 0
        
        energy_active = energy_data[0] if energy_data else 0

        # Format according to standard format (to be adjusted based on actual DMG1 output)
        formatted_data = {
            "companyID": self.counter_config.company_id,
            "ts": timestamp,
            "counterID": str(self.counter_config.counter_id),
            "counterName": self.counter_config.counter_name,
            
            # Voltage measurements
            "vl1": f"{vl1:.2f}",
            "vl2": f"{vl2:.2f}",
            "vl3": f"{vl3:.2f}",
            
            # Current measurements
            "il1": f"{il1:.2f}",
            "il2": f"{il2:.2f}",
            "il3": f"{il3:.2f}",
            
            # Power measurements
            "pl1": f"{p1:.2f}",
            "pl2": f"{p2:.2f}",
            "pl3": f"{p3:.2f}",
            
            # Energy measurement
            "energyActive": f"{energy_active:.1f}",
            
            # TODO: Add other fields based on DMG1 specifications
        }
        
        return formatted_data


def main():
    """Main function for testing"""
    # Example configuration for testing
    counter_config = CounterConfiguration(
        counter_id=999,  # Placeholder ID for DMG1
        unit_id=1,
        counter_name="DMG1 Test Counter",
        company_id="TestCompany"
    )
    
    # DMG1 typically uses RTU
    rtu_config = ModbusRTUConfiguration(
        port="/dev/ttyUSB0",
        baudrate=9600,
        bytesize=8,
        parity='N',
        stopbits=1,
        timeout=3.0
    )
    
    collector = DMG1DataCollector(counter_config, rtu_config, use_tcp=False)
    
    try:
        logger.info("Starting DMG1 data collection...")
        
        if not collector.connect():
            logger.error("Failed to connect to meter")
            return
            
        while True:
            data = collector.collect_data()
            
            if data:
                # Here you can process data as needed
                # For example: save to database, send via MQTT, etc.
                print(json.dumps(data, indent=2, ensure_ascii=False))
            
            # Interval between readings (adjust as needed)
            time.sleep(30)
            
    except KeyboardInterrupt:
        logger.info("Stopping data collection...")
    except Exception as e:
        logger.error(f"Error in main execution: {e}")
    finally:
        collector.disconnect()


if __name__ == "__main__":
    main()