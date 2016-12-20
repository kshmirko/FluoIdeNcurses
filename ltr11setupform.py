import npyscreen
import ListBox as listbox

class NewChannelWidget(npyscreen.ActionPopup):
    DEFAULT_LINES=15
    def __init__(self):
        super(NewChannelWidget, self).__init__(name='Настройка канала')
        
        
    def create(self):
        """
        """
        self.nch = self.add(npyscreen.TitleText, name='Номер физического канала:', \
            begin_entry_at=30, value='0')
        self.chmode = self.add(npyscreen.TitleSelectOne, begin_entry_at=30, \
            name='Режим работы канала:', max_height=4, \
            value=[1,], values=['Дифференциальный','С общей землей','Измерения нуля'], \
            scroll_exit=True)
        self.chrange = self.add(npyscreen.TitleSelectOne, begin_entry_at=30, \
            name='Макс. напряжение на входе:', max_height=5, \
            value=[0,], values=['10 В','2.5 В', '0.624 В', '0.156 В'], \
            scroll_exit=True)
            
    def on_ok(self):
        self.result = "CH[%d] = (mode = %d, range = %d)"%(int(self.nch.value),
            self.chmode.value[0], self.chrange.value[0])
        self.editing=True
        return
    
    def on_cancel(self):
        if hasattr(self, 'result'):
            del self.result
            
            
class Ltr11SetupForm(npyscreen.ActionPopup):
    """
    Настройка параметров работы модуля LTR-11
    Режим запуска преобразования
    Режим старта ввода данных
    Частота сбора данных
    Время измерений
    Количество вводимых блоков
    Описание каналов
    
    """
    DEFAULT_LINES=25
    def __init__(self):
        super(Ltr11SetupForm, self).__init__(name='Настройка АЦП "LTR-11"')
        
    def create(self):
        self.start_adc_mode = self.add(npyscreen.TitleSelectOne, begin_entry_at=30, \
            name='Режим запуска АЦП:', max_height=4, \
            value=[1,], values=['INTERNAL','EXT RISE','EXT FALL'], \
            scroll_exit=True)
            
        self.input_adc_mode = self.add(npyscreen.TitleSelectOne, begin_entry_at=30, \
            name='Режим ввода данных в АЦП:', max_height=4, \
            value=[2,], values=['EXT RISE','EXT FALL','INTERNAL'], \
            scroll_exit=True)
            
        self.frequency = self.add(npyscreen.TitleText, name='Частота сбора данных (Гц):', \
            begin_entry_at=30, \
            value='400000')
            
        self.meas_time = self.add(npyscreen.TitleText, name='Время измерений (мкс):', \
            begin_entry_at=30, \
            value='0')
            
        self.num_blocks = self.add(npyscreen.TitleText, name='Количество блоков данных:', \
            begin_entry_at=30, \
            value='0')
            
        self.channels = self.add(listbox.ListBox, 
            formklass=NewChannelWidget,
            name='Каналы:', \
            begin_entry_at=30, \
            max_height=10,\
            footer="Нажми i/d для добавления/удаления",
            values=None,\
            slow_scroll=True)
            
    def on_ok(self):
        config = []
        config.append('START ADC MODE: %d\n'%self.start_adc_mode.value[0])
        config.append('INPUT MODE: %d\n'%self.input_adc_mode.value[0])
        config.append('ADC MODE: 0\n')
        config.append('FREQUENCY: %d Hz\n'%int(self.frequency.value))
        channels = self.channels.values
        config.append('LOGICAL CHANNELS COUNT: %d\n'%len(channels))
        for i in range(len(channels)):
            config.append('%s\n'%channels[i])
        config.append('MEASUREMENTS TIME (mks): %.2f\n'%float(self.meas_time.value))
        config.append('REQUIRED BLOCKS : %d\n'%int(self.num_blocks.value))
        with open('config.ltr11','wt') as txt:
            txt.writelines(config)
        
            
            
