from machine import I2C
from machine import Pin
from machine import sleep
import libacc
i2c = I2C(scl=Pin(22), sda=Pin(21))     #initializing the I2C method for ESP32
mpu= libacc.accel(i2c)
p = Pin(2, Pin.OUT)
while True:
 values = mpu.get_values()
 if (abs(values["AcY"]) >= 5000):
     p.on()
 else:
     p.off()
 if (abs(values["GyY"]) >= 20000):
     for _ in range(5):
         p.off()
         print("HELLO MOTO!")
         sleep(50)
         p.on()
         sleep(50)
 print(values)
 
 sleep(500)
