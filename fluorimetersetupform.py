import npyscreen 

class FluorimeterSetupForm(npyscreen.ActionPopup):
    """
    Установка параметров работы флуориметра
    Необхоимо выполнять при работе с устройством как с флуориметром
    """
    def __init__(self):
        super(FluorimeterSetupForm, self).__init__(name='Настройка устройства "Флуориметр"')
