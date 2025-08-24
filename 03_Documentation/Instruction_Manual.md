# TriAxis Pro - Instruction Manual
**Professional 3-Axis Stepper Motor Controller**

*Developed by: Amol M.*  
*Company: APEX PRECISION MECHATRONIX PVT. LTD.*

---

## 📦 Package Contents

### Hardware Components
- **Arduino ESP32 Development Board**
- **3x Stepper Motor Driver Modules (A4988/DRV8825)**
- **3x NEMA 17 Stepper Motors**
- **Power Supply (12V/5A)**
- **Emergency Stop Button**
- **3x Limit Switches**
- **Status LED**
- **Connecting Cables & Jumper Wires**
- **Mounting Hardware**

### Software Components
- **TriAxis Pro Mobile App** (Android/iOS)
- **Arduino Firmware** (TriAxis_Controller.ino)
- **USB Programming Cable**

---

## 🔧 Hardware Setup

### Step 1: Arduino ESP32 Connections

#### Stepper Motor Connections
```
X-Axis Motor:
- Step Pin: GPIO 2
- Direction Pin: GPIO 3

Y-Axis Motor:
- Step Pin: GPIO 4  
- Direction Pin: GPIO 5

Z-Axis Motor:
- Step Pin: GPIO 6
- Direction Pin: GPIO 7

Motor Enable: GPIO 8 (Common to all drivers)
```

#### Safety & Control Connections
```
Emergency Stop: GPIO 9 (Pull-up enabled)
X-Limit Switch: GPIO 10 (Pull-up enabled)
Y-Limit Switch: GPIO 11 (Pull-up enabled)  
Z-Limit Switch: GPIO 12 (Pull-up enabled)
Status LED: GPIO 13
```

#### Power Connections
```
ESP32: 5V from USB or external 5V supply
Motor Drivers: 12V from external power supply
Motors: Connect to driver outputs (A+, A-, B+, B-)
```

### Step 2: Driver Configuration
1. **Set microstepping** on A4988/DRV8825 drivers
2. **Adjust current limit** using potentiometer
3. **Connect motor coils** according to datasheet
4. **Verify wiring** before powering on

### Step 3: Safety Installation
1. **Mount emergency stop** in accessible location
2. **Install limit switches** at axis endpoints
3. **Secure all connections** to prevent disconnection
4. **Test emergency stop** before operation

---

## 💻 Software Installation

### Arduino Firmware Upload

#### Required Libraries
Install these libraries in Arduino IDE:
```
- WiFi (ESP32 Core)
- BluetoothSerial (ESP32 Core)
- AccelStepper (by Mike McCauley)
- ArduinoJson (by Benoit Blanchon)
```

#### Upload Steps
1. **Connect ESP32** to computer via USB
2. **Select board**: "ESP32 Dev Module"
3. **Select port**: Choose correct COM port
4. **Open** TriAxis_Controller.ino
5. **Upload** firmware to ESP32
6. **Monitor serial** output for startup messages

#### WiFi Configuration
Default settings in code:
```cpp
SSID: "TriAxis_Controller"
Password: "APEX2024"
IP Address: 192.168.4.1
```

### Mobile App Installation
1. **Download** TriAxis Pro app from app store
2. **Install** on Android (8.0+) or iOS (12.0+)
3. **Grant permissions** for Bluetooth and location
4. **Launch** app and proceed to connection setup

---

## 📱 Mobile App Usage

### Initial Setup

#### 1. Connection Tab
- **Select connection type**: Bluetooth or WiFi
- **Scan for devices**: Tap "Scan for Devices"
- **Choose controller**: Select "TriAxis_Motor_Hub"
- **Connect**: Tap "Connect" button
- **Verify status**: Check green connection indicator

#### 2. First-Time Calibration
- **Go to Manual tab** after connection
- **Home all axes**: Use individual axis controls
- **Set zero positions**: Reset position counters
- **Test movements**: Verify all axes respond correctly

