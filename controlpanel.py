import npyscreen


class MyMultiLineAction(npyscreen.MultiLineAction):
    def actionHighlighted(self, act_on_this, key):
        super(MyMultiLineAction, self).h_select(key)
        if key==10:
            pass
        pass
        
class MyTitleMultiLine(npyscreen.TitleMultiLine):
    _entry_type=MyMultiLineAction
    

#class MyTitleSelectOne(MyTitleMultiLine):
#    _entry_type=npyscreen.SelectOne
    
    
#class MySelectOne(npyscreen.SelectOne):
    
#    def h_select(self, ch):
#        super(MyTitleSelectOne,self).h_select(ch)
        #self.on_activate(ch)
        
    #def on_activate(self, ch):
    #    npyscreen.notify("wewe", title="Message", form_color='STANDOUT', wrap=True, wide=False)
    #    pass
        
#class MyTitleSelectOne(npyscreen.TitleMultiLine):
    
#    _entry_type = npyscreen.SelectOne
    
#    def actionHighlighted(self, act_on_this, ch):
#        pass


class ControlPanel(npyscreen.ActionPopup):
    DEFAULT_LINES=30
    SHOW_ATX = 30
    SHOW_ATY = 5
    def __init__(self):
        super(ControlPanel, self).__init__(name='Панель управления')
    
    def create(self):
        self.btnConnect = self.add(npyscreen.Button, name='Подключитсья')
        self.leds = self.add(MyTitleMultiLine, begin_entry_at=30,\
            name='Светодиод:', max_height=10, values=['Выкл.', '№1', '№2', \
                        '№3', '№4', '№5', '№6','№7','№8'],
            value=[0,])
        self.turret = self.add(MyTitleMultiLine, begin_entry_at=30,\
            name='Турель:', max_height=4, values=['№1', '№2', \
                        '№3'],value_changed_callback=on_changed,
            value=[0,])
        pass
    
    
        
    def on_ok(self):
        pass
        
    def on_cancel(self):
        pass

def on_changed(widget):
    npyscreen.notify("wewe", title="Message", form_color='STANDOUT', wrap=True, wide=False)
