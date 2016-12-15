import curses
import npyscreen
from fluorimetersetupform import FluorimeterSetupForm
from ltr11setupform import Ltr11SetupForm
from ltr210setupform import Ltr210SetupForm
from configdevicespathsform import ConfigDevicesPathsForm

MAIN_FORM = 'MAIN'
BIND_DEVICES_FORM = 'BINDDEV'
CONFIG_FLUO_FORM = 'CONFFLUO'
CONFIG_LTR11_FORM = 'CONFLTR11'
CONFIG_LTR210_FORM = 'CONFLTR210'
TEST_PANEL_FORM = 'TESTPANEL'

class MainApp(npyscreen.NPSAppManaged):
    def onStart(self):
        npyscreen.setTheme(npyscreen.Themes.ElegantTheme)
        self.registerForm(MAIN_FORM, \
            FluoForm())
        
        self.registerForm(BIND_DEVICES_FORM, \
            ConfigDevicesPathsForm())
            
        self.registerForm(CONFIG_FLUO_FORM, \
            FluorimeterSetupForm()) 
            
        self.registerForm(CONFIG_LTR11_FORM, \
            Ltr11SetupForm())       
        
        self.registerForm(CONFIG_LTR210_FORM, \
            Ltr210SetupForm())       

       
class FluoForm(npyscreen.FormWithMenus):

    def __init__(self):
        super(FluoForm, self).__init__(name='Программа управления устройством "Флуориметр"')
        
    def create(self):
        self.file_menu = self.add_menu(name='Файл', shortcut='1')
        self.file_menu.addItemsFromList([
            ('Выход', self.exit_app, '1')
        ])
        
        self.setup_menu = self.add_menu(name='Настройка', shortcut='2')
        self.setup_menu.addItemsFromList([
            ('Связать устройства...', self.whenAssociateDevicesCB, '1'),
            ('Настроить флуориметр...', self.whenFluorimeterSetupCB, '2'),
            ('Настроить LTR-11...', self.whenLTR11SetupCB, '3'),
            ('Настроить LTR-210...', self.whenLTR210SetupCB, '4'),
        ])
        
        self.run_menu = self.add_menu(name='Запуск', shortcut='3')
        self.run_menu.addItemsFromList([
            ('Запуск панели управления...', self.whenLaunchControllPanelCB, '1'),
            
        ])
        
    def exit_app(self):
        self.parentApp.setNextForm(None)
        self.editing = False
        self.parentApp.switchFormNow()
        
    def whenFluorimeterSetupCB(self):
        self.parentApp.getForm(CONFIG_FLUO_FORM).edit()
        pass
    
    def whenLTR11SetupCB(self):
        self.parentApp.getForm(CONFIG_LTR11_FORM).edit()
        pass
        
    def whenLTR210SetupCB(self):
        self.parentApp.getForm(CONFIG_LTR210_FORM).edit()
        pass
    
    def whenAssociateDevicesCB(self):
        self.parentApp.getForm(BIND_DEVICES_FORM).edit()
        pass
        
    def whenLaunchControllPanelCB(self):
        """
        Если активирована тестовая панель, переходим на новый экран
        """
        pass
        
def main():
    App = MainApp()
    App.run()
    
if __name__=='__main__':
    main()
    