### Manual Control Operations

#### Individual Axis Control
- **Speed adjustment**: Use horizontal sliders (0-1000 RPM)
- **Torque setting**: Adjust torque percentage
- **Direction control**: Use ← → buttons for movement
- **Position monitoring**: Watch real-time position display

#### Coordinated Movement
- **Multi-axis control**: Move multiple axes simultaneously
- **Speed synchronization**: Enable coordinated movement
- **Emergency stop**: Red STOP button always accessible

### Pattern Execution

#### Pre-programmed Patterns
1. **Circle Pattern**
   - Adjustable radius and speed
   - Perfect circular movements
   - Ideal for testing XY coordination

2. **Square Pattern**
   - Precise 90-degree corners
   - Adjustable size parameters
   - Tests positioning accuracy

3. **Spiral Pattern**
   - Expanding spiral movements
   - Smooth acceleration curves
   - Demonstrates complex coordination

#### Custom Pattern Recording
1. **Start recording**: Tap record button
2. **Perform movements**: Use manual controls
3. **Stop recording**: Save pattern with name
4. **Playback**: Execute recorded sequence

### 3D Signature Replicator

#### Drawing Your Signature
1. **Go to Draw tab**
2. **Draw signature**: Use finger on touch screen
3. **Select style**: Choose from options below
4. **Execute 3D**: Tap "Execute 3D" button

#### Style Options
- **Normal**: Direct 2D to 3D conversion
- **Calligraphy**: Variable Z-height for thickness
- **Embossed**: Raised/lowered sections for depth
- **Animated**: Smooth pen-up/pen-down movements

#### 3D Execution Process
1. **Pen attachment**: Mount pen/marker to Z-axis
2. **Paper positioning**: Place paper in XY plane
3. **Height adjustment**: Set Z-axis for proper contact
4. **Execute**: Watch signature drawn in real-time

---

## ⚙️ Advanced Configuration

### Motor Settings

#### Speed & Acceleration
```cpp
// In Arduino code, modify these values:
stepperX.setMaxSpeed(2000);     // Max speed in steps/sec
stepperX.setAcceleration(1000); // Acceleration in steps/sec²
```

#### Microstepping Configuration
- **Full step**: 200 steps/revolution
- **Half step**: 400 steps/revolution  
- **1/4 step**: 800 steps/revolution
- **1/8 step**: 1600 steps/revolution
- **1/16 step**: 3200 steps/revolution

#### Current Limiting
Adjust driver potentiometer for optimal current:
- **Too low**: Motor skips steps, weak torque
- **Too high**: Motor overheats, driver protection
- **Optimal**: Smooth operation, minimal heat

### Communication Protocols

#### Bluetooth Commands
JSON format for motor control:
```json
{
  "action": "move",
  "axis": "X",
  "steps": 1000,
  "speed": 500
}
```

#### WiFi API Endpoints
HTTP POST to ESP32 IP address:
```
POST /api/move
Content-Type: application/json

{
  "axis": "Y",
  "position": 2500,
  "speed": 800
}
```

### Safety Configuration

#### Emergency Stop Response
- **Immediate halt**: All motors stop instantly
- **Power disable**: Motor drivers disabled
- **Status indication**: Red LED and app notification
- **Manual reset**: Required to resume operation

#### Limit Switch Behavior
- **Soft limits**: Configurable in software
- **Hard limits**: Physical switch activation
- **Homing sequence**: Automatic zero positioning
- **Overtravel protection**: Prevents mechanical damage

---

## 🔍 Troubleshooting

### Connection Issues

#### Bluetooth Problems
**Symptom**: Cannot find device
- **Check**: ESP32 powered on and programmed
- **Verify**: Bluetooth enabled on phone
- **Reset**: Restart both devices
- **Range**: Move closer to controller

**Symptom**: Connection drops frequently
- **Interference**: Move away from WiFi routers
- **Power**: Check ESP32 power supply stability
- **Distance**: Maintain <10m range

