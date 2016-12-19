import serial

CR = b'\r'
HEADER_STR_LEN = 156
TEST_HEADER_LEN=225

class FluoDevice(serial.Serial):

    def initialize(self):
        self.write(CR)
        v = self.read(HEADER_STR_LEN)
        self.test_mode = False
        return v
        
    def enter_test(self):
        self.write(b't')
        self.read(1)
        v=self.read(TEST_HEADER_LEN)
        self.test_mode = True
        return v
    
    def leave_test(self):
        self.write(b'e')
        self.read(1)
        v=self.read(HEADER_STR_LEN)
        self.test_mode = False
        return v
    
    def send_char(self, ch):
        if not self.test_mode:
            self.enter_test()
        
        n=self.write(ch.encode('ascii'))
        self.read(n)
        v=self.read(TEST_HEADER_LEN)
        return v
        
    def send_char_led(self, ch):
        if self.test_mode:
            self.leave_test() # Switch off LED
        self.enter_test()
        
        n=self.write(ch.encode('ascii'))
        self.read(n)
        v=self.read(TEST_HEADER_LEN)
        return v    
        
    
