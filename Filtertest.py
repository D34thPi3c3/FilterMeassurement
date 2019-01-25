# coding: utf8

"""
Create:       08.01.2018
@Autor:       Rafael Eberle
Company:      TBSafety AG
Edit by:  
Edit Date:
"""
#Import Backend Stuff because otherwise it doesnt work on Raspberry
import os
os.environ['KIVY_GL_BACKEND'] = 'gl'

#Import Stuff for Kivy (GUI_TOOL)
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.config import Config
from kivy.core.window import Window

#Import other Important stuff:
#platform: Check if Linux or Windows (because I Programmed on Windows)
#smbus: For I2C
#time: For time things as delay
import platform
if platform.system() == 'Linux':
    import smbus
    bus = smbus.SMBus(1)       
import time

#I2C adressen Definieren
PRESSURE_MEAS_ADDRESS = 0x10
FLOW_MEAS_ADRESS = 0x11

#If you're screen has a bigger Resolution than 800x480
#use this raspysetup
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '480')
Config.write()

#On a Rasperry Py, use this setup
#Window.fullscreen = True

# You can create your kv code in the Python file
Builder.load_string("""
<CustButton@Button>:
    font_size: 20
                        

<StartScreen>:
    BoxLayout:
        padding: 10
        spacing: 10
        orientation: 'horizontal'
        CustButton:
            text: 'Start Messung'
            on_press: 
                root.manager.transition.direction = 'left'
                root.manager.transition.duration = 0.25
                root.manager.current = 'filterpressuremeasurement'
                
        CustButton:
            text: 'Gemessene Filter'
            on_press:
                root.manager.transition.direction = 'left'
                root.manager.transition.duration = 0.25
                root.manager.current = 'filtersummary'

<SummaryScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: 10
        spacing: 10
        Label:
            text: 'Hier sollten alle gemessenen Filter Aufgelistet sein'
            
        CustButton:
            text: 'Zurück'
            size_hint: 1, 0.15
            on_press:
                root.manager.transition.direction = 'right'
                root.manager.transition.duration = 0.25
                root.manager.current = 'startscreen'
                
<PressureMeasurementScreen>:
    id: press_measurement
    status: status_press_meas
    BoxLayout:
        orientation: 'vertical'
        padding: 10
        spacing: 10
        BoxLayout:
            orientation: 'horizontal'
            spacing: 15
            size_hint: 1, 0.15
            CustButton:
                text: 'Start Druckmessung'
                on_press: press_measurement.start_meassurement()
            Label:
                id: status_press_meas
                size_hint: 0.5, 1
                font_size: 20
                text: 'Status: 0%'
            Image:
                id: image_press_meas
                size_hint: 0.3, 1
                source: 'picture/white.jpg'
            
        Label:
            spacing: 10
            id: label_press_meas
            font_size: 20
            text_size: 700, None
            text: 'Die Messung wurde noch nicht gestartet. Um die Messung zu Starten muss der Knopf Start Druckmessung gedrückt werden. Es kann erst zur nächsten Messung gewechselt werden, sobald die Messung grün ist!'
        
        BoxLayout:
            orientation: 'horizontal'
            spacing: 10
            size_hint: 1, 0.15
            CustButton:
                text: 'Messung Abbrechen'
                on_press:
                    root.manager.transition.direction = 'right'
                    root.manager.transition.duration = 0.25
                    root.manager.current = 'startscreen'
            
            CustButton:
                text: 'Nächste Messung'
                on_press:
                    press_measurement.next_page()

<FlowMeasurementScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: 10
        spacing: 10
        Label:
            text: 'Hier sollte der Durchflussmessung durchgeführt werden'
        
        BoxLayout:
            orientation: 'horizontal'
            spacing: 10
            size_hint: 1, 0.15
            CustButton:
                text: 'Messung Abbrechen'
                on_press:
                    root.manager.transition.direction = 'right'
                    root.manager.transition.duration = 0.25
                    root.manager.current = 'startscreen'
            
            CustButton:
                text: 'Messung Beenden'
                on_press:
                    root.manager.transition.direction = 'left'
                    root.manager.transition.duration = 0.25
                    root.manager.current = 'endmeasurement'
                

<EndMeasurementScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: 10
        spacing: 10
        Label:
            text: 'Hier sollten die gesamten Daten und der QRCode angezeigt werden'
        
        BoxLayout:
            orientation: 'horizontal'
            spacing: 10
            size_hint: 1, 0.15
            CustButton:
                text: 'QR Code Drucken'
            
            CustButton:
                text: 'Messung Speichern und Beenden'
                on_press:
                    root.manager.transition.direction = 'right'
                    root.manager.transition.duration = 0.25
                    root.manager.current = 'startscreen'
            
            CustButton:
                text: 'Messung löschen'
                on_press:
                    root.manager.transition.direction = 'right'
                    root.manager.transition.duration = 0.25
                    root.manager.current = 'startscreen'
""")

# Create a class for all screens in which you can include
# helpful methods specific to that screen    
class StartScreen(Screen):
    pass

class SummaryScreen(Screen):
    pass

class PressureMeasurementScreen(Screen):
    startmeassurement = False
    def start_meassurement(self):
        if platform.system() == 'nux':
            bus.write_byte()
        else:    
            self.status.text = "Status: 100%"
            self.startmeassurement = True
    
    def next_page(self):
        if self.startmeassurement:
            self.manager.transition.direction = 'left'
            self.manager.transition.duration = 0.25
            self.manager.current = 'flowmeasurement'
            

class FlowMeasurementScreen(Screen):
    pass

class EndMeasurementScreen(Screen):
    pass



# The ScreenManager controls moving between screens
screen_manager = ScreenManager()

# Add the screens to the manager and then supply a name
# that is used to switch screens
screen_manager.add_widget(StartScreen(name="startscreen"))
screen_manager.add_widget(SummaryScreen(name="filtersummary"))
screen_manager.add_widget(PressureMeasurementScreen(
        name="filterpressuremeasurement"))
screen_manager.add_widget(FlowMeasurementScreen(name="flowmeasurement"))
screen_manager.add_widget(EndMeasurementScreen(name="endmeasurement"))

#Build the whole App with all the logical Part
class FilterTestApp(App):
    
    def build(self):
        return screen_manager
    
sample_app = FilterTestApp()
sample_app.run()






    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
