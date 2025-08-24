# TriAxis Pro Mobile App Source Code
# Developer: Amol M.
# Company: APEX PRECISION MECHATRONIX PVT. LTD.
# Version: 1.0

# This is the enhanced mobile app source code
# To compile to APK, use tools like:
# - Kivy + Buildozer
# - BeeWare
# - React Native
# - Flutter

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import json

class ConnectionManager:
    def __init__(self):
        self.connection_type = None
        self.is_connected = False
        self.device_info = {}
        
    def scan_bluetooth_devices(self):
        # Simulate Bluetooth device scanning
        return [
            {"name": "StepperController_BT01", "address": "00:11:22:33:44:55", "signal": -45},
            {"name": "TriAxis_Motor_Hub", "address": "AA:BB:CC:DD:EE:FF", "signal": -62},
            {"name": "Arduino_Stepper", "address": "12:34:56:78:90:AB", "signal": -38}
        ]
    
    def scan_wifi_devices(self):
        # Simulate WiFi device scanning
        return [
            {"name": "StepperController_192.168.1.100", "ip": "192.168.1.100", "signal": -35},
            {"name": "MotorHub_192.168.1.150", "ip": "192.168.1.150", "signal": -50},
            {"name": "TriAxis_192.168.1.200", "ip": "192.168.1.200", "signal": -42}
        ]
    
    def connect_bluetooth(self, device_address):
        # Simulate Bluetooth connection
        time.sleep(2)  # Connection delay
        self.connection_type = "Bluetooth"
        self.is_connected = True
        self.device_info = {"address": device_address, "type": "BT"}
        return True
    
    def connect_wifi(self, device_ip):
        # Simulate WiFi connection
        time.sleep(1.5)  # Connection delay
        self.connection_type = "WiFi"
        self.is_connected = True
        self.device_info = {"ip": device_ip, "type": "WiFi"}
        return True
    
    def disconnect(self):
        self.connection_type = None
        self.is_connected = False
        self.device_info = {}

