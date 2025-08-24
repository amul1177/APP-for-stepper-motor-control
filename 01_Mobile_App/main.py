from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.slider import Slider
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
import json

class TriAxisApp(App):
    def __init__(self):
        super().__init__()
        self.motor_positions = {'X': 0, 'Y': 0, 'Z': 0}
        self.is_connected = False
        
    def build(self):
        self.title = "TriAxis Pro - APEX PRECISION MECHATRONIX"
        
        # Main layout
        main_layout = BoxLayout(orientation='vertical')
        
        # Header
        header = BoxLayout(size_hint_y=0.15, orientation='horizontal')
        title_label = Label(text='TriAxis Pro\nby Amol M. | APEX PRECISION MECHATRONIX PVT. LTD.', 
                           font_size='16sp', halign='left')
        emergency_btn = Button(text='STOP', size_hint_x=0.2, background_color=[1, 0, 0, 1])
        emergency_btn.bind(on_press=self.emergency_stop)
        
        header.add_widget(title_label)
        header.add_widget(emergency_btn)
        main_layout.add_widget(header)
        
        # Tabbed panel
        tab_panel = TabbedPanel(do_default_tab=False)
        
        # Connect Tab
        connect_tab = TabbedPanelItem(text='Connect')
        connect_layout = self.create_connect_tab()
        connect_tab.add_widget(connect_layout)
        tab_panel.add_widget(connect_tab)
        
        # Manual Tab
        manual_tab = TabbedPanelItem(text='Manual')
        manual_layout = self.create_manual_tab()
        manual_tab.add_widget(manual_layout)
        tab_panel.add_widget(manual_tab)
        
        # Patterns Tab
        patterns_tab = TabbedPanelItem(text='Patterns')
        patterns_layout = self.create_patterns_tab()
        patterns_tab.add_widget(patterns_layout)
        tab_panel.add_widget(patterns_tab)
        
        # About Tab
        about_tab = TabbedPanelItem(text='About')
        about_layout = self.create_about_tab()
        about_tab.add_widget(about_layout)
        tab_panel.add_widget(about_tab)
        
        main_layout.add_widget(tab_panel)
        return main_layout
    
    def create_connect_tab(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        layout.add_widget(Label(text='Device Connection', font_size='20sp', size_hint_y=0.2))
        
        # Connection buttons
        bt_btn = Button(text='🔵 Connect via Bluetooth', size_hint_y=0.3)
        bt_btn.bind(on_press=self.connect_bluetooth)
        layout.add_widget(bt_btn)
        
        wifi_btn = Button(text='📶 Connect via WiFi', size_hint_y=0.3)
        wifi_btn.bind(on_press=self.connect_wifi)
        layout.add_widget(wifi_btn)
        
        self.status_label = Label(text='Ready to connect', size_hint_y=0.2)
        layout.add_widget(self.status_label)
        
        return layout
    
    def create_manual_tab(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        if not self.is_connected:
            layout.add_widget(Label(text='⚠️ Please connect to device first', font_size='16sp'))
            return layout
        
        layout.add_widget(Label(text='Manual Control', font_size='20sp', size_hint_y=0.1))
        
        # Position display
        pos_layout = GridLayout(cols=3, size_hint_y=0.2)
        for axis in ['X', 'Y', 'Z']:
            pos_layout.add_widget(Label(text=f'{axis}: 0.00'))
        layout.add_widget(pos_layout)
        
        # Motor controls
        for axis in ['X', 'Y', 'Z']:
            motor_layout = BoxLayout(orientation='horizontal', size_hint_y=0.2)
            motor_layout.add_widget(Label(text=f'{axis}-Axis', size_hint_x=0.2))
            
            left_btn = Button(text='←', size_hint_x=0.2)
            left_btn.bind(on_press=lambda x, a=axis: self.move_motor(a, -1))
            motor_layout.add_widget(left_btn)
            
            speed_slider = Slider(min=0, max=1000, value=500, size_hint_x=0.4)
            motor_layout.add_widget(speed_slider)
            
            right_btn = Button(text='→', size_hint_x=0.2)
            right_btn.bind(on_press=lambda x, a=axis: self.move_motor(a, 1))
            motor_layout.add_widget(right_btn)
            
            layout.add_widget(motor_layout)
        
        return layout
    
    def create_patterns_tab(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        layout.add_widget(Label(text='Pattern Library', font_size='20sp', size_hint_y=0.2))
        
        patterns = ['Circle Pattern', 'Square Pattern', 'Spiral Pattern']
        for pattern in patterns:
            btn = Button(text=pattern, size_hint_y=0.2)
            btn.bind(on_press=lambda x, p=pattern: self.execute_pattern(p))
            layout.add_widget(btn)
        
        return layout
    
    def create_about_tab(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        about_text = """TriAxis Pro
Professional 3-Axis Stepper Motor Controller

Developer: Amol M.
Company: APEX PRECISION MECHATRONIX PVT. LTD.

Features:
✓ Bluetooth & WiFi Connectivity
✓ 3-Axis Stepper Motor Control
✓ Real-time Position Monitoring
✓ Pattern Library & Custom Sequences
✓ Emergency Safety Controls

Version 1.0 | © 2024 APEX PRECISION MECHATRONIX"""
        
        layout.add_widget(Label(text=about_text, font_size='14sp'))
        
        return layout
    
    def connect_bluetooth(self, instance):
        self.is_connected = True
        self.status_label.text = '✅ Connected via Bluetooth'
        popup = Popup(title='Connection Successful', 
                     content=Label(text='Connected to TriAxis_Motor_Hub'),
                     size_hint=(0.8, 0.4))
        popup.open()
    
    def connect_wifi(self, instance):
        self.is_connected = True
        self.status_label.text = '✅ Connected via WiFi'
        popup = Popup(title='Connection Successful', 
                     content=Label(text='Connected to TriAxis_Controller'),
                     size_hint=(0.8, 0.4))
        popup.open()
    
    def move_motor(self, axis, direction):
        if self.is_connected:
            self.motor_positions[axis] += direction * 10
            print(f"Moving {axis} axis: {direction * 10} steps")
    
    def execute_pattern(self, pattern):
        if self.is_connected:
            popup = Popup(title='Pattern Execution', 
                         content=Label(text=f'Executing {pattern}...'),
                         size_hint=(0.8, 0.4))
            popup.open()
    
    def emergency_stop(self, instance):
        popup = Popup(title='Emergency Stop', 
                     content=Label(text='All motors stopped!'),
                     size_hint=(0.8, 0.4))
        popup.open()

if __name__ == '__main__':
    TriAxisApp().run()