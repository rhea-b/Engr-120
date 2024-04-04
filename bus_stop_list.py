# This is a sample code that demonstrates wireless communication.
# You are expected to use this code and modify it to suit your project needs.

# ------------------------------------------------------------------------
# In this project, a red LED is connected to GP14.
# The red LED is controlled based on the value of a light sensor's output.
# The light sensor output is connected to GP26 (ADC pin).
# The red LED status and the value of the red LED pin (GP14) are communicated wirelessly to a server.
# The status and value are displayed on the webpage. In addition, the user interface has
# a circle indicating the LED turns color depending upon the status of the physical LED. 
# ------------------------------------------------------------------------


# -----------------------------------------------------------------------
# The following list of libraries are required. Do not remove any. 
import machine
import network
import usocket as socket
import utime as time
import _thread
import json
# -------------------------------------------------------------------------

# -------------------------------------------------------------------------

# The below portion of the code is to be tweaked based on your needs. 


# Initialize onboard LED pin as output
LED_IR = machine.Pin(14, machine.Pin.OUT)

# Initialize IR emitter pin as output
emitter_IR = machine.Pin(15, machine.Pin.OUT)

# Initialize IR sensor pin as analog input
sensor_IR = machine.ADC(26)

#light sensor initialization

LED_light = machine.Pin(10, machine.Pin.OUT)
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

# Define a function to get the red LED status
def get_LED_light_status():
    return "On" if LED_light.value() == 1 else "Off"

def get_LED_IR_status():
    return "On" if LED_IR.value() == 1 else "Off"
# Note that the function returns the status.

# Define a function to periodically check the ADC pin and control the red LED pin.
def check_adc_and_control_LED_light():
    global LED_light_status  # Declare LED_light_status as global.
    adc_light = machine.ADC(28) # Configure GP26 as ADC pin.
    
    global LED_IR_status
    adc_IR = machine.ADC(26)
    
    

    while True:
        LightSensor_value = adc_light.read_u16()*conversion_factor # read the value of the ADC pin and save it in a variable.
        print("ADC Value:", LightSensor_value)

        
    
        if (LightSensor_value < 0.7):
            print("Mobile light off; turning on the red LED")
            LED_light.value(1)
        else:
            print("Mobile light on; turning off the red LED")
            LED_light.value(0) # set the GP14 pin to low (value = 0).

        LED_light_status = get_LED_light_status()  # Update LED_light_status
        print("Red LED Status:", LED_light_status)
        time.sleep(1) # wait for 1 second.
        
        ########Start of IR code
        
        IR_Sensor_value = adc_IR.read_u16() # read the value of the ADC pin and save it in a variable.
        print("ADC Value:", IR_Sensor_value)
        # Sleep/wait for time specified
        time.sleep(1)
        # Turn on IR emitter
        emitter_IR.value(1)
        # Check if the analog reading exce eds the specified threshold value 
        # Note that this threshold value may need to be changed depending on the environment the sensor is in
        if(sensor_IR.read_u16()>338):
            print("IR light off; turning on the IR LED")
            LED_IR.value(1) # If threshold is exceeded, turn LED on (this means the sensor is blocked)
        else:
            print("IR light on; turning off the IR LED")
            LED_IR.value(0) # If threshold is not exceeded, turn off LED

        LED_IR_status = get_LED_IR_status()  # Update LED_light_status
        print("IR LED Status:", LED_IR_status)
        time.sleep(1) # wait for 1 second.
    
    
# --------------------------------------------------------------------------

# --------------------------------------------------------------------------
# Below given code should not be modified (except for the name of ssid and password). 
# Create a network connection
ssid = 'RPI_PICO_AP'       #Set access point name 
password = '12345678'      #Set your access point password
ap = network.WLAN(network.AP_IF)
ap.config(essid=ssid, password=password)
ap.active(True)            #activating

while ap.active() == False:
  pass
print('Connection is successful')
print(ap.ifconfig())

# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# Below given code defines the web page response. Your html code must be used in this section.
# 
# Define HTTP response
#def web_page():
    #LED_light_status = get_LED_light_status()
    #station1buzzer = "red" if LED_light_status == "On" else "grey"
    #station2buzzer = "green" if LED_light_status == "Off" else "blue"
def web_page():
    LED_IR_status = get_LED_IR_status()
    station1buzzer = "red" if LED_IR_status == "On" else "grey"
    station2buzzer = "green" if LED_IR_status == "Off" else "blue"
    