class EnhancedTriAxisApp:
    def __init__(self, master):
        self.master = master
        master.title("TriAxis Pro - APEX PRECISION MECHATRONIX")
        master.geometry("450x750")
        
        self.connection_manager = ConnectionManager()
        self.motor_positions = {'X': 0, 'Y': 0, 'Z': 0}
        self.motor_speeds = {'X': 50, 'Y': 50, 'Z': 50}
        self.motor_torques = {'X': 50, 'Y': 50, 'Z': 50}
        
        self.create_interface()
    
    def create_interface(self):
        # Header with enhanced status
        header_frame = tk.Frame(self.master, bg='#2c3e50', height=70)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        title_frame = tk.Frame(header_frame, bg='#2c3e50')
        title_frame.pack(side='left', padx=10, pady=5)
        
        tk.Label(title_frame, text="TriAxis Pro", fg='white', bg='#2c3e50', 
                font=('Arial', 16, 'bold')).pack(anchor='w')
        tk.Label(title_frame, text="by Amol M. | APEX PRECISION MECHATRONIX PVT. LTD.", 
                fg='#bdc3c7', bg='#2c3e50', font=('Arial', 8)).pack(anchor='w')
        
        # Connection status with type indicator
        status_frame = tk.Frame(header_frame, bg='#2c3e50')
        status_frame.pack(side='right', padx=10, pady=10)
        
        self.connection_icon = tk.Label(status_frame, text="📶", bg='#2c3e50', font=('Arial', 16))
        self.connection_icon.pack(side='top')
        
        self.connection_label = tk.Label(status_frame, text="Disconnected", fg='#e74c3c', 
                                       bg='#2c3e50', font=('Arial', 8))
        self.connection_label.pack(side='bottom')
        
        # Emergency Stop
        tk.Button(header_frame, text="STOP", bg='#e74c3c', fg='white',
                 font=('Arial', 12, 'bold'), command=self.emergency_stop).pack(side='right', padx=5, pady=15)
        
        # Navigation tabs
        nav_frame = tk.Frame(self.master, bg='#34495e', height=50)
        nav_frame.pack(fill='x')
        nav_frame.pack_propagate(False)
        
        tabs = ['Connect', 'Manual', 'Patterns', 'Draw', 'About']
        for tab in tabs:
            btn = tk.Button(nav_frame, text=tab, bg='#34495e', fg='white',
                          command=lambda t=tab: self.switch_tab(t))
            btn.pack(side='left', fill='x', expand=True, padx=1, pady=5)
        
        # Main content
        self.content_frame = tk.Frame(self.master, bg='white')
        self.content_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.current_tab = 'Connect'
        self.show_connect_tab()
    
    def switch_tab(self, tab_name):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        self.current_tab = tab_name
        
        if tab_name == 'Connect':
            self.show_connect_tab()
        elif tab_name == 'Manual':
            self.show_manual_tab()
        elif tab_name == 'Patterns':
            self.show_patterns_tab()
        elif tab_name == 'Draw':
            self.show_draw_tab()
        elif tab_name == 'About':
            self.show_about_tab()
    
    def show_connect_tab(self):
        tk.Label(self.content_frame, text="Device Connection", font=('Arial', 16, 'bold')).pack(pady=10)
        
        # Connection type selection
        type_frame = tk.LabelFrame(self.content_frame, text="Connection Type", font=('Arial', 12, 'bold'))
        type_frame.pack(fill='x', pady=10)
        
        self.conn_type = tk.StringVar(value="Bluetooth")
        
        bt_frame = tk.Frame(type_frame)
        bt_frame.pack(fill='x', padx=10, pady=5)
        tk.Radiobutton(bt_frame, text="🔵 Bluetooth", variable=self.conn_type, value="Bluetooth",
                      font=('Arial', 12), command=self.on_connection_type_change).pack(side='left')
        tk.Label(bt_frame, text="Range: 10m | Power: Low", font=('Arial', 9), fg='gray').pack(side='right')
        
        wifi_frame = tk.Frame(type_frame)
        wifi_frame.pack(fill='x', padx=10, pady=5)
        tk.Radiobutton(wifi_frame, text="📶 WiFi", variable=self.conn_type, value="WiFi",
                      font=('Arial', 12), command=self.on_connection_type_change).pack(side='left')
        tk.Label(wifi_frame, text="Range: 100m | Power: Medium", font=('Arial', 9), fg='gray').pack(side='right')
        
        # Device list
        self.device_frame = tk.LabelFrame(self.content_frame, text="Available Devices")
        self.device_frame.pack(fill='both', expand=True, pady=10)
        
        # Scan button
        scan_frame = tk.Frame(self.content_frame)
        scan_frame.pack(fill='x', pady=5)
        
        self.scan_btn = tk.Button(scan_frame, text="🔍 Scan for Devices", bg='#3498db', fg='white',
                                 font=('Arial', 12), command=self.scan_devices)
        self.scan_btn.pack(side='left', padx=5)
        
        self.refresh_btn = tk.Button(scan_frame, text="🔄 Refresh", bg='#95a5a6', fg='white',
                                   command=self.scan_devices)
        self.refresh_btn.pack(side='left', padx=5)
        
        # Connection status
        self.status_frame = tk.Frame(self.content_frame, relief='sunken', bd=1)
        self.status_frame.pack(fill='x', pady=10)
        
        self.status_text = tk.Label(self.status_frame, text="Ready to scan for devices", 
                                   font=('Arial', 10), fg='blue')
        self.status_text.pack(pady=10)
        
        # Auto-scan on startup
        self.scan_devices()
    
    def on_connection_type_change(self):
        self.scan_devices()
    
    def scan_devices(self):
        self.scan_btn.config(state='disabled', text='Scanning...')
        self.status_text.config(text="Scanning for devices...", fg='orange')
        
        # Clear previous devices
        for widget in self.device_frame.winfo_children():
            widget.destroy()
        
        def scan_thread():
            time.sleep(1)  # Simulate scan time
            
            if self.conn_type.get() == "Bluetooth":
                devices = self.connection_manager.scan_bluetooth_devices()
                icon = "🔵"
            else:
                devices = self.connection_manager.scan_wifi_devices()
                icon = "📶"
            
            # Update UI in main thread
            self.master.after(0, lambda: self.display_devices(devices, icon))
        
        threading.Thread(target=scan_thread, daemon=True).start()
    
    def display_devices(self, devices, icon):
        self.scan_btn.config(state='normal', text='🔍 Scan for Devices')
        
        if not devices:
            self.status_text.config(text="No devices found", fg='red')
            return
        
        self.status_text.config(text=f"Found {len(devices)} device(s)", fg='green')
        
        for i, device in enumerate(devices):
            device_frame = tk.Frame(self.device_frame, relief='raised', bd=1, bg='#f8f9fa')
            device_frame.pack(fill='x', padx=5, pady=2)
            
            # Device info
            info_frame = tk.Frame(device_frame, bg='#f8f9fa')
            info_frame.pack(side='left', fill='x', expand=True, padx=10, pady=5)
            
            name_label = tk.Label(info_frame, text=f"{icon} {device['name']}", 
                                 font=('Arial', 11, 'bold'), bg='#f8f9fa')
            name_label.pack(anchor='w')
            
            if self.conn_type.get() == "Bluetooth":
                detail_text = f"Address: {device['address']} | Signal: {device['signal']}dBm"
            else:
                detail_text = f"IP: {device['ip']} | Signal: {device['signal']}dBm"
            
            detail_label = tk.Label(info_frame, text=detail_text, font=('Arial', 9), 
                                   fg='gray', bg='#f8f9fa')
            detail_label.pack(anchor='w')
            
            # Signal strength indicator
            signal_strength = abs(device['signal'])
            if signal_strength < 40:
                signal_color = '#27ae60'  # Strong
                signal_text = "●●●"
            elif signal_strength < 55:
                signal_color = '#f39c12'  # Medium
                signal_text = "●●○"
            else:
                signal_color = '#e74c3c'  # Weak
                signal_text = "●○○"
            
            tk.Label(device_frame, text=signal_text, fg=signal_color, 
                    font=('Arial', 12), bg='#f8f9fa').pack(side='right', padx=5)
            
            # Connect button
            connect_btn = tk.Button(device_frame, text="Connect", bg='#27ae60', fg='white',
                                  command=lambda d=device: self.connect_to_device(d))
            connect_btn.pack(side='right', padx=5, pady=5)
    
    def connect_to_device(self, device):
        self.status_text.config(text="Connecting...", fg='orange')
        
        def connect_thread():
            try:
                if self.conn_type.get() == "Bluetooth":
                    success = self.connection_manager.connect_bluetooth(device['address'])
                    device_id = device['address']
                else:
                    success = self.connection_manager.connect_wifi(device['ip'])
                    device_id = device['ip']
                
                if success:
                    self.master.after(0, lambda: self.on_connection_success(device, device_id))
                else:
                    self.master.after(0, lambda: self.on_connection_failed())
                    
            except Exception as e:
                self.master.after(0, lambda: self.on_connection_failed(str(e)))
        
        threading.Thread(target=connect_thread, daemon=True).start()
    
    def on_connection_success(self, device, device_id):
        self.status_text.config(text=f"Connected to {device['name']}", fg='green')
        
        # Update header status
        conn_type = self.connection_manager.connection_type
        if conn_type == "Bluetooth":
            self.connection_icon.config(text="🔵")
            self.connection_label.config(text="Bluetooth", fg='#3498db')
        else:
            self.connection_icon.config(text="📶")
            self.connection_label.config(text="WiFi", fg='#27ae60')
        
        # Show connection details
        details = f"Connected via {conn_type}\nDevice: {device['name']}\nID: {device_id}"
        messagebox.showinfo("Connection Successful", details)
        
        # Enable other tabs
        self.switch_tab('Manual')
    
    def on_connection_failed(self, error="Connection failed"):
        self.status_text.config(text=error, fg='red')
        messagebox.showerror("Connection Failed", f"Could not connect to device.\n{error}")
    
    def show_manual_tab(self):
        if not self.connection_manager.is_connected:
            tk.Label(self.content_frame, text="⚠️ Please connect to a device first", 
                    font=('Arial', 14), fg='red').pack(pady=50)
            tk.Button(self.content_frame, text="Go to Connection", bg='#3498db', fg='white',
                     command=lambda: self.switch_tab('Connect')).pack(pady=10)
            return
        
        # Connection info bar
        conn_info = tk.Frame(self.content_frame, bg='#d5f4e6', relief='raised', bd=1)
        conn_info.pack(fill='x', pady=(0, 10))
        
        conn_text = f"Connected via {self.connection_manager.connection_type}"
        tk.Label(conn_info, text=f"✅ {conn_text}", bg='#d5f4e6', 
                font=('Arial', 10, 'bold')).pack(pady=5)
        
        # Position display
        pos_frame = tk.LabelFrame(self.content_frame, text="Current Position")
        pos_frame.pack(fill='x', pady=5)
        
        self.pos_labels = {}
        for i, axis in enumerate(['X', 'Y', 'Z']):
            tk.Label(pos_frame, text=f"{axis}:").grid(row=0, column=i*2, padx=5, pady=5)
            self.pos_labels[axis] = tk.Label(pos_frame, text="0.00", font=('Arial', 10, 'bold'))
            self.pos_labels[axis].grid(row=0, column=i*2+1, padx=5, pady=5)
        
        # Motor controls
        for axis in ['X', 'Y', 'Z']:
            motor_frame = tk.LabelFrame(self.content_frame, text=f"{axis}-Axis Control")
            motor_frame.pack(fill='x', pady=3)
            
            tk.Label(motor_frame, text="Speed:").grid(row=0, column=0, padx=5, pady=2)
            speed_scale = tk.Scale(motor_frame, from_=0, to=1000, orient='horizontal')
            speed_scale.set(self.motor_speeds[axis])
            speed_scale.grid(row=0, column=1, columnspan=2, sticky='ew', padx=5)
            
            tk.Button(motor_frame, text="←", command=lambda a=axis: self.move_motor(a, -1)).grid(row=1, column=0, padx=2, pady=2)
            tk.Button(motor_frame, text="→", command=lambda a=axis: self.move_motor(a, 1)).grid(row=1, column=2, padx=2, pady=2)
            
            motor_frame.columnconfigure(1, weight=1)
        
        # Disconnect button
        tk.Button(self.content_frame, text="Disconnect", bg='#e74c3c', fg='white',
                 command=self.disconnect_device).pack(pady=10)
    
    def show_patterns_tab(self):
        if not self.connection_manager.is_connected:
            tk.Label(self.content_frame, text="⚠️ Please connect to a device first", 
                    font=('Arial', 14), fg='red').pack(pady=50)
            return
        
        tk.Label(self.content_frame, text="Pattern Library", font=('Arial', 16, 'bold')).pack(pady=10)
        
        patterns = [("Circle", "Perfect circles"), ("Square", "Precise squares"), ("Spiral", "Spiral movements")]
        
        for pattern_name, description in patterns:
            pattern_frame = tk.Frame(self.content_frame, relief='raised', bd=1)
            pattern_frame.pack(fill='x', pady=2)
            
            tk.Label(pattern_frame, text=pattern_name, font=('Arial', 12, 'bold')).pack(anchor='w', padx=10, pady=2)
            tk.Label(pattern_frame, text=description, font=('Arial', 9)).pack(anchor='w', padx=10)
            tk.Button(pattern_frame, text="Execute", bg='#3498db', fg='white').pack(side='right', padx=10, pady=5)
    
    def show_draw_tab(self):
        if not self.connection_manager.is_connected:
            tk.Label(self.content_frame, text="⚠️ Please connect to a device first", 
                    font=('Arial', 14), fg='red').pack(pady=50)
            return
        
        tk.Label(self.content_frame, text="3D Signature Replicator", font=('Arial', 16, 'bold')).pack(pady=10)
        
        self.canvas = tk.Canvas(self.content_frame, width=400, height=200, bg='white', relief='sunken', bd=2)
        self.canvas.pack(pady=10)
        
        control_frame = tk.Frame(self.content_frame)
        control_frame.pack(pady=10)
        
        tk.Button(control_frame, text="Clear", command=self.clear_canvas).pack(side='left', padx=5)
        tk.Button(control_frame, text="Execute 3D", bg='#e67e22', fg='white').pack(side='left', padx=5)
    
    def move_motor(self, axis, direction):
        step_size = 10 * direction
        self.motor_positions[axis] += step_size
        self.pos_labels[axis].config(text=f"{self.motor_positions[axis]:.2f}")
        
        # Send command via current connection
        command = {
            "axis": axis,
            "steps": step_size,
            "speed": self.motor_speeds[axis],
            "connection": self.connection_manager.connection_type
        }
        print(f"Sending command: {json.dumps(command)}")
    
    def disconnect_device(self):
        self.connection_manager.disconnect()
        self.connection_icon.config(text="📶")
        self.connection_label.config(text="Disconnected", fg='#e74c3c')
        messagebox.showinfo("Disconnected", "Device disconnected successfully")
        self.switch_tab('Connect')
    
    def emergency_stop(self):
        if self.connection_manager.is_connected:
            print("EMERGENCY STOP - All motors halted!")
            messagebox.showwarning("Emergency Stop", "All motors have been stopped!")
    
    def clear_canvas(self):
        self.canvas.delete("all")
    
    def show_about_tab(self):
        tk.Label(self.content_frame, text="TriAxis Pro", font=('Arial', 20, 'bold')).pack(pady=10)
        tk.Label(self.content_frame, text="Professional 3-Axis Stepper Motor Controller", 
                font=('Arial', 12)).pack(pady=5)
        
        info_frame = tk.LabelFrame(self.content_frame, text="Developer Information")
        info_frame.pack(fill='x', pady=20, padx=20)
        
        tk.Label(info_frame, text="Developer: Amol M.", font=('Arial', 12, 'bold')).pack(pady=5)
        tk.Label(info_frame, text="Company: APEX PRECISION MECHATRONIX PVT. LTD.", 
                font=('Arial', 12, 'bold')).pack(pady=5)
        tk.Label(info_frame, text="Specializing in Precision Motion Control Solutions", 
                font=('Arial', 10), fg='gray').pack(pady=5)
        
        features_frame = tk.LabelFrame(self.content_frame, text="App Features")
        features_frame.pack(fill='x', pady=10, padx=20)
        
        features = [
            "✓ Bluetooth & WiFi Connectivity",
            "✓ 3-Axis Stepper Motor Control",
            "✓ Real-time Position Monitoring",
            "✓ Pattern Library & Custom Sequences",
            "✓ 3D Signature Replicator",
            "✓ Emergency Safety Controls"
        ]
        
        for feature in features:
            tk.Label(features_frame, text=feature, font=('Arial', 10)).pack(anchor='w', padx=10, pady=2)
        
        tk.Label(self.content_frame, text="Version 1.0 | © 2024 APEX PRECISION MECHATRONIX", 
                font=('Arial', 9), fg='gray').pack(side='bottom', pady=20)

if __name__ == "__main__":
    root = tk.Tk()
    app = EnhancedTriAxisApp(root)
    root.mainloop()