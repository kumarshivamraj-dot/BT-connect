<<<<<<< HEAD
# BT-connect
Its dope
=======
# Bluetooth Emergency Communication System

A Python-based emergency communication app using Bluetooth Low Energy (BLE) for offline message propagation with panic button functionality and responder dashboard.

## Features

### 🚨 Panic Button
- Large, prominent emergency button
- Instant alert transmission via Bluetooth
- Location tagging support
- Visual feedback (button flashing)

### 📡 Offline Message Propagation
- Mesh-like message forwarding
- Messages propagate through nearby devices
- Hop count tracking (max 5 hops)
- Duplicate message prevention
- Works without internet/cellular connection

### 👨‍🚒 Responder Dashboard
- Real-time panic alert monitoring
- Alert acknowledgment system
- Statistics tracking
- Active alerts display with color coding
- Location information

### 🔍 Network Status
- Nearby device discovery
- Message propagation logging
- Connection status monitoring
- Device list with last seen timestamps

## Installation

### Prerequisites
- Python 3.8 or higher
- Bluetooth Low Energy (BLE) capable device
- Administrator/root privileges (for Bluetooth access)

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

Or manually:
```bash
pip install bleak
```

### Step 2: Platform-Specific Setup

#### Linux
```bash
# Install BlueZ (Bluetooth stack)
sudo apt-get install bluez

# Add user to bluetooth group
sudo usermod -a -G bluetooth $USER

# Reboot for changes to take effect
```

#### macOS
- Bluetooth should work out of the box
- Grant Bluetooth permissions when prompted

#### Windows
- Ensure Bluetooth is enabled in settings
- Windows 10 version 1803 or higher recommended

## Usage

### Running the Application

```bash
python bluetooth_emergency_app.py
```

### Configuration

1. **Device Name**: Enter a unique identifier for your device
2. **Location**: Optional field for specifying your location
3. **Responder Mode**: Check this box if you're a first responder

### User Mode (Regular User)

1. Click "Start System" to activate Bluetooth communication
2. **Send Panic Alert**: Click the large red PANIC BUTTON
3. **Send Regular Message**: Type message and click "Send Message"
4. **View Messages**: All received messages appear in the Messages tab
5. **Monitor Network**: Check "Network Status" tab for nearby devices

### Responder Mode

1. Enable "Responder Mode" checkbox
2. Click "Start System"
3. **Monitor Alerts**: View all panic alerts in "Responder Dashboard" tab
4. **Acknowledge Alerts**: Select alert and click "Acknowledge Alert"
5. **View Statistics**: See total messages, panic counts, and active alerts

## How It Works

### Message Flow

```
User A (Panic!) → User B (propagates) → User C (propagates) → Responder
```

1. User sends panic alert or message
2. Nearby devices receive via Bluetooth
3. Devices automatically forward (propagate) messages
4. Messages hop through network until reaching responders
5. Duplicate prevention ensures efficiency

### Bluetooth Communication

- Uses BLE (Bluetooth Low Energy)
- Scans for nearby devices every 2 seconds
- Connects and exchanges messages
- Range: typically 10-100 meters depending on environment

### Message Structure

```json
{
  "id": "unique-message-id",
  "sender": "User_abc123",
  "content": "Help needed!",
  "is_panic": true,
  "location": "Building A, Floor 2",
  "timestamp": "2024-02-13T10:30:00",
  "hop_count": 2,
  "propagated_by": ["User_def456", "User_ghi789"]
}
```

## Use Cases

### Emergency Situations
- Natural disasters (earthquakes, floods)
- Building emergencies (fire, structural failure)
- Search and rescue operations
- Medical emergencies in remote areas

### Events & Gatherings
- Concert/festival safety
- Hiking group communication
- Campus safety systems
- Convention security

### Remote Locations
- Mountain hiking trails
- Underground facilities
- Areas with poor cellular coverage
- Maritime applications

## Features Explanation

### Offline Message Propagation
Messages don't require internet or cellular service. Each device acts as both receiver and transmitter, creating a mesh network that extends range beyond direct Bluetooth connections.

### Hop Count Limiting
Maximum 5 hops prevents infinite message loops and network congestion while ensuring good coverage.

### Responder Dashboard
Dedicated interface for emergency responders to:
- Monitor all active panic alerts
- Track alert locations
- Acknowledge handled emergencies
- View network statistics

## Troubleshooting

### Bluetooth Not Available
**Error**: "Bluetooth library not installed"
**Solution**: 
```bash
pip install bleak
```

### Permission Denied (Linux)
**Error**: Bluetooth access denied
**Solution**:
```bash
sudo usermod -a -G bluetooth $USER
# Then log out and back in
```

### No Devices Found
**Possible Causes**:
1. Bluetooth not enabled
2. No other devices running the app nearby
3. Bluetooth range exceeded (>100m)

**Solutions**:
- Verify Bluetooth is on
- Start app on multiple devices
- Move devices closer together

### Messages Not Propagating
**Check**:
1. Both devices have "Start System" activated
2. Devices are within Bluetooth range
3. No interference from other BLE devices

## Architecture

```
┌─────────────────────────────────────┐
│     EmergencyAppGUI (Tkinter)       │
│  ┌───────────┬──────────┬────────┐  │
│  │ Messaging │Dashboard │Network │  │
│  └───────────┴──────────┴────────┘  │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│   BluetoothEmergencySystem          │
│  - Message queue                    │
│  - Device discovery                 │
│  - Message propagation              │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│        Bleak (BLE Library)          │
│  - BLE scanning                     │
│  - Device connection                │
│  - Data transmission                │
└─────────────────────────────────────┘
```

## Security Considerations

⚠️ **Current Implementation**
- No message encryption (transmitted in plaintext)
- No authentication (any device can send/receive)
- No message signing (sender identity not verified)

🔒 **For Production Use, Add**:
- End-to-end encryption
- Device authentication
- Message signing
- Rate limiting
- Access control

## Future Enhancements

- [ ] GPS integration for precise location
- [ ] Message encryption
- [ ] Voice messages via Bluetooth
- [ ] Battery optimization
- [ ] Multi-language support
- [ ] Medical information sharing
- [ ] Group messaging
- [ ] Message priority levels
- [ ] Offline map integration

## License

MIT License - Feel free to modify and distribute

## Contributing

Contributions welcome! Areas for improvement:
- Security enhancements
- UI/UX improvements
- Additional platform support
- Performance optimization
- Testing coverage

## Support

For issues or questions:
1. Check Troubleshooting section
2. Verify Bluetooth hardware compatibility
3. Test with latest bleak version

## Acknowledgments

Built with:
- [Bleak](https://github.com/hbldh/bleak) - Bluetooth Low Energy library
- Tkinter - Python GUI framework
- asyncio - Asynchronous I/O

---

**Note**: This is a demonstration/prototype application. For production emergency systems, additional safety, security, and reliability measures are required.
>>>>>>> d4daf6c (first-commit)
