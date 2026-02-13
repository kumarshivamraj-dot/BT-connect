"""
Bluetooth Emergency Communication System
Features:
- Panic Button
- Offline Message Propagation (Mesh-like)
- Responder Dashboard
- Bluetooth LE Communication
"""

import asyncio
import json
import time
import uuid
from datetime import datetime
from typing import Dict, List, Set
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import queue

# Try to import bluetooth libraries
try:
    from bleak import BleakScanner, BleakClient, BleakServer
    from bleak.backends.characteristic import GattCharacteristicsFlags
    BLUETOOTH_AVAILABLE = True
except ImportError:
    BLUETOOTH_AVAILABLE = False
    print("Warning: bleak not installed. Install with: pip install bleak")


class Message:
    """Represents an emergency or regular message"""
    def __init__(self, msg_id: str = None, sender: str = "", content: str = "", 
                 is_panic: bool = False, location: str = ""):
        self.id = msg_id or str(uuid.uuid4())
        self.sender = sender
        self.content = content
        self.is_panic = is_panic
        self.location = location
        self.timestamp = datetime.now().isoformat()
        self.hop_count = 0
        self.propagated_by: Set[str] = set()
    
    def to_dict(self):
        return {
            'id': self.id,
            'sender': self.sender,
            'content': self.content,
            'is_panic': self.is_panic,
            'location': self.location,
            'timestamp': self.timestamp,
            'hop_count': self.hop_count,
            'propagated_by': list(self.propagated_by)
        }
    
    @staticmethod
    def from_dict(data: dict):
        msg = Message(
            msg_id=data['id'],
            sender=data['sender'],
            content=data['content'],
            is_panic=data['is_panic'],
            location=data.get('location', '')
        )
        msg.timestamp = data['timestamp']
        msg.hop_count = data.get('hop_count', 0)
        msg.propagated_by = set(data.get('propagated_by', []))
        return msg


class BluetoothEmergencySystem:
    """Main system for Bluetooth emergency communication"""
    
    # BLE Service and Characteristic UUIDs
    SERVICE_UUID = "12345678-1234-5678-1234-56789abcdef0"
    MESSAGE_CHAR_UUID = "12345678-1234-5678-1234-56789abcdef1"
    
    def __init__(self, device_name: str, is_responder: bool = False):
        self.device_name = device_name
        self.is_responder = is_responder
        self.messages: Dict[str, Message] = {}
        self.seen_messages: Set[str] = set()
        self.nearby_devices: Dict[str, datetime] = {}
        self.message_queue = queue.Queue()
        self.running = False
        
        # Callbacks
        self.on_message_received = None
        self.on_panic_received = None
        self.on_device_discovered = None
    
    async def start_scanning(self):
        """Scan for nearby BLE devices"""
        if not BLUETOOTH_AVAILABLE:
            print("Bluetooth not available - running in simulation mode")
            return
        
        self.running = True
        print(f"🔍 Starting BLE scan for {self.device_name}...")
        
        while self.running:
            try:
                devices = await BleakScanner.discover(timeout=5.0)
                for device in devices:
                    if device.name and "Emergency" in device.name:
                        self.nearby_devices[device.address] = datetime.now()
                        if self.on_device_discovered:
                            self.on_device_discovered(device.name, device.address)
                        
                        # Try to connect and read messages
                        await self.connect_and_read(device.address)
            except Exception as e:
                print(f"Scan error: {e}")
            
            await asyncio.sleep(2)
    
    async def connect_and_read(self, address: str):
        """Connect to a device and read messages"""
        try:
            async with BleakClient(address, timeout=10.0) as client:
                if client.is_connected:
                    # Read message characteristic
                    data = await client.read_gatt_char(self.MESSAGE_CHAR_UUID)
                    if data:
                        self.handle_received_data(data.decode())
        except Exception as e:
            print(f"Connection error to {address}: {e}")
    
    def handle_received_data(self, data: str):
        """Process received message data"""
        try:
            msg_dict = json.loads(data)
            msg = Message.from_dict(msg_dict)
            
            # Check if we've seen this message
            if msg.id in self.seen_messages:
                return
            
            self.seen_messages.add(msg.id)
            self.messages[msg.id] = msg
            
            # Notify callbacks
            if msg.is_panic and self.on_panic_received:
                self.on_panic_received(msg)
            elif self.on_message_received:
                self.on_message_received(msg)
            
            # Propagate message if under hop limit
            if msg.hop_count < 5:  # Max 5 hops
                msg.hop_count += 1
                msg.propagated_by.add(self.device_name)
                self.message_queue.put(msg)
        
        except json.JSONDecodeError:
            print(f"Invalid message data: {data}")
    
    def send_message(self, content: str, is_panic: bool = False, location: str = ""):
        """Create and queue a message for sending"""
        msg = Message(
            sender=self.device_name,
            content=content,
            is_panic=is_panic,
            location=location
        )
        self.messages[msg.id] = msg
        self.seen_messages.add(msg.id)
        self.message_queue.put(msg)
        return msg
    
    def send_panic(self, location: str = ""):
        """Send panic alert"""
        return self.send_message(
            content="🚨 EMERGENCY - IMMEDIATE ASSISTANCE NEEDED",
            is_panic=True,
            location=location
        )
    
    def stop(self):
        """Stop the system"""
        self.running = False


