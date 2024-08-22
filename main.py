from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import ds1302
import time
import framebuf

i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=400000)
oled = SSD1306_I2C(128, 64, i2c)  # Inicio de Display SSD1306

led = Pin(20, Pin.OUT)  # Definición del LED
boton = Pin(22, Pin.IN, Pin.PULL_UP)  # Botón
ds = ds1302.DS1302(Pin(5), Pin(18), Pin(19))  # Inicio de RTC DS1302
ldr = machine.ADC(27)  # Definición del Fotoresistor
buzzer = Pin(15, Pin.OUT)  # Definición del Buzzer

# Hora y minuto de la alarma
hora_alarma = 5
minuto_alarma = 30
segundos_alarma = 0

# Configuración del tiempo del Pomodoro
pomodoro_time = 25 * 60  # 25 minutos en segundos
short_break_time = 5 * 60  # 5 minutos en segundos
long_break_time = 15 * 60  # 15 minutos en segundos
pomodoro_count = 0

# Función para convertir la hora a formato 12 horas con AM/PM
def formato_12_horas(hora, minuto, segundo):
    if hora == 0:
        hora_12 = 12
        periodo = "AM"
    elif 1 <= hora < 12:
        hora_12 = hora
        periodo = "AM"
    elif hora == 12:
        hora_12 = 12
        periodo = "PM"
    else:
        hora_12 = hora - 12
        periodo = "PM"
    return "{:02d}:{:02d}:{:02d} {}".format(hora_12, minuto, segundo, periodo)

# Función para mostrar el tiempo restante en la pantalla
def mostrar_tiempo_restante(tiempo_restante):
    minutos, segundos = divmod(tiempo_restante, 60)
    oled.fill(0)
    oled.text("Tiempo Restante:", 0, 0)
    oled.text("{:02d}:{:02d}".format(minutos, segundos), 32, 20)
    oled.show()

# Función para iniciar el temporizador del Pomodoro
def start_timer(duration):
    start_time = time.time()
    while time.time() - start_time < duration:
        tiempo_restante = int(duration - (time.time() - start_time))
        mostrar_tiempo_restante(tiempo_restante)
        
        led.on()  # LED encendido
        time.sleep(0.5)
        led.off()  # LED apagado
        time.sleep(0.5)
        
        if boton.value() == 0:  # Si el botón es presionado, se reinicia el cronómetro
            return False
    return True

# Ciclo Pomodoro
def pomodoro_cycle():
    global pomodoro_count
    while True:
        oled.fill(0)
        oled.text("Pomodoro: 25 min", 0, 0)
        oled.show()
        if not start_timer(pomodoro_time):
            break

        pomodoro_count += 1

        if pomodoro_count % 4 == 0:
            oled.fill(0)
            oled.text("Descanso largo: 15 min", 0, 0)
            oled.show()
            if not start_timer(long_break_time):
                break
        else:
            oled.fill(0)
            oled.text("Descanso corto: 5 min", 0, 0)
            oled.show()
            if not start_timer(short_break_time):
                break

# Pintar iconos en pantalla
def Abrir_Icono(ruta_icono):
    doc = open(ruta_icono, "rb")
    doc.readline()
    xy = doc.readline()
    x = int(xy.split()[0])
    y = int(xy.split()[1])
    icono = bytearray(doc.read())
    doc.close()
    return framebuf.FrameBuffer(icono, x, y, framebuf.MONO_HLSB)

# Definir estado del día
def Buenas(time):
    if time >= 1 and time <= 12:
        oled.text("BUENOS DIAS", 0, 0)
        oled.contrast(255)
    elif time >= 12 and time <= 18:
        oled.text("BUENAS TARDES", 0, 0)
        oled.contrast(255)
    else:
        oled.text("BUENAS NOCHES", 0, 0)
        oled.contrast(1)
        

# Definir sonido
def Bip():
    oled.fill(0)
    oled.text("ALARMAAAAAA", 64, 32)
    oled.show()
    led.value(1)
    buzzer.value(1)
    time.sleep(1.5)
    led.value(0)
    buzzer.value(0)
    time.sleep(1.5)
    
# Función de despertador
def Alarma(hora_alarma, minuto_alarma, segundos_alarma):
    while boton.value() == 1 and hora_alarma == ds.hour() and minuto_alarma == ds.minute() and segundos_alarma == ds.second():
        for i in range(10):
            Bip()
            if boton.value() == 0:
                break

# Loop principal
while True:

    # Variables del loop
    sensor_luz = ldr.read_u16()

    # Eventos
    Alarma(hora_alarma, minuto_alarma, segundos_alarma)
    
    # Verifica si el botón es presionado para iniciar el Pomodoro
    if boton.value() == 0:
        oled.fill(0)
        oled.text("Iniciando Pomodoro", 0, 0)
        oled.show()
        pomodoro_cycle()
        oled.fill(0)
        oled.text("Pomodoro Finalizado", 0, 0)
        oled.show()

    # Display print 
    Buenas(ds.hour())
    
    oled.blit(Abrir_Icono("img/calendario.pbm"), 0, 16)
    oled.text("{}/{}/{}".format(ds.day(), ds.month(), ds.year()), 17, 20)
    
    oled.blit(Abrir_Icono("img/reloj.pbm"), 0, 34)
    oled.text(formato_12_horas(ds.hour(), ds.minute(), ds.second()), 17, 39)
    
    oled.show()
    oled.fill(0)  # Limpio la pantalla para que no se superponga el texto

# Funciones para definir tiempo del modulo RTC 1306
# ds.year(2024)  # Set the year to 2024
# ds.month(8)    # Set the month to August
# ds.day(14)     # Set the day to 14th
# ds.hour(19)    # Set the hour to 19:00
# ds.minute(08)  # Set the minute to 08
# ds.second(20)  # Set the second to 20
