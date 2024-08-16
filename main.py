from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import ds1302
import time
import dht
import framebuf

#Inicio de Display SSD1306
i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=400000)
oled = SSD1306_I2C(128,64,i2c)

#Inicio de RTC DS1302
ds = ds1302.DS1302(Pin(5),Pin(18),Pin(19))  # (clk, dio, cs)

#Inicio DHT11
d = dht.DHT11(machine.Pin(4))

#Inicio FOtoresistor
ldr = machine.ADC(27)


#Display Date
while True:
    d.measure() # Leer datos de DHT11 (todavia no probado)
    oled.text("BUENAS NOCHES :)", 0, 0)
    oled.text("{}/{}/{}" .format(ds.day(),ds.month(),ds.year()), 0, 17)
    oled.text("{}:{}:{}" .format(ds.hour(), ds.minute(),ds.second()), 0,27)
    oled.text("{}" .format(ldr.read_u16()), 0,34)
    oled.text("{}" .format(d.temperature(), d.humidity()), 0, 41)
    #oled.text("{}:{}" .format(dht.humidity(), dht.temperature()), 0, 34)
    time.sleep(1)
    oled.show() #Renderizo texto en pantalla
    oled.fill(0) #Limpio la pantalla para que no se superponga el texto


# Set the date and time on the RTC
#ds.year(2024)  # Set the year to 2085
#ds.month(6)    # Set the month to January
#ds.day(14)     # Set the day to 17th
#ds.hour(19)    # Set the hour to midnight (00)
#ds.minute(08)  # Set the minute to 17
#ds.second(20)  # Set the second to 30