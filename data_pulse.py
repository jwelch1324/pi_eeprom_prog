import RPi.GPIO as GPIO
import time

#Define the pins

D0 = 4
D1 = 17
D2 = 27
D3 = 22
D4 = 10
D5 = 9
D6 = 11
D7 = 0

ADDR_DATA = 14
ADDR_CLK = 15
DATA_DATA = 18
DATA_ENABLE = 23
DATA_PUSH = 24
DATA_CLK = 25
EEPROM_CE = 8
EEPROM_OE = 7
EEPROM_WE = 1

#GPIO.cleanup()
GPIO.setmode(GPIO.BCM)

#Setup the data pins
GPIO.setup(D0,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(D1,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(D2,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(D3,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(D4,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(D5,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(D6,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(D7,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#Setup the register pins
GPIO.setup(ADDR_DATA,GPIO.OUT)
GPIO.setup(ADDR_CLK,GPIO.OUT)
GPIO.setup(DATA_DATA,GPIO.OUT)
GPIO.setup(DATA_ENABLE,GPIO.OUT)
GPIO.setup(DATA_CLK,GPIO.OUT)
GPIO.setup(DATA_PUSH,GPIO.OUT)

#Setup the EEPROM Pins
GPIO.setup(EEPROM_CE, GPIO.OUT)
GPIO.setup(EEPROM_OE, GPIO.OUT)
GPIO.setup(EEPROM_WE, GPIO.OUT)

#Turn off the EEPROM chip initially
GPIO.output(EEPROM_CE, GPIO.HIGH)
GPIO.output(EEPROM_OE, GPIO.HIGH)
GPIO.output(EEPROM_WE, GPIO.HIGH)

#Enable the data register
GPIO.output(DATA_ENABLE,GPIO.LOW)

def pulse_pin(pin):
   GPIO.output(pin, GPIO.HIGH)
   GPIO.output(pin, GPIO.LOW)

def inv_pulse_pin(pin):
   GPIO.output(pin, GPIO.LOW)
   GPIO.output(pin, GPIO.HIGH)

def pulse_data_clk():
   pulse_pin(DATA_CLK)

def pulse_addr_clk():
   pulse_pin(ADDR_CLK)

def push_data():
   pulse_pin(DATA_PUSH)

def set_register(ser_pin, clk_pin, bits, data):
   for i in range(bits):
      GPIO.output(ser_pin, GPIO.HIGH if (data & 1) else GPIO.LOW)
      pulse_pin(clk_pin)
      data = data >> 1

def set_data(data):
   set_register(DATA_DATA, DATA_CLK, 8, data)

def set_addr(addr):
   set_register(ADDR_DATA, ADDR_CLK, 13, addr)

def disable_eeprom():
   GPIO.output(EEPROM_CE,GPIO.HIGH)

def enable_eeprom():
   GPIO.output(EEPROM_CE, GPIO.LOW)

def disable_data_register():
   GPIO.output(DATA_ENABLE, GPIO.HIGH)

def enable_data_register():
   GPIO.output(DATA_ENABLE, GPIO.LOW)

def enable_eeprom_read():
   GPIO.output(EEPROM_OE, GPIO.LOW)

def disable_eeprom_read():
   GPIO.output(EEPROM_OE,GPIO.HIGH)

def read_eeprom():
   disable_data_register()
   time.sleep(1)
   enable_eeprom()
   enable_eeprom_read()
   read_data()
   disable_eeprom_read()

def write_eeprom(addr, data):
   disable_eeprom_read()
   enable_data_register()
   enable_eeprom()
   set_addr(addr)
   set_data(data)
   push_data()
   GPIO.output(EEPROM_WE,GPIO.LOW)
   time.sleep(0.000001)
   GPIO.output(EEPROM_WE,GPIO.HIGH)

def read_data():
   #We need to disable the data register output so it doesn't cause contention with the eeprom output
   #GPIO.output(DATA_ENABLE,GPIO.HIGH)
   def read_pin(pin):
      return GPIO.input(pin)

   d0 = read_pin(D0)
   d1 = read_pin(D1)
   d2 = read_pin(D2)
   d3 = read_pin(D3)
   d4 = read_pin(D4)
   d5 = read_pin(D5)
   d6 = read_pin(D6)
   d7 = read_pin(D7)

   print(f"b{d0}{d1}{d2}{d3}{d4}{d5}{d6}{d7}\t {hex(int(''.join(map(str,[d0,d1,d2,d3,d4,d5,d6,d7])),2))}")
#for i in range(4):
#   GPIO.output(23,GPIO.LOW)
   #time.sleep(1)
#   pulse_clk()
#   time.sleep(1)
#   push()
#   GPIO.output(23,GPIO.HIGH)
#   pulse_clk()
#   push()

set_addr(0x0)
read_eeprom()
time.sleep(2)
write_eeprom(0x0,0xFA)
set_addr(0xFF)
read_eeprom()
set_addr(0x0)
read_eeprom()
time.sleep(2)
disable_eeprom()


while True:
   enable_data_register()
   set_data(0x55)
   push_data()
   read_data()
#   disable_data_register()
   read_data()
   time.sleep(0.1)
   enable_data_register()
   set_data(0xaa)
   push_data()
   read_data()
   time.sleep(0.1)

#GPIO.cleanup()
