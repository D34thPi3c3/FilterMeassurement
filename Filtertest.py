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
if platform.system() != 'Windows':
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
""")
    
#Load all the diffrent screen
Builder.load_file('screenconfig/startscreen.kv')
Builder.load_file('screenconfig/configscreen.kv')
Builder.load_file('screenconfig/summaryscreen.kv')
Builder.load_file('screenconfig/pressuremeasurementscreen.kv')
Builder.load_file('screenconfig/flowmeasurementscreen.kv')
Builder.load_file('screenconfig/endmeasurementscreen.kv')

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
    #This Variable has the info, which Checkbox is checked
    selected_checkbox = None
    
    def checkbox_clicked(self, selectedcheckbox):
        self.selected_checkbox = selectedcheckbox
    
    def textinput_selected(self, selectedti):
        textinputselected = selectedti
        self.add_number(textinputselected)
    
    def add_number(self, number):
        if self.selected_checkbox == 'minfillheight':
            self.min_height.text += number
        elif self.selected_checkbox == 'maxfillheight':
            self.max_height.text += number
        elif self.selected_checkbox == 'minforce':
            self.min_force.text += number
        elif self.selected_checkbox == 'maxforce':
            self.max_force.text += number
        elif self.selected_checkbox == 'minpressuremotor':
            self.min_pressuremotor.text += number 
        elif self.selected_checkbox == 'maxpressuremotor':
            self.max_pressuremotor.text += number
        elif self.selected_checkbox == 'minflow':
            self.min_flow.text += number
        elif self.selected_checkbox == 'maxflow':
            self.max_flow.text += number
        elif self.selected_checkbox == 'minpressureloss':
            self.min_pressureloss.text += number
        elif self.selected_checkbox == 'maxpressureloss':
            self.max_pressureloss.text += number     
            
    def delete_number(self):
        if self.selected_checkbox == 'minfillheight':
            self.min_height.text = self.min_height.text[:-1]
        elif self.selected_checkbox == 'maxfillheight':
            self.max_height.text = self.max_height.text[:-1]
        elif self.selected_checkbox == 'minforce':
            self.min_force.text = self.min_force.text[:-1]
        elif self.selected_checkbox == 'maxforce':
            self.max_force.text = self.max_force.text[:-1]
        elif self.selected_checkbox == 'minpressuremotor':
            self.min_pressuremotor.text = self.min_pressuremotor.text[:-1] 
        elif self.selected_checkbox == 'maxpressuremotor':
            self.max_pressuremotor.text = self.max_pressuremotor.text[:-1]
        elif self.selected_checkbox == 'minflow':
            self.min_flow.text = self.min_flow.text[:-1]
        elif self.selected_checkbox == 'maxflow':
            self.max_flow.text = self.max_flow.text[:-1]
        elif self.selected_checkbox == 'minpressureloss':
            self.min_pressureloss.text = self.min_pressureloss.text[:-1]
        elif self.selected_checkbox == 'maxpressureloss':
            self.max_pressureloss.text = self.max_pressureloss.text[:-1]



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






    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
