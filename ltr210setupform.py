import npyscreen


class Ltr210SetupForm(npyscreen.ActionPopup):
    DEFAULT_LINES=29
    DEFAULT_COLUMNS=95
    def __init__(self):
        super(Ltr210SetupForm, self).__init__(name='Настройка АЦП "LTR-210"')

    def create(self):
       self.sync_mode = self.add(npyscreen.TitleSelectOne, begin_entry_at=30, \
            name='Режим синхронизации АЦП:', max_height=9, \
            value=[5,], values=['INTERNAL','CH1_RISE','CH1_FALL',\
            'CH2_RISE','CH2_FALL','SYNC_IN_RISE','SYNC_IN_FALL',\
            'PERIODIC', 'CONTINUOUS'], \
            scroll_exit=True, rely=2)
       self.hist_time = self.add(npyscreen.TitleText, name='Предыстория (мкс):', \
            begin_entry_at=30, \
            value='0')
       self.meas_time = self.add(npyscreen.TitleText, name='Время измерений (мкс):', \
            begin_entry_at=30, \
            value='0')
       self.frequency = self.add(npyscreen.TitleText, name='Частота сбора данных (Гц):', \
            begin_entry_at=30, \
            value='10000000')
       self.num_blocks = self.add(npyscreen.TitleText, name='Количество блоков данных:', \
            begin_entry_at=30, \
            value='1')
       self.frame_freq = self.add(npyscreen.TitleText, name='Частота сбора кадров (Гц):', \
            begin_entry_at=30, \
            value='5')
       self.meas_zero = self.add(npyscreen.CheckBox, begin_entry_at=30, \
            name='Измерение смещения нуля:', max_height=1, \
            value=[0,], scroll_exit=True)
       self.ch1_en = self.add(npyscreen.FormControlCheckbox, begin_entry_at=30, \
            name = 'Канал 1', values=['Включен'], rely=17, max_width=20)
       self.ch1_range = self.add(npyscreen.TitleSelectOne, begin_entry_at=30, \
            name='Макс. напряжение на входе:', max_height=5, \
            value=[0,], values=['10 В','5 В','2 В',\
            '1 В','0.5 В'], max_width=45, scroll_exit=True)
       self.ch1_mode = self.add(npyscreen.TitleSelectOne, begin_entry_at=30, \
            name='Режим работы канала:', max_height=3, \
            value=[0,], values=['ACDC','AC','ZERO'], max_width=45,\
            scroll_exit=True)
       self.ch1_en.addVisibleWhenSelected(self.ch1_range)
       self.ch1_en.addVisibleWhenSelected(self.ch1_mode)
       
       self.ch2_en = self.add(npyscreen.FormControlCheckbox, begin_entry_at=30, \
            name = 'Канал 2', values=['Включен'], rely=17, max_width=20, relx=46)
       self.ch2_range = self.add(npyscreen.TitleSelectOne, begin_entry_at=30, \
            name='Макс. напряжение на входе:', max_height=5, \
            value=[0,], values=['10 В','5 В','2 В',\
            '1 В','0.5 В'], scroll_exit=True, max_width=45,
            relx=46)
       self.ch2_mode = self.add(npyscreen.TitleSelectOne, begin_entry_at=30, \
            name='Режим работы канала:', max_height=3, max_width=45,\
            value=[0,], values=['ACDC','AC','ZERO'], relx=46, scroll_exit=True)
       self.ch2_en.addVisibleWhenSelected(self.ch2_range)
       self.ch2_en.addVisibleWhenSelected(self.ch2_mode)
       
    def on_ok(self):
        config = []
        config.append("SYNC MODE: %d\n"%(self.sync_mode.value[0]))
        config.append("FLAGS: 3\n")
        config.append("HISTORY TIME (mks): %d\n"%(int(self.hist_time.value)))
        config.append("MEASUREMENTS TIME (mks): %d\n"%(int(self.meas_time.value)))
        config.append("FREQUENCY: %d Hz\n"%(int(self.frequency.value)))
        config.append("MEAS ZERO OFFSET: %d\n"%(self.meas_zero.value[0]))
        config.append("REQUIRED BLOCKS: %d\n"%(int(self.num_blocks.value)))
        config.append("CH[0].Enabled: %d\n"%int(self.ch1_en.value))
        config.append("CH[0].Range: %d\n"%(self.ch1_range.value[0]))
        config.append("CH[0].Mode: %d\n"%(self.ch1_mode.value[0]))
        config.append("CH[1].Enabled: %d\n"%int(self.ch2_en.value))
        config.append("CH[1].Range: %d\n"%(self.ch2_range.value[0]))
        config.append("CH[1].Mode: %d\n"%(self.ch2_mode.value[0]))
        config.append("FRAME FREQ: %d Hz\n"%(int(self.frame_freq.value)))
        with open('ltr210.config','wt') as txt:
            txt.writelines(config)
        return
       
       
