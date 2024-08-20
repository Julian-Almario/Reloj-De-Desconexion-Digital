from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import ds1302
import time
import framebuf

i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=400000)
oled = SSD1306_I2C(128,64,i2c) #Inicio de Display SSD1306

led = machine.Pin(20, machine.Pin.OUT) # led

boton = machine.Pin(22, machine.Pin.IN, machine.Pin.PULL_UP) # Boton

ds = ds1302.DS1302(Pin(5),Pin(18),Pin(19)) # Inicio de RTC DS1302

ldr = machine.ADC(27) # Inicio Fotoresistor

buzzer = machine.Pin(15, Pin.OUT)

#Pintar iconos en pantalla
def Abrir_Icono(ruta_icono):
    doc = open(ruta_icono, "rb")
    doc.readline()
    xy = doc.readline()
    x = int(xy.split()[0])
    y = int(xy.split()[1])
    icono = bytearray(doc.read())
    doc.close()
    return framebuf.FrameBuffer(icono, x, y, framebuf.MONO_HLSB)

def Buenas(time): #Definir estado del dia
    if time >= 1 and time <= 12:
        oled.text("BUENAS DIAS", 0, 0)
    elif time >= 12 and time <= 18:
        oled.text("BUENAS TARDES", 0, 0)
    else:
        oled.text("BUENAS NOCHES", 0, 0)

# Hora y minuto de la alarma
hora_alarma = 10
minuto_alarma = 49

# Funcion de despertador
def Alarma(hora_alarma, minuto_alarma):
    while hora_alarma == ds.hour() and minuto_alarma == ds.minute():
        oled.fill(0)
        oled.text("ALARMAAAA", 0, 0)
        oled.show()
        led.value(1)
        buzzer.value(1)
        time.sleep(2)
        led.value(0)
        buzzer.value(0)

        led.value(1)
        buzzer.value(1)                  
        time.sleep(3)
        led.value(0)
        buzzer.value(0)




# Display Data
while True:
    # Variables del loop
    sensor_luz = ldr.read_u16()
    
    print(boton.value())
    
    # Eventos
    Alarma(hora_alarma, minuto_alarma)
    
    # Display print 
    Buenas(ds.hour()) #Buenas
    
    oled.blit(Abrir_Icono("img/calendario.pbm"), 0, 16)
    oled.text("{}/{}/{}" .format(ds.day(),ds.month(),ds.year()), 17, 20)
    
    oled.blit(Abrir_Icono("img/reloj.pbm"), 0, 34)
    oled.text("{}:{}:{}" .format(ds.hour(), ds.minute(),ds.second()), 17,39)
    
    oled.show()
    oled.fill(0)# Limpio la pantalla para que no se superponga el texto

#ds.year(2024)  # Set the year to 2085
#ds.month(8)    # Set the month to January
#ds.day(14)     # Set the day to 17th
#ds.hour(19)    # Set the hour to midnight (00)
#ds.minute(08)  # Set the minute to 17
#ds.second(20)  # Set the second to 30