# Modify the html portion appropriately.
# Style section below can be changed.
# In the Script section some changes would be needed (mostly updating variable names and adding lines for extra elements). 

    html = """<html>
    <head>
        <link rel="icon" type="image/x-icon" href="assets/favicon.ico" />
        <!-- website little icon on the tab-->
        <link href="https://upload.wikimedia.org/wikipedia/commons/a/ae/Bus_icon_white_and_blue_background.svg" rel="shortcut icon" />
        <link href="CSS.css" rel="stylesheet" />
        <style>
            /*navigation bar css*/
            #navbar {
              overflow: hidden;
              background-color: #D46E68;
            }
            
            #navbar a {
              float: left;
              display: block;
              color: #f2f2f2;
              text-align: center;
              padding: 14px 16px;
              text-decoration: none;
              font-size: 17px;
            }
            
            #navbar a:hover {
              background-color: #EFA9A5;
              color: black;
            }
            
            #navbar a.active {
              background-color: #d44038;
              color: white;
            }
            
            .content {
              padding: 16px;
            }
            
            .sticky {
              position: fixed;
              top: 0;
              width: 100%;
            }
            
            .sticky + .content {
              padding-top: 60px;
            }
            /*css for texts*/
            .heading2{
                position: absolute; left: 250px; top: 130px;font-family: 'Courier New', Courier, monospace;
                font-size: 300%;
                font-weight: bolder;
                color:#d44038;
                text-align: center;
                padding: auto;
            }
            .heading3{
                position: absolute; left: 260px; top: 230px; 
                font-family: 'Trebuchet MS';
                color: #0e4e2f;

            }
            .heading4{
                position: absolute; left: 250px; top: 510px;font-family: 'Courier New', Courier, monospace;
                font-size: 300%;
                font-weight: bolder;
                color:#d44038;
                text-align: center;
                padding: auto;
            }
            .heading5{
                position: absolute; left: 260px; top: 610px;font-family: 'Courier New', Courier, monospace;
                font-family: 'Trebuchet MS';
                color: #0e4e2f;
            }

            .circle1 {
            width: 40px;
            height: 40px;
            border-radius: 50%;
            display: inline-block;
            margin-left: 50px;
            margin-top: 6%;
          }
          .circle2 {
            width: 40px;
            height: 40px;
            border-radius: 50%;
            display: inline-block;
            margin-left: 50px;
            margin-top: 12%;
          }
            </style>
    </head>
    <body class="background">
    <!--navigation bar-->
    <div id="navbar">
        <a class="active" href="index.html">Home</a>
        <a href="busstoplist.html">Bus Stop list</a></a>
        <a href="aboutus.html">About Us</a>
    </div>
    <!--bus stop 1-->
    <div>
        <a href="station1.html">
          <div class="circle1" id="station1buzzer" style="background-color: greenyellow;padding:5%;"></div>
        </a>
        <h2 class="heading2">
            Station 1
        </h2>
        <h3 class="heading3">
            Whatisthis Rd
        </h3>
    </div>
    <!--bus stop 2-->
    <div>
        <a href="station2.html">
          <div class="circle2" id="station2buzzer" style="background-color: red;padding:5%;"></div>
        </a>
        <h2 class="heading4">
            Station 2
        </h2>
        <h3 class="heading5">
            Whatisthis Rd
        </h3>
    </div>
    </body>
     <script>
        function updateStatus() {
            var xhr = new XMLHttpRequest();
            xhr.onreadystatechange = function() {
                if (xhr.readyState == 4 && xhr.status == 200) {
                    var data = JSON.parse(xhr.responseText);
                   
                    document.getElementById("LED_IR_status").innerHTML = data.LED_IR_status;
                    var buzzerColor = data.LED_IR_status === "On" ? "red" : "gray";l 
                    document.getElementById("buzzerIndicator").style.backgroundColor = buzzerColor;
                    var station2buzzer = data.LED_IR_status === "Off" ? "green" : "black";
                    document.getElementById("station2buzzer").style.backgroundColor = station2buzzer;
                    var peepeepoopoo = data.LED_IR_status === "Off" ? "green" : "red";
                    document.getElementById("textonoff").style.color= peepeepoopoo;
                }
            };
            xhr.open("GET", "/status", true);
            xhr.send();
        }
        setInterval(updateStatus, 1000); // Refresh every 1 second
    </script>
    </head>
    <body>
     
    
    <div class="circle1" id="station1buzzer" style="background-color: """ + station1buzzer + """;"></div></p>
    <div class="circle2" id="station2buzzer" style="background-color: """ + station2buzzer + """;"></div></p>    
  
    </body>
</html>"""
    return html
# --------------------------------------------------------------------
# This section could be tweaked to return status of multiple sensors or actuators.

# Define a function to get the status of the red LED.
# The function retuns status. 
def get_status():
    status = {
        "LED_IR_status": LED_IR_status,
        "LED_light_status": LED_light_status,
        # You will add lines of code if status of more sensors is needed.
    }
    return json.dumps(status)
# ------------------------------------------------------------------------

# -------------------------------------------------------------------------
# This portion of the code remains as it is.

# Start the ADC monitoring function in a separate thread
_thread.start_new_thread(check_adc_and_control_LED_light, ())

# Create a socket server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

# --------------------------------------------------------------------------

# --------------------------------------------------------------------------

# This section of the code will have minimum changes. 
while True:
    conn, addr = s.accept()
    print('Got a connection from %s' % str(addr))
    request = conn.recv(1024)
    if request:
        request = str(request)
        print('Content = %s' % request)

# this part of the code remains as it is. 
    if request.find("/status") == 6:
        response = get_status()
        conn.send("HTTP/1.1 200 OK\n")
        conn.send("Content-Type: application/html\n")
        conn.send("Connection: close\n\n")
        conn.sendall(response)
    else:
        response = web_page()
        conn.send("HTTP/1.1 200 OK\n")
        conn.send("Content-Type: text/html\n")
        conn.send("Connection: close\n\n")
        conn.sendall(response)
    conn.close()






