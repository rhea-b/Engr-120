import machine
import utime

#connecting to machine
led_onboard = machine.Pin(10, machine.Pin.OUT)
sensor = machine.ADC(28)
conversion_factor = 3.3/(65535)

#turning led on/off based on readings
while True:
    reading = sensor.read_u16()*conversion_factor
    if (reading > 3.0):
        led_onboard.value(1) #led on
    else:
        led_onboard.value(0) #led off