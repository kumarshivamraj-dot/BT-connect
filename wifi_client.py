"""
WiFi Chat Client - Run on Device 2
Connects to the WiFi server
"""

import socket
import threading
import sys

def receive_messages(client_socket):
    """Listen for incoming messages"""
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print(f"\n📥 Them: {message}")
                print("You: ", end="", flush=True)
            else:
                break
        except:
            break
    
    print("\n❌ Connection closed")

def start_client():
    """Connect to server and start chatting"""
    
    print("=" * 60)
    print("📱 WIFI CHAT CLIENT")
    print("=" * 60)
    print()
    print("📝 Instructions:")
    print("   1. The server will show you an IP address")
    print("   2. Enter that IP address below")
    print("   3. Start chatting!")
    print()
    
    # Get server IP
    server_ip = input("Enter server IP address: ").strip()
    
    if not server_ip:
        print("❌ No IP address entered")
        return
    
    print(f"\n🔗 Connecting to {server_ip}:5555...")
    
    try:
        # Create socket and connect
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((server_ip, 5555))
        
        print(f"✅ Connected to server!")
        print()
        print("=" * 60)
        print("💬 CHAT STARTED - Type your messages")
        print("=" * 60)
        print()
        
        # Start receiving thread
        receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
        receive_thread.daemon = True
        receive_thread.start()
        
        # Send messages
        print("You: ", end="", flush=True)
        while True:
            try:
                message = input()
                if message.lower() == 'quit':
                    break
                
                client_socket.send(message.encode('utf-8'))
                print("You: ", end="", flush=True)
                
            except KeyboardInterrupt:
                break
            except:
                print("\n❌ Connection lost")
                break
        
        client_socket.close()
        print("\n👋 Disconnected")
        
    except ConnectionRefusedError:
        print(f"\n❌ Cannot connect to {server_ip}:5555")
        print("\nMake sure:")
        print("  1. Server is running")
        print("  2. IP address is correct")
        print("  3. Both laptops on same WiFi network")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    try:
        start_client()
    except Exception as e:
        print(f"\n❌ Error: {e}")
