"""
BLE Client - Run this on Device 2
This device SCANS and CONNECTS to the server
"""

import asyncio
from bleak import BleakScanner, BleakClient

# Service and Characteristic UUIDs (must match server)
SERVICE_UUID = "12345678-1234-5678-1234-56789abcdef0"
RX_CHAR_UUID = "12345678-1234-5678-1234-56789abcdef1"  # Client writes to this
TX_CHAR_UUID = "12345678-1234-5678-1234-56789abcdef2"  # Client reads from this

class BLEClient:
    def __init__(self):
        self.client = None
        self.connected = False
        
    def on_notification(self, sender, data):
        """Called when server sends a message"""
        message = data.decode('utf-8')
        print(f"\n📥 RECEIVED: {message}")
        print("Type message to send: ", end="", flush=True)
    
    async def scan_for_server(self):
        """Scan for BLE servers"""
        print("🔍 Scanning for BLE devices...")
        print("(This may take 5-10 seconds...)")
        
        devices = await BleakScanner.discover(timeout=10.0)
        
        print(f"\n✅ Found {len(devices)} devices:")
        print()
        
        valid_devices = []
        for i, device in enumerate(devices):
            if device.name:  # Only show named devices
                print(f"  [{i}] {device.name}")
                print(f"      Address: {device.address}")
                print()
                valid_devices.append(device)
        
        if not valid_devices:
            print("❌ No devices found!")
            print("\nTroubleshooting:")
            print("  1. Make sure the server is running on the other laptop")
            print("  2. Bluetooth is ON on both devices")
            print("  3. Devices are close to each other (within 10m)")
            return None
        
        print(f"Found {len(valid_devices)} devices")
        choice = int(input("Enter device number to connect: "))
        
        if 0 <= choice < len(valid_devices):
            return valid_devices[choice]
        return None
    
    async def connect(self, device):
        """Connect to a BLE server"""
        print(f"\n🔗 Connecting to {device.name} ({device.address})...")
        
        self.client = BleakClient(device.address, timeout=20.0)
        
        try:
            await self.client.connect()
            
            if self.client.is_connected:
                print(f"✅ Connected to {device.name}!")
                self.connected = True
                
                # Subscribe to notifications (receive messages)
                await self.client.start_notify(TX_CHAR_UUID, self.on_notification)
                print("\n👂 Listening for messages...")
                print("Type message to send: ", end="", flush=True)
                
                return True
            else:
                print("❌ Connection failed")
                return False
                
        except Exception as e:
            print(f"❌ Connection error: {e}")
            return False
    
    async def send_message(self, message):
        """Send message to server"""
        if not self.connected or not self.client:
            print("❌ Not connected!")
            return False
        
        try:
            # Write to RX characteristic (server receives here)
            await self.client.write_gatt_char(
                RX_CHAR_UUID, 
                message.encode('utf-8'),
                response=False
            )
            print(f"📤 SENT: {message}")
            return True
            
        except Exception as e:
            print(f"❌ Send error: {e}")
            return False
    
    async def chat_loop(self):
        """Main chat loop"""
        try:
            while self.connected:
                # Get message from user
                message = await asyncio.get_event_loop().run_in_executor(
                    None, input
                )
                
                if message.strip():
                    await self.send_message(message)
                    print("Type message to send: ", end="", flush=True)
                    
        except KeyboardInterrupt:
            print("\n\nDisconnecting...")
        finally:
            if self.client and self.client.is_connected:
                await self.client.disconnect()
                print("✅ Disconnected")

async def main():
    print("=" * 50)
    print("BLE CLIENT - Device 2")
    print("=" * 50)
    print()
    
    print("📝 Instructions:")
    print("1. Make sure ble_server.py is running on the other laptop")
    print("2. This will scan and connect to it")
    print("3. Start chatting!")
    print()
    
    input("Press Enter to start scanning...")
    print()
    
    client = BLEClient()
    
    # Scan for devices
    device = await client.scan_for_server()
    
    if not device:
        print("\n❌ No device selected. Exiting.")
        return
    
    # Connect to selected device
    connected = await client.connect(device)
    
    if not connected:
        print("\n❌ Failed to connect. Exiting.")
        return
    
    # Start chatting
    print()
    print("=" * 50)
    print("💬 CHAT STARTED")
    print("=" * 50)
    print()
    
    await client.chat_loop()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\nClient stopped.")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure you have:")
        print("  1. Bluetooth enabled")
        print("  2. 'bleak' installed: pip install bleak")
        print("  3. Server running on the other laptop")
