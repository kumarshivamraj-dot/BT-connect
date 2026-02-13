# Quick Start Guide

## 🚀 Getting Started in 3 Steps

### Step 1: Install Dependencies
```bash
pip install bleak
```

### Step 2: Run the App
```bash
python bluetooth_emergency_app.py
```

### Step 3: Configure and Start
1. Enter your device name (e.g., "Rescuer_John" or "User_Sarah")
2. Enter your location (optional)
3. Check "Responder Mode" if you're a first responder
4. Click "Start System"

---

## 🎮 Try the Demo Mode (No Bluetooth Required)

If you don't have Bluetooth hardware or just want to see how it works:

```bash
python demo_simulation.py
```

This runs a full simulation showing:
- Network topology visualization
- Automatic message propagation
- Panic alerts with location
- Multi-hop routing
- Real-time activity log

---

## 📱 Basic Usage

### For Regular Users

**Send a Panic Alert:**
1. Make sure the system is started
2. Click the big red "🚨 PANIC BUTTON 🚨"
3. Your alert will broadcast to all nearby devices

**Send a Message:**
1. Type your message in the text box
2. Click "Send Message"
3. Message propagates through the network

### For Responders

1. Enable "Responder Mode" before starting
2. Go to "Responder Dashboard" tab
3. Monitor incoming panic alerts
4. Click an alert and "Acknowledge Alert" when handled

---

## 🔧 Common Issues & Solutions

### Issue: "Bluetooth library not installed"
**Solution:**
```bash
pip install bleak
```

### Issue: No devices found
**Solution:**
- Make sure Bluetooth is enabled on your device
- Start the app on at least 2 devices
- Keep devices within 10-100 meters of each other

### Issue: Permission denied (Linux)
**Solution:**
```bash
sudo usermod -a -G bluetooth $USER
# Log out and back in
```

---

## 📊 Understanding the Interface

### Messaging Tab
- **Panic Button**: Emergency alert (large red button)
- **Message Box**: Send regular communications
- **Message Log**: View all received messages

### Responder Dashboard
- **Active Alerts**: See all panic alerts
- **Acknowledge**: Mark alerts as handled
- **Statistics**: Network performance metrics

### Network Status
- **Nearby Devices**: List of discovered devices
- **Propagation Log**: Message routing information

---

## 💡 Tips for Best Results

1. **Keep Bluetooth On**: Enable Bluetooth and keep app running
2. **Strategic Placement**: Responders should stay in central locations
3. **Update Location**: Change location field as you move
4. **Test First**: Try the demo mode to understand how it works
5. **Battery**: Bluetooth scanning uses battery - monitor levels

---

## 🆘 Emergency Usage Scenarios

### Scenario 1: Building Emergency
```
User on Floor 5 → Panic Button
↓
User on Floor 3 (relay)
↓
User on Floor 1 (relay)
↓
Responder in Lobby (receives alert)
```

### Scenario 2: Hiking Group
```
Lost Hiker → Panic Button
↓
Nearby Hiker (relay, hop 1)
↓
Another Hiker (relay, hop 2)
↓
Group Leader/Responder (receives)
```

---

## 📝 Message Types

### Panic Alert
- ❗ Highest priority
- 🚨 Distinctive visual/audio alerts
- 📍 Includes location
- ♻️ Auto-propagated to all devices

### Regular Message
- 💬 Normal priority
- 📤 Sent to nearby devices
- 🔄 May be propagated based on network

---

## 🎯 Real-World Applications

✅ Emergency Services
✅ Disaster Response
✅ Event Safety
✅ Search & Rescue
✅ Campus Security
✅ Remote Area Communication
✅ Building Evacuation
✅ Medical Emergencies

---

## ⚡ Performance Expectations

- **Range**: 10-100 meters (varies by environment)
- **Latency**: 500ms - 2 seconds per hop
- **Max Hops**: 5 (prevents network flooding)
- **Device Limit**: No hard limit (tested up to 20)
- **Battery Impact**: Moderate (similar to other BLE apps)

---

## 🔐 Security Notice

⚠️ This is a demonstration application. For production use:
- Add encryption
- Implement authentication
- Use message signing
- Add rate limiting

---

## 📞 Support & Help

**Can't get it working?**
1. Check the full README.md for detailed troubleshooting
2. Verify Bluetooth hardware compatibility
3. Try the demo simulation mode first
4. Ensure you have Python 3.8+

**Want to contribute?**
- Improvements welcome!
- Check README.md for contribution guidelines

---

## 🎓 Learning Resources

Want to understand how it works?
1. Run `demo_simulation.py` to see the network in action
2. Check the message propagation log
3. Watch the network topology visualization
4. Monitor the statistics

---

**Ready to start? Run this command:**
```bash
python bluetooth_emergency_app.py
```

**Or try the demo:**
```bash
python demo_simulation.py
```