#### WiFi Problems
**Symptom**: Cannot connect to WiFi
- **SSID**: Verify "TriAxis_Controller" appears
- **Password**: Use "APEX2024" (case sensitive)
- **IP**: Connect to 192.168.4.1
- **Reset**: Power cycle ESP32

### Motor Issues

#### Motors Not Moving
**Check List**:
- [ ] Power supply connected (12V)
- [ ] Enable pin activated (LOW)
- [ ] Driver connections secure
- [ ] Motor coils connected correctly
- [ ] Emergency stop not activated

#### Erratic Movement
**Possible Causes**:
- **Current too low**: Increase driver current
- **Speed too high**: Reduce maximum speed
- **Acceleration too high**: Reduce acceleration
- **Mechanical binding**: Check for obstructions

#### Overheating
**Solutions**:
- **Reduce current**: Adjust driver potentiometer
- **Add cooling**: Install heatsinks or fans
- **Duty cycle**: Allow rest periods
- **Check wiring**: Verify connections

### App Issues

#### App Crashes
- **Update**: Install latest app version
- **Memory**: Close other apps
- **Restart**: Reboot phone
- **Reinstall**: Delete and reinstall app

#### Slow Response
- **Connection**: Check signal strength
- **Background**: Close unnecessary apps
- **Distance**: Move closer to controller
- **Interference**: Change WiFi channel

---

## 📋 Maintenance

### Regular Maintenance

#### Weekly Checks
- [ ] Visual inspection of all connections
- [ ] Emergency stop function test
- [ ] Limit switch operation verification
- [ ] Motor temperature check
- [ ] App connection test

#### Monthly Maintenance
- [ ] Clean motor and driver heatsinks
- [ ] Tighten mechanical connections
- [ ] Lubricate linear guides (if applicable)
- [ ] Update firmware if available
- [ ] Backup custom patterns

#### Annual Service
- [ ] Replace limit switch batteries (if wireless)
- [ ] Motor bearing inspection
- [ ] Driver calibration verification
- [ ] Complete system performance test
- [ ] Documentation update

### Spare Parts List
- **Fuses**: 5A automotive blade fuses
- **Connectors**: JST-XH connectors
- **Switches**: Micro limit switches
- **Cables**: Shielded motor cables
- **Drivers**: Spare A4988/DRV8825 modules

---

## 📞 Technical Support

### Contact Information
**APEX PRECISION MECHATRONIX PVT. LTD.**
- **Developer**: Amol M.
- **Email**: support@apexprecision.com
- **Phone**: +91-XXXX-XXXXXX
- **Website**: www.apexprecision.com

### Support Resources
- **Online Manual**: Latest version available online
- **Video Tutorials**: Step-by-step setup guides
- **Community Forum**: User discussions and tips
- **Remote Support**: TeamViewer assistance available

### Warranty Information
- **Hardware**: 2 years from purchase date
- **Software**: Lifetime updates included
- **Support**: 1 year free technical support
- **Extended**: Additional support packages available

---

## 📄 Specifications

### System Specifications
| Parameter | Value |
|-----------|-------|
| Axes | 3 (X, Y, Z) |
| Motor Type | NEMA 17 Stepper |
| Max Speed | 2000 steps/sec |
| Resolution | Up to 3200 steps/rev |
| Communication | Bluetooth 5.0 + WiFi |
| Power | 12V/5A external |
| Control | ESP32 microcontroller |

### Performance Specifications
| Parameter | Value |
|-----------|-------|
| Positioning Accuracy | ±0.1mm |
| Repeatability | ±0.05mm |
| Max Travel Speed | 100mm/sec |
| Operating Temperature | 0°C to 50°C |
| Humidity | 10% to 90% RH |
| Noise Level | <60dB |

---

*© 2024 APEX PRECISION MECHATRONIX PVT. LTD. All rights reserved.*  
*Version 1.0 - Initial Release*