class EmergencyAppGUI:
    """GUI for the Emergency Communication App"""
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Bluetooth Emergency Communication System")
        self.root.geometry("900x700")
        
        # System
        self.system = None
        self.is_responder = tk.BooleanVar(value=False)
        self.device_name = tk.StringVar(value=f"User_{uuid.uuid4().hex[:6]}")
        self.location = tk.StringVar(value="")
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the user interface"""
        
        # Configuration Frame
        config_frame = ttk.LabelFrame(self.root, text="Configuration", padding=10)
        config_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(config_frame, text="Device Name:").grid(row=0, column=0, sticky=tk.W, padx=5)
        ttk.Entry(config_frame, textvariable=self.device_name, width=30).grid(row=0, column=1, padx=5)
        
        ttk.Label(config_frame, text="Location:").grid(row=0, column=2, sticky=tk.W, padx=5)
        ttk.Entry(config_frame, textvariable=self.location, width=20).grid(row=0, column=3, padx=5)
        
        ttk.Checkbutton(config_frame, text="Responder Mode", 
                       variable=self.is_responder).grid(row=0, column=4, padx=10)
        
        self.start_btn = ttk.Button(config_frame, text="Start System", 
                                    command=self.start_system)
        self.start_btn.grid(row=0, column=5, padx=5)
        
        self.stop_btn = ttk.Button(config_frame, text="Stop System", 
                                   command=self.stop_system, state=tk.DISABLED)
        self.stop_btn.grid(row=0, column=6, padx=5)
        
        # Main content area with tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Tab 1: Panic Button & Messaging
        self.messaging_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.messaging_tab, text="Messaging")
        self.setup_messaging_tab()
        
        # Tab 2: Responder Dashboard
        self.dashboard_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.dashboard_tab, text="Responder Dashboard")
        self.setup_dashboard_tab()
        
        # Tab 3: Network Status
        self.network_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.network_tab, text="Network Status")
        self.setup_network_tab()
        
        # Status bar
        self.status_var = tk.StringVar(value="System Offline")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, 
                              relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(fill=tk.X, side=tk.BOTTOM)
    
    def setup_messaging_tab(self):
        """Setup the messaging tab with panic button"""
        
        # Panic Button (Large and prominent)
        panic_frame = ttk.Frame(self.messaging_tab)
        panic_frame.pack(fill=tk.X, padx=20, pady=20)
        
        self.panic_btn = tk.Button(panic_frame, text="🚨 PANIC BUTTON 🚨",
                                   font=("Arial", 24, "bold"),
                                   bg="red", fg="white",
                                   activebackground="darkred",
                                   height=3,
                                   command=self.send_panic,
                                   state=tk.DISABLED)
        self.panic_btn.pack(fill=tk.BOTH, expand=True)
        
        # Message composition
        msg_frame = ttk.LabelFrame(self.messaging_tab, text="Send Message", padding=10)
        msg_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.message_text = tk.Text(msg_frame, height=3, width=60)
        self.message_text.pack(side=tk.LEFT, padx=5, fill=tk.BOTH, expand=True)
        
        self.send_msg_btn = ttk.Button(msg_frame, text="Send Message",
                                       command=self.send_message,
                                       state=tk.DISABLED)
        self.send_msg_btn.pack(side=tk.LEFT, padx=5)
        
        # Received messages
        received_frame = ttk.LabelFrame(self.messaging_tab, text="Messages", padding=10)
        received_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.messages_display = scrolledtext.ScrolledText(received_frame, 
                                                          wrap=tk.WORD,
                                                          height=15)
        self.messages_display.pack(fill=tk.BOTH, expand=True)
        
        # Configure tags for different message types
        self.messages_display.tag_config("panic", foreground="red", font=("Arial", 10, "bold"))
        self.messages_display.tag_config("normal", foreground="black")
        self.messages_display.tag_config("system", foreground="blue", font=("Arial", 9, "italic"))
    
    def setup_dashboard_tab(self):
        """Setup responder dashboard"""
        
        # Active alerts
        alerts_frame = ttk.LabelFrame(self.dashboard_tab, text="Active Panic Alerts", padding=10)
        alerts_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Treeview for alerts
        columns = ("Time", "Sender", "Location", "Hops", "Status")
        self.alerts_tree = ttk.Treeview(alerts_frame, columns=columns, show="tree headings")
        
        self.alerts_tree.heading("#0", text="ID")
        self.alerts_tree.column("#0", width=100)
        
        for col in columns:
            self.alerts_tree.heading(col, text=col)
            self.alerts_tree.column(col, width=120)
        
        self.alerts_tree.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(alerts_frame, orient=tk.VERTICAL, 
                                 command=self.alerts_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.alerts_tree.configure(yscrollcommand=scrollbar.set)
        
        # Action buttons
        action_frame = ttk.Frame(self.dashboard_tab)
        action_frame.pack(fill=tk.X, padx=20, pady=10)
        
        ttk.Button(action_frame, text="Acknowledge Alert",
                  command=self.acknowledge_alert).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Refresh Alerts",
                  command=self.refresh_alerts).pack(side=tk.LEFT, padx=5)
        
        # Statistics
        stats_frame = ttk.LabelFrame(self.dashboard_tab, text="Statistics", padding=10)
        stats_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.stats_text = tk.Text(stats_frame, height=5, state=tk.DISABLED)
        self.stats_text.pack(fill=tk.BOTH, expand=True)
    
    def setup_network_tab(self):
        """Setup network status tab"""
        
        # Nearby devices
        devices_frame = ttk.LabelFrame(self.network_tab, text="Nearby Devices", padding=10)
        devices_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        columns = ("Device Name", "Address", "Last Seen")
        self.devices_tree = ttk.Treeview(devices_frame, columns=columns, show="headings")
        
        for col in columns:
            self.devices_tree.heading(col, text=col)
            self.devices_tree.column(col, width=200)
        
        self.devices_tree.pack(fill=tk.BOTH, expand=True)
        
        # Message propagation log
        prop_frame = ttk.LabelFrame(self.network_tab, text="Message Propagation Log", padding=10)
        prop_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.propagation_log = scrolledtext.ScrolledText(prop_frame, height=10)
        self.propagation_log.pack(fill=tk.BOTH, expand=True)
    
    def start_system(self):
        """Start the emergency system"""
        device_name = self.device_name.get().strip()
        if not device_name:
            messagebox.showerror("Error", "Please enter a device name")
            return
        
        self.system = BluetoothEmergencySystem(
            device_name=device_name,
            is_responder=self.is_responder.get()
        )
        
        # Set callbacks
        self.system.on_message_received = self.handle_message_received
        self.system.on_panic_received = self.handle_panic_received
        self.system.on_device_discovered = self.handle_device_discovered
        
        # Start system in background thread
        if BLUETOOTH_AVAILABLE:
            threading.Thread(target=self.run_bluetooth_loop, daemon=True).start()
        else:
            self.log_message("Running in simulation mode (Bluetooth not available)")
        
        # Update UI
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.panic_btn.config(state=tk.NORMAL)
        self.send_msg_btn.config(state=tk.NORMAL)
        self.status_var.set(f"System Online - {device_name} - {'Responder' if self.is_responder.get() else 'User'}")
        
        self.log_message(f"System started: {device_name}", "system")
    
    def run_bluetooth_loop(self):
        """Run the asyncio event loop for Bluetooth"""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.system.start_scanning())
    
    def stop_system(self):
        """Stop the emergency system"""
        if self.system:
            self.system.stop()
        
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.panic_btn.config(state=tk.DISABLED)
        self.send_msg_btn.config(state=tk.DISABLED)
        self.status_var.set("System Offline")
        
        self.log_message("System stopped", "system")
    
    def send_panic(self):
        """Send panic alert"""
        if not self.system:
            return
        
        location = self.location.get().strip()
        msg = self.system.send_panic(location=location)
        
        self.log_message(f"🚨 PANIC ALERT SENT: {msg.content}", "panic")
        self.log_message(f"   Location: {location or 'Not specified'}", "panic")
        self.log_message(f"   Message ID: {msg.id[:8]}...", "system")
        
        # Flash the panic button
        self.flash_panic_button()
        
        # Add to alerts if responder
        if self.is_responder.get():
            self.add_alert_to_dashboard(msg)
    
    def send_message(self):
        """Send regular message"""
        if not self.system:
            return
        
        content = self.message_text.get("1.0", tk.END).strip()
        if not content:
            return
        
        msg = self.system.send_message(content=content, location=self.location.get())
        
        self.log_message(f"📤 Sent: {content}", "normal")
        self.message_text.delete("1.0", tk.END)
    
    def handle_message_received(self, msg: Message):
        """Handle received message"""
        self.root.after(0, lambda: self.log_message(
            f"📥 From {msg.sender}: {msg.content} (hops: {msg.hop_count})",
            "normal"
        ))
    
    def handle_panic_received(self, msg: Message):
        """Handle received panic alert"""
        def update():
            self.log_message(f"🚨 PANIC ALERT from {msg.sender}!", "panic")
            self.log_message(f"   {msg.content}", "panic")
            self.log_message(f"   Location: {msg.location or 'Unknown'}", "panic")
            self.log_message(f"   Hops: {msg.hop_count}", "system")
            
            if self.is_responder.get():
                self.add_alert_to_dashboard(msg)
                messagebox.showwarning("Panic Alert", 
                                      f"Panic alert from {msg.sender}!\nLocation: {msg.location or 'Unknown'}")
        
        self.root.after(0, update)
    
    def handle_device_discovered(self, name: str, address: str):
        """Handle discovered device"""
        def update():
            # Update devices tree
            self.devices_tree.insert("", tk.END, values=(name, address, 
                                                         datetime.now().strftime("%H:%M:%S")))
            self.propagation_log.insert(tk.END, 
                                       f"[{datetime.now().strftime('%H:%M:%S')}] Device discovered: {name}\n")
            self.propagation_log.see(tk.END)
        
        self.root.after(0, update)
    
    def add_alert_to_dashboard(self, msg: Message):
        """Add alert to responder dashboard"""
        self.alerts_tree.insert("", 0, 
                               text=msg.id[:8],
                               values=(
                                   datetime.fromisoformat(msg.timestamp).strftime("%H:%M:%S"),
                                   msg.sender,
                                   msg.location or "Unknown",
                                   msg.hop_count,
                                   "Active"
                               ),
                               tags=("panic",))
        self.alerts_tree.tag_configure("panic", background="lightcoral")
        self.update_statistics()
    
    def acknowledge_alert(self):
        """Acknowledge selected alert"""
        selection = self.alerts_tree.selection()
        if selection:
            for item in selection:
                values = list(self.alerts_tree.item(item)["values"])
                values[4] = "Acknowledged"
                self.alerts_tree.item(item, values=values, tags=("acknowledged",))
                self.alerts_tree.tag_configure("acknowledged", background="lightgreen")
            self.update_statistics()
    
    def refresh_alerts(self):
        """Refresh alerts display"""
        if self.system:
            self.update_statistics()
    
    def update_statistics(self):
        """Update statistics display"""
        if not self.system:
            return
        
        total_messages = len(self.system.messages)
        panic_count = sum(1 for msg in self.system.messages.values() if msg.is_panic)
        active_alerts = len([item for item in self.alerts_tree.get_children() 
                           if self.alerts_tree.item(item)["values"][4] == "Active"])
        
        stats_text = f"""
