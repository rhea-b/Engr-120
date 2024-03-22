import machine
import utime

#connecting the leds to GPIO pins
# LED 1 as heater
led_onboard1 = machine.Pin(12, machine.Pin.OUT)
#LED 2 as fan
led_onboard2 = machine.Pin(13, machine.Pin.OUT)

#connecting temperature sensor to an ADC pin
temperature_sensor = machine.ADC(27)

conversion_factor = 3.3/65535

#voltage divider
Vin = 3.3
Ro = 10000

#loop to determine which components is turning on
while True:
    Vout = temperature_sensor.read_u16()*conversion_factor
    Rt = (Vout * Ro)/(Vin - Vout)
    if (Rt > 10000): #10k Rt should be equal to around 25 degrees celcius
        led_onboard1.value(1)
        led_onboard2.value(0)
    else:
        led_onboard1.value(0)
        led_onboard2.value(1)