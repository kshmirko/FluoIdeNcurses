import npyscreen


class ConfigDevicesPathsForm(npyscreen.ActionPopup):
    """
    Настройка подключений к различным устройствам.
    Указываются пути к последовательным портам для подключения флуориметра и 
    спектрометра, а также каналы связи с ацп LTR-11 и LTR-210
    """
    def __init__(self):
        super(ConfigDevicesPathsForm, self).__init__(name='Настройка соединения')
        
    def create(self):
        """
        """
        self.devfluo = self.add(npyscreen.TitleFilename, \
                name=' Устройство "Флуориметр":', begin_entry_at=30)
        self.devspec = self.add(npyscreen.TitleFilename, \
                name='Устройство "Спектрометр":', begin_entry_at=30)
        self.ltr11crate = self.add(npyscreen.TitleText, \
                name='    Канал связи с LTR-11:', begin_entry_at=30)
        self.ltr210crate = self.add(npyscreen.TitleText, \
                name='   Канал связи с LTR-210:', begin_entry_at=30)
    
    def on_ok(self):
        """
        Если ввод корректен, то возврящаемся на главную форму
        """
        #self.parentApp.change_form(MAIN_FORM) 
