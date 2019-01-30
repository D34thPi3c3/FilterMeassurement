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
import platform
if platform.system() == 'Linux':
    os.environ['KIVY_GL_BACKEN'] = 'gl'
else:
    os.environ['KIVY_GL_BACKEND'] = 'sdl2'

#Import Stuff for Kivy (GUI_TOOL)
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.config import Config
from kivy.properties import ObjectProperty
#from kivy.core.window import Window

#Import other Important stuff:
#platform: Check if Linux or Windows (because I Programmed on Windows)
#smbus: For I2C
#time: For time things as delay
if platform.system() == 'Linux':
    import smbus
    bus = smbus.SMBus(1)       
import time

#I2C adressen Definieren
PRESSURE_MEAS_ADDRESS = 0x10
FLOW_MEAS_ADRESS = 0x11
START_MEAS = 0x0A
STOP_MEAS = 0x14
STATUS_MEAS = 0x1E

#If you're screen has a bigger Resolution than 800x480
#use this raspysetup
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '480')
Config.write()

#Some Global Variable
textinputselected = 'min_height'

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
            
        BoxLayout:
            orientation: 'vertical'
            CustButton:   
                text: 'Gemessene Filter'
                on_press:
                    root.manager.transition.direction = 'left'
                    root.manager.transition.duration = 0.25
                    root.manager.current = 'filtersummary'
            CustButton:
                text: 'Config ändern'
                on_press:
                    root.manager.transition.direction = 'left'
                    root.manager.transition.duration = 0.25
                    root.manager.current = 'config'
