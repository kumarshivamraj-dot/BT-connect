"""
BLE Server - Run this on Device 1
This device ADVERTISES and waits for connections
"""

import asyncio
import sys
from bleak import BleakServer, BleakGATTCharacteristic, BleakGATTServiceCollection
from bleak.backends.characteristic import GattCharacteristicsFlags

# Service and Characteristic UUIDs (must match on both devices)
SERVICE_UUID = "12345678-1234-5678-1234-56789abcdef0"
RX_CHAR_UUID = "12345678-1234-5678-1234-56789abcdef1"  # Server receives on this
TX_CHAR_UUID = "12345678-1234-5678-1234-56789abcdef2"  # Server sends on this

class BLEServer:
    def __init__(self, name="BLE-Server"):
        self.name = name
        self.server = None
        self.connected = False
        
    def read_request(self, characteristic: BleakGATTCharacteristic):
        """Called when client wants to read"""
        print(f"Client reading from {characteristic.uuid}")
        return b"Hello from server"
    
    def write_request(self, characteristic: BleakGATTCharacteristic, value: bytearray):
        """Called when client writes data"""
        message = value.decode('utf-8')
        print(f"\n📥 RECEIVED: {message}")
        print("Type message to send back: ", end="", flush=True)
    
    async def run(self):
        """Start the BLE server"""
        
        def on_client_connected():
            self.connected = True
            print("\n✅ Client connected!")
            print("You can now send messages.")
            print("Type message to send: ", end="", flush=True)
        
        def on_client_disconnected():
            self.connected = False
            print("\n❌ Client disconnected")
        
        # Define the GATT service
        def setup_service(service_collection: BleakGATTServiceCollection):
            # Create service
            service_collection.add_service(SERVICE_UUID)
            
            # RX Characteristic (server receives here)
            service_collection.add_characteristic(
                SERVICE_UUID,
                RX_CHAR_UUID,
                GattCharacteristicsFlags.write | GattCharacteristicsFlags.write_without_response,
                None,
                self.write_request
            )
            
            # TX Characteristic (server sends here)
            self.tx_char = service_collection.add_characteristic(
                SERVICE_UUID,
                TX_CHAR_UUID,
                GattCharacteristicsFlags.read | GattCharacteristicsFlags.notify,
                self.read_request,
                None
            )
        
        # Start server
        print(f"🔵 Starting BLE Server: {self.name}")
        print("Waiting for client to connect...")
        print("=" * 50)
        
        async with BleakServer(setup_service, self.name) as server:
            self.server = server
            
            # Set connection callbacks
            server.on_connected = on_client_connected
            server.on_disconnected = on_client_disconnected
            
            # Keep server running and allow sending messages
            try:
                while True:
                    if self.connected:
                        # Get input from user
                        message = await asyncio.get_event_loop().run_in_executor(
                            None, input
                        )
                        
                        if message.strip():
                            # Send message via notification
                            await server.notify(TX_CHAR_UUID, message.encode('utf-8'))
                            print(f"📤 SENT: {message}")
                            print("Type message to send: ", end="", flush=True)
                    else:
                        await asyncio.sleep(1)
                        
            except KeyboardInterrupt:
                print("\n\nShutting down server...")

async def main():
    print("=" * 50)
    print("BLE SERVER - Device 1")
    print("=" * 50)
    print()
    
    server_name = input("Enter your device name (e.g., 'Alice-Laptop'): ").strip()
    if not server_name:
        server_name = "BLE-Server"
    
    print()
    print("📝 Instructions:")
    print("1. Keep this server running")
    print("2. Run ble_client.py on the other laptop")
    print("3. The client will scan and connect to you")
    print("4. Start chatting!")
    print()
    
    server = BLEServer(server_name)
    await server.run()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\nServer stopped.")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure you have:")
        print("  1. Bluetooth enabled")
        print("  2. 'bleak' installed: pip install bleak")
        print("  3. Administrator/root privileges (may be needed)")
