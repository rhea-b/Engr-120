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

# Configure GP14 as output and define it as redLED_pin 
redLED_pin = machine.Pin(10, machine.Pin.OUT)
redLED_status = "Off" # Define a variable called redLED_status and set it to "Off"
conversion_factor = 3.3/(65535)

# Define a function to get the red LED status
def get_redLED_status():
    return "On" if redLED_pin.value() == 1 else "Off"
# Note that the function returns the status.

# Define a function to periodically check the ADC pin and control the red LED pin.
def check_adc_and_control_redLED():
    global redLED_status  # Declare redLED_status as global. 
    adc = machine.ADC(28) # Configure GP26 as ADC pin.
    while True:
        LightSensor_value = adc.read_u16()*conversion_factor # read the value of the ADC pin and save it in a variable.
        print("ADC Value:", LightSensor_value)

        
    
        if (LightSensor_value < 3):
            print("Mobile light off; turning on the red LED")
            redLED_pin.value(1)
        else:
            
            print("Mobile light on; turning off the red LED")
            redLED_pin.value(0) # set the GP14 pin to low (value = 0).

        redLED_status = get_redLED_status()  # Update redLED_status
        print("Red LED Status:", redLED_status)
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
def main_page():
    redLED_status = get_redLED_status()
    LED_color = "red" if redLED_status == "On" else "greenyellow"
    
# Modify the html portion appropriately.
# Style section below can be changed.
# In the Script section some changes would be needed (mostly updating variable names and adding lines for extra elements). 

    html = """<html>
    <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no" />
        <meta name="description" content="" />
        <meta name="author" content="Adeline Theodora, Emily Simons-Lane, and Rhea Bona" />
        <title>Bus Stop</title>
        <!-- i do not know what this does but slay-->
        <link rel="icon" type="image/x-icon" href="assets/favicon.ico" />
        <!-- website little icon on the tab-->
        <link href="https://upload.wikimedia.org/wikipedia/commons/a/ae/Bus_icon_white_and_blue_background.svg" rel="shortcut icon" />
        <!-- link to css-->
        <link href="CSS.css" rel="stylesheet" />
        <style>
          /*css for navigation bar*/
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

            /*css for maps and pins*/
            .img-map{
                float:center;
                position:relative;
            }
            .img-pinsstation1{
                position: absolute;
                top:7%;
                right:15%;
            }
            .img-pinsstation2{
                position: absolute;
                top:48%;
                right:38%;
            }
            .circle1 {
            width: 50px;
            height: 50px;
            border-radius: 50%;
            display: inline-block;
            margin-left: 10px;
        }
            .circle2 {
            width: 50px;
            height: 50px;
            border-radius: 50%;
            display: inline-block;
            margin-left: 10px;
        }
        </style>
        <script>
        function updateStatus() {
            var xhr = new XMLHttpRequest();
            xhr.onreadystatechange = function() {
                if (xhr.readyState == 4 && xhr.status == 200) {
                    var data = JSON.parse(xhr.responseText);
                   
                    document.getElementById("RedLEDStatus").innerHTML = data.RedLEDStatus;
                    var buzzerColor = data.RedLEDStatus === "On" ? "red" : "gray";
                    document.getElementById("buzzerIndicator").style.backgroundColor = buzzerColor;
                    var greenLED = data.RedLEDStatus === "Off" ? "green" : "black";
                    document.getElementById("greenLED").style.backgroundColor = greenLED;
                    var peepeepoopoo = data.RedLEDStatus === "Off" ? "green" : "red";
                    document.getElementById("textonoff").style.color= peepeepoopoo;

                    document.getElementById("station1map").style.backgroundColor = station1map;
                    var station1map = data.LED_IR_status === "On" ? "red" : "greenyellow";
                    document.getElementById("station2map").style.backgroundColor = station2map;
                    var station2map = data.LED_IR_status === "On" ? "greenyellow" : "red";
                }
            };
            xhr.open("GET", "/status", true);
            xhr.send();
        }
        setInterval(updateStatus, 1000); // Refresh every 1 second
        </script>
    </head>
    <body class="background">
        <!--navigation bar-->
        <div id="navbar">
            <a class="active" href="index.html">Home</a>
            <a href="busstoplist.html">Bus Stop list</a></a>
            <a href="aboutus.html">About Us</a>
        </div>
        <!--header-->
        <h1 class="heading-word">Victoria Bus</h1>
        <!--map component-->
        <div class="img-map" >
        <img src="victoria-downtown.gif" alt ="victoria map" class="map-padding">
        <!--pin for station 1-->
        <div class="img-pinsstation1 image-pins">
            <a href="station1.html">
                <div class="circle1" id="station1map" style="background-color:"""+ LED_color +""";padding:5%;"></div>
            </a>
        </div>
        <!--pin for station 2-->
        <div class="img-pinsstation2">
            <a href="station2.html">
                <div class="circle2" id="station2map" style="background-color: """+ LED_color +""";padding:5%;"></div>
            </a>
        </div>
        </div>
        </body>
        </html>"""
    return html

def busstoplist():
    redLED_status = get_redLED_status()
    LED_color = "red" if redLED_status == "On" else "green"
    html = """
    
    """
    return html

def get_station1():
    redLED_status = get_redLED_status()
    LED_color = "red" if redLED_status == "On" else "green"
    html = """
    """
    return html

def busstoplist():
    redLED_status = get_redLED_status()
    LED_color = "red" if redLED_status == "On" else "green"
    html = """"""
    return html
# --------------------------------------------------------------------
# This section could be tweaked to return status of multiple sensors or actuators.

# Define a function to get the status of the red LED.
# The function retuns status. 
def get_status():
    status = {
        "RedLEDStatus": redLED_status,
        # You will add lines of code if status of more sensors is needed.
    }
    return json.dumps(status)
# ------------------------------------------------------------------------

# -------------------------------------------------------------------------
# This portion of the code remains as it is.

# Start the ADC monitoring function in a separate thread
_thread.start_new_thread(check_adc_and_control_redLED, ())

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
        conn.send("Content-Type: application/json\n")
        conn.send("Connection: close\n\n")
        conn.sendall(response)
    #main webpage
    elif:
        response = main_page()
        conn.send("HTTP/1.1 200 OK\n")
        conn.send("Content-Type: text/html\n")
        conn.send("Connection: close\n\n")
        conn.sendall(response)
     #bus stop list
    elif request.find("/busstoplist.html")==6:
        response = busstoplist()
        conn.send("HTTP/1.1 200 OK\n")
        conn.send("Content-Type: text/html\n")
        conn.send("Connection: close\n\n")
        conn.sendall(response)
    elif request.find("/station1.html")==6:
        response = get_station1()
        conn.send("HTTP/1.1 200 OK\n")
        conn.send("Content-Type: text/html\n")
        conn.send("Connection: close\n\n")
        conn.sendall(response)
    elif request.find("/station2.html")==6:
        response = get_station2()
        conn.send("HTTP/1.1 200 OK\n")
        conn.send("Content-Type: text/html\n")
        conn.send("Connection: close\n\n")
        conn.sendall(response)
    conn.close()
   




