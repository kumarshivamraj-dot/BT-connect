"""
Simulation Demo - Bluetooth Emergency Communication System
Demonstrates the app functionality without requiring actual Bluetooth hardware
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import uuid
import time
import threading
from datetime import datetime
from typing import Dict, List
import random


class SimulatedMessage:
    """Simulated emergency message"""
    def __init__(self, sender: str, content: str, is_panic: bool = False, location: str = ""):
        self.id = str(uuid.uuid4())
        self.sender = sender
        self.content = content
        self.is_panic = is_panic
        self.location = location
        self.timestamp = datetime.now().isoformat()
        self.hop_count = 0


class SimulationDemo:
    """Simulation demo of the emergency communication system"""
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Emergency Communication System - SIMULATION DEMO")
        self.root.geometry("1000x750")
        
        self.running = False
        self.messages: List[SimulatedMessage] = []
        self.simulated_devices = ["Responder_Alpha", "User_Bob", "User_Carol", "User_David"]
        
        self.setup_ui()
        
        # Auto-start simulation
        self.root.after(1000, self.show_welcome)
    
    def setup_ui(self):
        """Setup UI"""
        
        # Header
        header = tk.Label(self.root, 
                         text="🚨 Bluetooth Emergency Communication - DEMO MODE 🚨",
                         font=("Arial", 16, "bold"),
                         bg="#FF6B6B", fg="white", pady=10)
        header.pack(fill=tk.X)
        
        info = tk.Label(self.root,
                       text="This demo simulates Bluetooth mesh networking without requiring actual hardware",
                       font=("Arial", 10),
                       bg="#FFE66D", pady=5)
        info.pack(fill=tk.X)
        
        # Control panel
        control_frame = ttk.LabelFrame(self.root, text="Simulation Controls", padding=10)
        control_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(control_frame, text="▶️ Start Simulation",
                  command=self.start_simulation).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="⏸️ Stop Simulation",
                  command=self.stop_simulation).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="🚨 Send Simulated Panic",
                  command=self.simulate_panic).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="💬 Send Simulated Message",
                  command=self.simulate_message).pack(side=tk.LEFT, padx=5)
        
        # Main content
        content_frame = ttk.Frame(self.root)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Left: Network visualization
        left_frame = ttk.LabelFrame(content_frame, text="Network Topology", padding=10)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        self.canvas = tk.Canvas(left_frame, bg="white", width=400, height=400)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Right: Message log
        right_frame = ttk.LabelFrame(content_frame, text="Message Activity Log", padding=10)
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        self.log_display = scrolledtext.ScrolledText(right_frame, wrap=tk.WORD, height=20)
        self.log_display.pack(fill=tk.BOTH, expand=True)
        
        # Configure tags
        self.log_display.tag_config("panic", foreground="red", font=("Arial", 10, "bold"))
        self.log_display.tag_config("normal", foreground="black")
        self.log_display.tag_config("system", foreground="blue", font=("Arial", 9, "italic"))
        self.log_display.tag_config("propagate", foreground="green")
        
        # Bottom: Statistics
        stats_frame = ttk.LabelFrame(self.root, text="Network Statistics", padding=10)
        stats_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.stats_label = tk.Label(stats_frame, text="Waiting for simulation to start...",
                                    font=("Courier", 10), justify=tk.LEFT)
        self.stats_label.pack()
        
        # Status bar
        self.status_var = tk.StringVar(value="Demo Mode - Ready to Start")
        status_bar = ttk.Label(self.root, textvariable=self.status_var,
                              relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(fill=tk.X, side=tk.BOTTOM)
    
    def show_welcome(self):
        """Show welcome message"""
        messagebox.showinfo("Welcome to Demo Mode",
                          "This simulation demonstrates:\n\n"
                          "✓ Panic button functionality\n"
                          "✓ Message propagation through mesh network\n"
                          "✓ Multi-hop routing (up to 5 hops)\n"
                          "✓ Responder dashboard\n"
                          "✓ Network visualization\n\n"
                          "Click 'Start Simulation' to begin!")
    
    def start_simulation(self):
        """Start the simulation"""
        if self.running:
            return
        
        self.running = True
        self.status_var.set("Simulation Active - Devices Online")
        self.log("🔵 Simulation started - Network initializing...", "system")
        
        # Draw network
        self.draw_network()
        
        # Start simulation thread
        threading.Thread(target=self.simulation_loop, daemon=True).start()
    
    def stop_simulation(self):
        """Stop the simulation"""
        self.running = False
        self.status_var.set("Simulation Stopped")
        self.log("🔴 Simulation stopped", "system")
    
    def simulation_loop(self):
        """Main simulation loop"""
        while self.running:
            time.sleep(random.uniform(3, 7))
            
            if random.random() < 0.3:  # 30% chance of activity
                if random.random() < 0.2:  # 20% of activity is panic
                    self.simulate_panic(auto=True)
                else:
                    self.simulate_message(auto=True)
    
    def simulate_panic(self, auto=False):
        """Simulate a panic alert"""
        sender = random.choice(self.simulated_devices[1:])  # Not from responder
        location = random.choice([
            "Building A, Floor 3",
            "Parking Lot B",
            "Conference Room 201",
            "Cafeteria",
            "Emergency Exit 4"
        ])
        
        msg = SimulatedMessage(
            sender=sender,
            content="🚨 EMERGENCY - IMMEDIATE ASSISTANCE NEEDED",
            is_panic=True,
            location=location
        )
        
        self.messages.append(msg)
        self.log(f"🚨 PANIC ALERT from {sender}!", "panic")
        self.log(f"   Location: {location}", "panic")
        self.log(f"   Message ID: {msg.id[:8]}...", "system")
        
        # Simulate propagation
        self.simulate_propagation(msg)
        
        # Flash visualization
        self.flash_device(sender)
        
        self.update_stats()
    
    def simulate_message(self, auto=False):
        """Simulate a regular message"""
        sender = random.choice(self.simulated_devices)
        contents = [
            "Status check - all clear",
            "Need supplies at station 2",
            "Moving to checkpoint B",
            "Requesting backup",
            "Area secured"
        ]
        
        msg = SimulatedMessage(
            sender=sender,
            content=random.choice(contents),
            is_panic=False
        )
        
        self.messages.append(msg)
        self.log(f"📤 {sender}: {msg.content}", "normal")
        
        # Simulate propagation
        if random.random() < 0.5:  # 50% get propagated
            self.simulate_propagation(msg)
        
        self.update_stats()
    
    def simulate_propagation(self, msg: SimulatedMessage):
        """Simulate message propagation through network"""
        num_hops = random.randint(1, 4)
        
        for hop in range(num_hops):
            time.sleep(0.3)
            relay = random.choice(self.simulated_devices)
            msg.hop_count = hop + 1
            
            self.root.after(0, lambda r=relay, h=hop+1: 
                          self.log(f"   ↪️ Hop {h}: Relayed by {r}", "propagate"))
            
            # Draw propagation line
            self.root.after(0, lambda: self.draw_propagation_effect())
        
        # Received by responder
        if num_hops > 0:
            self.root.after(0, lambda: 
                          self.log(f"   ✅ Received by Responder_Alpha", "system"))
    
    def draw_network(self):
        """Draw network topology visualization"""
        self.canvas.delete("all")
        
        # Calculate positions for devices in a circle
        center_x, center_y = 200, 200
        radius = 120
        
        positions = {}
        for i, device in enumerate(self.simulated_devices):
            angle = (2 * 3.14159 * i) / len(self.simulated_devices)
            x = center_x + radius * (1.5 if i == 0 else 1) * (0 if i == 0 else __import__('math').cos(angle))
            y = center_y + radius * (1.5 if i == 0 else 1) * (0 if i == 0 else __import__('math').sin(angle))
            
            if i == 0:  # Responder in center
                x, y = center_x, center_y
            
            positions[device] = (x, y)
            
            # Draw connections
            for other_device in self.simulated_devices:
                if other_device != device:
                    ox, oy = positions.get(other_device, (0, 0))
                    if ox != 0:  # Only if other position exists
                        self.canvas.create_line(x, y, ox, oy, fill="lightgray", width=1, dash=(2, 4))
            
            # Draw device node
            color = "red" if i == 0 else "lightblue"
            self.canvas.create_oval(x-25, y-25, x+25, y+25, fill=color, outline="black", width=2, tags=device)
            self.canvas.create_text(x, y, text=device.split('_')[1], font=("Arial", 9, "bold"))
        
        self.device_positions = positions
    
    def draw_propagation_effect(self):
        """Draw a propagation effect"""
        # Random line between devices
        device1 = random.choice(self.simulated_devices)
        device2 = random.choice([d for d in self.simulated_devices if d != device1])
        
        x1, y1 = self.device_positions[device1]
        x2, y2 = self.device_positions[device2]
        
        line = self.canvas.create_line(x1, y1, x2, y2, fill="yellow", width=3, tags="propagation")
        self.root.after(500, lambda: self.canvas.delete(line))
    
    def flash_device(self, device: str):
        """Flash a device node"""
        def flash(count=0):
            if count < 6 and device in self.device_positions:
                x, y = self.device_positions[device]
                if count % 2 == 0:
                    self.canvas.create_oval(x-30, y-30, x+30, y+30, 
                                          outline="red", width=3, tags="flash")
                else:
                    self.canvas.delete("flash")
                self.root.after(200, lambda: flash(count + 1))
        
        flash()
    
    def log(self, message: str, tag: str = "normal"):
        """Log message to display"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_display.insert(tk.END, f"[{timestamp}] {message}\n", tag)
        self.log_display.see(tk.END)
    
    def update_stats(self):
        """Update statistics display"""
        total = len(self.messages)
        panics = sum(1 for m in self.messages if m.is_panic)
        regular = total - panics
        avg_hops = sum(m.hop_count for m in self.messages) / max(total, 1)
        
        stats = f"""Total Messages: {total} | Panic Alerts: {panics} | Regular: {regular} | Avg Hops: {avg_hops:.1f}
Active Devices: {len(self.simulated_devices)} | Network Coverage: 100% | Latency: ~500ms"""
        
        self.stats_label.config(text=stats)


def main():
    """Run the simulation demo"""
    root = tk.Tk()
    demo = SimulationDemo(root)
    root.mainloop()


if __name__ == "__main__":
    main()
