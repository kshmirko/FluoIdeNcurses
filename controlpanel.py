import npyscreen
import curses
import subprocess

from consts import BIND_DEVICES_FORM
LED_KEYS_TRUE = ['a','s','d','f','g','h','j','k']
LED_KEYS_TEMP = ['1','2','3','4','5','6','7','8']
class ControlPanel(npyscreen.ActionPopup):
    DEFAULT_LINES=17
    SHOW_ATX = 40
    SHOW_ATY = 15
    
    def create(self):
        self.ltr11_run = False
        self.ltr210_run = False
    
        self.keypress_timeout=5
        self.add(npyscreen.TitleFixedText, name='Подкл./Откл. флуориметра', \
            begin_entry_at=30, rely=1,\
            value='^L')
        
        self.add(npyscreen.TitleFixedText, name='Соответствие:', begin_entry_at=30, \
            rely=3, value='1, 2, 3, 4, 5, 6, 7, 8')
            
        self.add(npyscreen.TitleFixedText, name='Управление светодиодами:', begin_entry_at=30, \
            rely=5, value='1, 2, 3, 4, 5, 6, 7, 8')
            
        self.add(npyscreen.TitleFixedText, name='Управление турелью:', begin_entry_at=30, \
            rely=7, value='Z, X, C, V, B, N, M, Q')
            
        self.add(npyscreen.TitleFixedText, name='Синхроимпульс:', begin_entry_at=30, \
            rely=9, value='W')
            
        self.add(npyscreen.TitleFixedText, name='Выход:', begin_entry_at=30, \
            rely=11, value='E')
            
        self.add(npyscreen.TitleFixedText, name='Запуск АЦП:', begin_entry_at=30, \
            rely=13, value='^A-LTR-11, ^S-LTR-210')
            
        self.add_handlers({
            "^L": self.connect_fluo,
            "^D": self.start_ltr_11,
            "^S": self.start_ltr_210,
            "1": self.send_control_chars,
            "2": self.send_control_chars,
            "3": self.send_control_chars,
            "4": self.send_control_chars,
            "5": self.send_control_chars,
            "6": self.send_control_chars,
            "7": self.send_control_chars,
            "8": self.send_control_chars,
            
            "z": self.send_control_chars,
            "x": self.send_control_chars,
            "c": self.send_control_chars,
            "v": self.send_control_chars,
            "b": self.send_control_chars,
            "n": self.send_control_chars,
            "m": self.send_control_chars,
            "q": self.send_control_chars,
            
            "w": self.send_control_chars,
            "e": self.send_control_chars,  
        })
    
    
    def start_ltr_11(self, ch):
        if not self.ltr11_run:
            cfg=self.parentApp.getForm(BIND_DEVICES_FORM)
            if (cfg.ltr11crate.value is None) or (len(cfg.ltr11crate.value)==0):
                cfg.edit()
            ltr11crate = cfg.ltr11crate.value
            self.ltr11_p = subprocess.Popen(['./ltr11-fluo', ltr11crate], \
                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.ltr11_run=True
        
        
    def start_ltr_210(self, ch):
        if not self.ltr210_run:
            cfg=self.parentApp.getForm(BIND_DEVICES_FORM)
            if (cfg.ltr210crate.value is None) or (len(cfg.ltr210crate.value)==0):
                cfg.edit()
            ltr210crate = cfg.ltr210crate.value
            self.ltr210_p = subprocess.Popen(['./ltr210-fluo', ltr210crate], \
                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.ltr210_run=True
    
    
    def connect_fluo(self, *argfs, **kwargs):
        cfg=self.parentApp.getForm(BIND_DEVICES_FORM)
        if (cfg.devfluo.value is None) or (len(cfg.devfluo.value)==0):
            cfg.edit()
        fluoport = cfg.devfluo.value
        
        if not self.parentApp.FluoDev.isOpen():
            self.parentApp.FluoDev.port = fluoport
            self.parentApp.FluoDev.baudrate = 9600
            self.parentApp.FluoDev.open()
            
            if self.parentApp.FluoDev.isOpen():
                v = self.parentApp.FluoDev.initialize()
                npyscreen.notify_confirm(v.decode('utf-8'), \
                    title="Message", form_color='STANDOUT')
        else:
            self.parentApp.FluoDev.close()
    
    
    def send_control_chars(self, ch):
        ch = chr(ch)
        v=b""
        if ch in LED_KEYS_TEMP:
            #Вкл светодиода
            ch = LED_KEYS_TRUE[LED_KEYS_TEMP.index(ch)]
            v=self.parentApp.FluoDev.send_char_led(ch)
        elif ch in ['z','x','c','v','b','n','m','q']:
            #перемещение турели
            v=self.parentApp.FluoDev.send_char(ch)
        elif ch in ['w']:
            #Синхронизация
            v=self.parentApp.FluoDev.send_char(ch)
        elif ch in ['e']:
            #Выход из тестового режима
            v=self.parentApp.FluoDev.leave_test() 
            
        npyscreen.notify_confirm(v.decode('ascii'), \
                    title="Message", form_color='STANDOUT')        
    
                        
    def on_ok(self):
        self.parentApp.FluoDev.leave_test() 
        if self.parentApp.FluoDev.isOpen():
            self.parentApp.FluoDev.close()
        return
        
    def on_cancel(self):
        self.parentApp.FluoDev.leave_test() 
        if self.parentApp.FluoDev.isOpen():
            self.parentApp.FluoDev.close()
        return
        
        
        
    def while_waiting(self):
        # Проверяем, завершились ли процессы с АЦП
        if self.ltr11_run and self.ltr11_p.poll():
            msg=None
            if self.ltr11_p.returncode<0 or self.ltr11_p.returncode!=0:
                msg = self.ltr11_p.stderr.read().decode('utf-8')
            else:
                msg = self.ltr11_p.stdout.read().decode('utf-8')
            npyscreen.notify(msg, \
                    title="Message", form_color='STANDOUT')
            self.ltr11_run=False
            
        if self.ltr210_run and self.ltr210_p.poll():
            msg=None
            if self.ltr210_p.returncode<0 or self.ltr210_p.returncode!=0:
                msg = self.ltr210_p.stderr.read().decode('utf-8')
            else:
                msg = self.ltr210_p.stdout.read().decode('utf-8')
            npyscreen.notify(msg, \
                    title="Message", form_color='STANDOUT')
            self.ltr210_run=False
        pass