<ConfigScreen>:
    id: configscreen
    min_height: min_height
    max_height: max_height
    FloatLayout:
        ## Füll Höhe Einbabe
        Label:
            text: 'Füll Höhe:'
            size_hint: 0.18, 0.1
            pos: 0, 432
            halign: 'right'
        Label:
            text: 'min'
            size_hint: 0.075, 0.1 
            pos: 130, 432 
        TextInput:
            id: min_height
            text: '000'
            size_hint: 0.1, 0.06
            pos: 190, 440
            multiline: False
            on_text_validate: configscreen.textinput_selected('min_height')
        Label:
            text: 'max'
            size_hint: 0.075, 0.1
            pos: 290, 432
        TextInput:
            id: max_height
            text: '004'
            size_hint: 0.1, 0.06
            pos: 350, 440
            multiline: False
            on_text_validate: configscreen.textinput_selected('max_height')
        CheckBox:
            size_hint: 0.05, 0.07
            value: root.min_fillHeight
            pos: 260, 440
            group: 'select_input'
        CheckBox:
            size_hint: 0.05, 0.07
            value: root.max_fillHeight
            pos: 420, 440
            group: 'select_input'
            
        ## Kraft eingabe
        Label:
            text: 'Kraft [N]:'
            size_hint: 0.18, 0.1
            pos: 0, 384
            halign: 'right'
        Label:
            text: 'min'
            size_hint: 0.075, 0.1 
            pos: 130, 384
        TextInput:
            text: '000'
            size_hint: 0.1, 0.06
            pos: 190, 392
            valign: 'middle'
        Label:
            text: 'max'
            size_hint: 0.075, 0.1
            pos: 290, 384
        TextInput:
            text: '004'
            size_hint: 0.1, 0.06
            pos: 350, 392
        CheckBox:
            size_hint: 0.05, 0.07
            pos: 260, 392
            value: root.min_force
            group: 'select_input'
        CheckBox:
            size_hint: 0.05, 0.07
            pos: 420, 392
            value: root.max_force
            group: 'select_input'
        
        ## Unterdruck Motor eingabe
        Label:
            text: 'Udruck Motor [mbar]:'
            size_hint: 0.18, 0.1
            pos: 0, 336
            halign: 'right'
        Label:
            text: 'min'
            size_hint: 0.075, 0.1 
            pos: 130, 336
        TextInput:
            text: '000'
            size_hint: 0.1, 0.06
            pos: 190, 344
            valign: 'middle'
        Label:
            text: 'max'
            size_hint: 0.075, 0.1
            pos: 290, 336
        TextInput:
            text: '004'
            size_hint: 0.1, 0.06
            pos: 350, 344
        CheckBox:
            size_hint: 0.05, 0.07
            pos: 260, 344
            value: root.min_pressureMotor
            group: 'select_input'
        CheckBox:
            size_hint: 0.05, 0.07
            pos: 420, 344
            value: root.max_pressureMotor
            group: 'select_input'
        
        ## Durchfluss eingabe
        Label:
            text: 'Durchfluss [l/min]:'
            size_hint: 0.18, 0.1
            pos: 0, 288
            halign: 'right'
        Label:
            text: 'min'
            size_hint: 0.075, 0.1 
            pos: 130, 288
        TextInput:
            text: '000'
            size_hint: 0.1, 0.06
            pos: 190, 296
            valign: 'middle'
        Label:
            text: 'max'
            size_hint: 0.075, 0.1
            pos: 290, 288
        TextInput:
            text: '004'
            size_hint: 0.1, 0.06
            pos: 350, 296
        CheckBox:
            size_hint: 0.05, 0.07
            pos: 260, 296
            value: root.min_flow
            group: 'select_input'
        CheckBox:
            size_hint: 0.05, 0.07
            pos: 420, 296
            value: root.max_flow
            group: 'select_input'
        
        ## Druckverlust eingabe
        Label:
            text: 'Druckverlust [mbar]:'
            size_hint: 0.18, 0.1
            pos: 0, 240
            halign: 'right'
        Label:
            text: 'min'
            size_hint: 0.075, 0.1 
            pos: 130, 240
        TextInput:
            text: '000'
            size_hint: 0.1, 0.06
            pos: 190, 248
            valign: 'middle'
        Label:
            text: 'max'
            size_hint: 0.075, 0.1
            pos: 290, 240
        TextInput:
            text: '004'
            size_hint: 0.1, 0.06
            pos: 350, 248
        CheckBox:
            size_hint: 0.05, 0.07
            pos: 260, 248
            value: root.min_pressureloss
            group: 'select_input'
        CheckBox:
            size_hint: 0.05, 0.07
            pos: 420, 248
            value: root.max_pressureloss
            group: 'select_input'
            
        ## Eingabe Feld
        CustButton:
            text: '1'
            size_hint: 0.1125, 0.1875
            pos: 465, 360
            on_press: configscreen.add_number('1')
        CustButton:
            text: '2'
            size_hint: 0.1125, 0.1875
            pos: 560, 360
            on_press: configscreen.add_number('2')
        CustButton:
            text: '3'
            size_hint: 0.1125, 0.1875
            pos: 655, 360
            on_press: configscreen.add_number('3')
        CustButton:
            text: '4'
            size_hint: 0.1125, 0.1875
            pos: 465, 265
            on_press: configscreen.add_number('4')
        CustButton:
            text: '5'
            size_hint: 0.1125, 0.1875
            pos: 560, 265
            on_press: configscreen.add_number('5')
        CustButton:
            text: '6'
            size_hint: 0.1125, 0.1875
            pos: 655, 265
            on_press: configscreen.add_number('6')
        CustButton:
            text: '7'
            size_hint: 0.1125, 0.1875
            pos: 465, 170
            on_press: configscreen.add_number('7')
        CustButton:
            text: '8'
            size_hint: 0.1125, 0.1875
            pos: 560, 170
            on_press: configscreen.add_number('8')
        CustButton:
            text: '9'
            size_hint: 0.1125, 0.1875
            pos: 655, 170
            on_press: configscreen.add_number('9')
        CustButton:
            text: ','
            size_hint: 0.1125, 0.1875
            pos: 465, 75
            on_press: configscreen.add_number(',')
        CustButton:
            text: '0'
            size_hint: 0.1125, 0.1875
            pos: 560, 75
            on_press: configscreen.add_number('0')
        CustButton:
            text: 'DEL'
            size_hint: 0.1125, 0.1875
            pos: 655, 75
            on_press: configscreen.delete_number()
            
        CustButton:
            text: 'Zurück und nicht speichern'
            size_hint: 0.5, 0.1
            pos: 0, 0
            on_press:
                root.manager.transition.direction = 'right'
                root.manager.transition.duration = 0.25
                root.manager.current = 'startscreen'
        CustButton: 
            text: 'Zurück und speichern'
            size_hint: 0.5, 0.1
            pos: 400, 0
            on_press:
                root.manager.transition.direction = 'right'
                root.manager.transition.duration = 0.25
                root.manager.current = 'startscreen'
                
        
                

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

class ConfigScreen(Screen):
    
    #This is for the Radio Buttons, that has to be selected
    min_fillHeight = ObjectProperty(False) 
    max_fillHeight = ObjectProperty(True)
    min_force = ObjectProperty(False)
    max_force = ObjectProperty(False)
    min_pressureMotor = ObjectProperty(False)
    max_pressureMotor = ObjectProperty(False)
    min_flow = ObjectProperty(False)
    max_flow = ObjectProperty(False)
    min_pressureloss = ObjectProperty(False)
    max_pressureloss = ObjectProperty(False)
    
    def textinput_selected(self, selectedti):
        textinputselected = selectedti
        self.add_number(textinputselected)
    
    def add_number(self, number):
        if self.min_fillHeight == True:
            self.min_height.text += number
        elif self.max_fillHeight == True:
            self.max_height.text += number
    
    def delete_number(self):
        self.min_height.text = self.min_height.text[:-1]
        



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
screen_manager.add_widget(ConfigScreen(name='config'))

#Build the whole App with all the logical Part
class FilterTestApp(App):
    
    def build(self):
        return screen_manager
    
sample_app = FilterTestApp()
sample_app.run()






    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
