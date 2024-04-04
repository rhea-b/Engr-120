# Import neccecary modules
import machine
import utime
import math
# Initialize onboard LED pin as output
led_IR = machine.Pin(14, machine.Pin.OUT)

# Initialize IR emitter pin as output
emitter_IR = machine.Pin(15, machine.Pin.OUT)

# Initialize IR sensor pin as analog input
sensor_IR = machine.ADC(26)

#light sensor initialization

led_Light = machine.Pin(10, machine.Pin.OUT)
sensor = machine.ADC(28)
conversion_factor = 3.3/(65535)

#Temp Sensor Initialization

#connecting the leds to GPIO pins
# LED 1 as heater
led_Temp1 = machine.Pin(12, machine.Pin.OUT)
#LED 2 as fan
led_Temp2 = machine.Pin(13, machine.Pin.OUT)

#connecting temperature sensor to an ADC pin
temperature_sensor = machine.ADC(27)

conversion_factor = 3.3/65535

#voltage divider
Vin = 3.3
Ro = 10000

# Define constants
Vin = 3.3  # Supply voltage
Ro = 10000  # Thermistor resistance at room temperature
conversion_factor = 3.3 / 65535  # Conversion factor for ADC reading to voltage

# Function to calculate temperature
def get_temperature():
    Vout = temperature_sensor.read_u16() * conversion_factor
    Rt = Ro * (Vin / Vout - 1)
    temp = 1 / (((math.log(Rt / Ro)) / 3950) + (1 / (273.15 + 25)))
    return temp - 307.06 # Return temperature in Celsius

# Main loop
while True:
    
    # beginning of IR sensor code in loop
    # Read analog value from sensor then print it 
    print(sensor_IR.read_u16())
    
    # Sleep/wait for time specified
    utime.sleep(0.5)
    
    # Turn on IR emitter
    emitter_IR.value(1)
    
    # Check if the analog reading exce eds the specified threshold value 
    # Note that this threshold value may need to be changed depending on the environment the sensor is in
    if(sensor_IR.read_u16()>336):
        
       
        led_IR.value(1) # If threshold is exceeded, turn LED on (this means the sensor is blocked)
    else:
        led_IR.value(0) # If threshold is not exceeded, turn off LED
        
  
 # Beginning of light sensor code in loop
 
    reading = sensor.read_u16()*conversion_factor
    
    if (reading < 3):
        led_Light.value(1) #led on
    else:
        led_Light.value(0) #led off
        
  # Beginning of Temp sensor code in loop

    temp = get_temperature()
    
    

    
    if (temp < 27): #10k Rt should be equal to around 25 degrees celcius, if less heater should turn on and fan turn off
       #lower on circut
        led_Temp1.value(1) #heater on
        led_Temp2.value(0) #fan off
        
    elif (temp > 30):
        led_Temp1.value(0) #heater on
        led_Temp2.value(1) #fan off
        
    else:
        led_Temp1.value(0) #heater on
        led_Temp2.value(0) #fan off

# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# Below given code defines the web page response. Your html code must be used in this section.
# 
# Define HTTP response
def main_page():

def busstoplist():

def get_status():

        
    