Total Messages: {total_messages}
Panic Alerts: {panic_count}
Active Alerts: {active_alerts}
Nearby Devices: {len(self.system.nearby_devices)}
        """
        
        self.stats_text.config(state=tk.NORMAL)
        self.stats_text.delete("1.0", tk.END)
        self.stats_text.insert("1.0", stats_text)
        self.stats_text.config(state=tk.DISABLED)
    
    def flash_panic_button(self):
        """Flash the panic button"""
        def flash(count=0):
            if count < 6:
                current_bg = self.panic_btn.cget("background")
                new_bg = "darkred" if current_bg == "red" else "red"
                self.panic_btn.config(bg=new_bg)
                self.root.after(200, lambda: flash(count + 1))
            else:
                self.panic_btn.config(bg="red")
        
        flash()
    
    def log_message(self, text: str, tag: str = "normal"):
        """Log message to display"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.messages_display.insert(tk.END, f"[{timestamp}] {text}\n", tag)
        self.messages_display.see(tk.END)


def main():
    """Main application entry point"""
    root = tk.Tk()
    app = EmergencyAppGUI(root)
    
    # Show initial info
    if not BLUETOOTH_AVAILABLE:
        messagebox.showinfo("Bluetooth Not Available",
                          "Bluetooth library not installed.\n\n"
                          "To enable Bluetooth functionality, install:\n"
                          "pip install bleak\n\n"
                          "Running in simulation mode for UI demonstration.")
    
    root.mainloop()


if __name__ == "__main__":
    main()
