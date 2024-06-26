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
    led_IR_status = get_led_IR_status()
    LED_color = "red" if led_IR_status == "On" else "greenyellow"
    
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
    led_IR_status = get_led_IR_status()
    LED_color = "red" if led_IR_status == "On" else "greenyellow"
    
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
            <script>
        function updateStatus() {
            var xhr = new XMLHttpRequest();
            xhr.onreadystatechange = function() {
                if (xhr.readyState == 4 && xhr.status == 200) {
                    var data = JSON.parse(xhr.responseText);

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
    <!--bus stop 1-->
    <div>
        <a href="station1.html">
          <div class="circle1" id="station1buzzer" style="background-color: """+ LED_color +""";padding:5%;"></div>
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
          <div class="circle2" id="station2buzzer" style="background-color: """+ LED_color +""";padding:5%;"></div>
        </a>
        <h2 class="heading4">
            Station 2
        </h2>
        <h3 class="heading5">
            Whatisthis Rd
        </h3>
    </div>
    </body>
</html>
    
    """
    return html

def get_station1():
    led_Light_status = get_led_Light_status()
    led_Temp1_status = get_led_Temp1_status()
    led_Temp2_status = get_led_Temp2_status()
    led_Light_color = "red" if led_Light_status == "Off" else "green"
    led_Temp1_color = "red" if led_Temp1_status == "Off" else "green"
    led_Temp2_color = "red" if led_Temp2_status == "Off" else "green"

    html = """<html>
<head>
    <title>Station 1</title>
        <!-- i do not know what this does but slay-->
        <link rel="icon" type="image/x-icon" href="assets/favicon.ico" />
        <!-- website little icon on the tab-->
        <link href="https://upload.wikimedia.org/wikipedia/commons/a/ae/Bus_icon_white_and_blue_background.svg" rel="shortcut icon" />
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
        /*css for website texts*/
        body {background-color: #fdf2e3;}
        h1 {
            color: #0e4e2f;
            font-family: 'Courier New', Courier, monospace;
            font-weight: bolder;
            font-size: 600%;
            text-align: center;
        }
        p {
            color: #0e4e2f;
            font-family: 'Trebuchet MS';
            font-size: 150%;
            position: absolute;
            left: 400px;
            top: 250px;
        }
        h2 {
            color: #0e4e2f;
            font-family: 'Trebuchet MS';
            font-size: 150%;
        }
        h3 {
            color: #0e4e2f;
            font-family: 'Trebuchet MS';
            font-size: 200%;
        }
    </style>
    <script>
        function updateStatus() {
            var xhr = new XMLHttpRequest();
            xhr.onreadystatechange = function() {
                if (xhr.readyState == 4 && xhr.status == 200) {
                    var data = JSON.parse(xhr.responseText);
                   
                    document.getElementById("led_Light_status").innerHTML = data.led_Light_status;
                    document.getElementById("led_Temp1_status").innerHTML = data.led_Temp1_status;
                    document.getElementById("led_Temp2_status").innerHTML = data.led_Temp2_status;

                    var s1light = data.RedLEDStatus === "On" ? "greenyellow" : "red";
                    document.getElementById("s1light").style.color= s1light;

                    var s1fan = data.RedLEDStatus === "On" ? "greenyellow" : "red";
                    document.getElementById("s1fan").style.color= s1fan;

                    var s1heater = data.RedLEDStatus === "On" ? "greenyellow" : "red";
                    document.getElementById("s1heater").style.color= s1heater;
                }
            };
            xhr.open("GET", "/status", true);
            xhr.send();
        }
        setInterval(updateStatus, 1000); // Refresh every 1 second
        </script>
    
    <title>
        Station 1
    </title>
</head>
        <body>
            <!--navigation bar-->
            <div id="navbar">
                <a class="active" href="index.html">Home</a>
                <a href="busstoplist.html">Bus Stop list</a></a>
                <a href="aboutus.html">About Us</a>
            </div>
            <!--big station text-->
            <h1>
                Station 1
            </h1>
            <!-- where data is inserted-->
            <p>
                date here
                <br>
                <br>
                Temperature: ...
                <br>
                <br>
                Capacity: ...
            </p>
            <!--light fan and heater status for different weather conditions-->
            <h2 style="position: absolute; left: 700px; top: 250px">
                Light Status:
            </h2>
            <h2 style="position: absolute; left: 400px; top: 450px">
            Fan Status:
            </h2>
            <h2 style="position: absolute; left: 700px; top: 450px">
                Heater Status:
            </h2>
            <h3 id="s1light" style="position: absolute; left: 745px; top: 275px; color: """+ led_Light_color +""";">
                <strong id="led_Light_status">""" + led_Light_status + """</strong>
            </h3>
            <h3 id="s1fan" style="position: absolute; left: 435px; top: 475px; color: """+ led_Temp2_color +""";">
                <strong id="led_Temp2_status">""" + led_Temp2_status + """</strong>
            </h3>
            <h3 id="s1heater" style="position: absolute; left: 745px; top: 475px; color: """+ led_Temp1_color +"""">
                <strong id="led_Temp1_status">""" + led_Temp1_status + """</strong>
            </h3>
        </body>
    </html>
    """
    return html

def get_station2():
    led_Light_status = get_led_Light_status()
    led_Temp1_status = get_led_Temp1_status()
    led_Temp2_status = get_led_Temp2_status()
    led_Light_color = "red" if led_Light_status == "Off" else "green"
    led_Temp1_color = "red" if led_Temp1_status == "Off" else "green"
    led_Temp2_color = "red" if led_Temp2_status == "Off" else "green"
    html = """<html>
<head>
    <title>Station 2</title>
        <!-- i do not know what this does but slay-->
        <link rel="icon" type="image/x-icon" href="assets/favicon.ico" />
        <!-- website little icon on the tab-->
        <link href="https://upload.wikimedia.org/wikipedia/commons/a/ae/Bus_icon_white_and_blue_background.svg" rel="shortcut icon" />
    <style>
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
        body {background-color: #fdf2e3;}
        h1 {
            color: #0e4e2f;
            font-family: 'Courier New', Courier, monospace;
            font-weight: bolder;
            font-size: 600%;
            text-align: center;
        }
        p {
            color: #0e4e2f;
            font-family: 'Trebuchet MS';
            font-size: 150%;
            position: absolute;
            left: 400px;
            top: 250px;
        }
        h2 {
            color: #0e4e2f;
            font-family: 'Trebuchet MS';
            font-size: 150%;
        }
        h3 {
            color: #0e4e2f;
            font-family: 'Trebuchet MS';
            font-size: 200%;
        }
    </style>
    <script>
        function updateStatus() {
            var xhr = new XMLHttpRequest();
            xhr.onreadystatechange = function() {
                if (xhr.readyState == 4 && xhr.status == 200) {
                    var data = JSON.parse(xhr.responseText);
                   
                    document.getElementById("led_Light_status").innerHTML = data.led_Light_status;
                    document.getElementById("led_Temp1_status").innerHTML = data.led_Temp1_status;
                    document.getElementById("led_Temp2_status").innerHTML = data.led_Temp2_status;
                    
                    var s2light = data.RedLEDStatus === "On" ? "greenyellow" : "red";
                    document.getElementById("s2light").style.color= s2light;
                    
                    var s2fan = data.RedLEDStatus === "On" ? "greenyellow" : "red";
                    document.getElementById("s2fan").style.color= s2fan;
                    
                    var s2heater = data.RedLEDStatus === "On" ? "greenyellow" : "red";
                    document.getElementById("s2heater").style.color= s2heater;
                }
            };
            xhr.open("GET", "/status", true);
            xhr.send();
        }
        setInterval(updateStatus, 1000); // Refresh every 1 second
        </script>
    <title>
        Station 2
    </title>
</head>
<body>
    <div id="navbar">
        <a class="active" href="index.html">Home</a>
        <a href="busstoplist.html">Bus Stop list</a></a>
        <a href="aboutus.html">About Us</a>
    </div>
    <h1>
        Station 2
    </h1>
    <p>
        date here
        <br>
        <br>
        Temperature: ...
        <br>
        <br>
        Capacity: ...
    </p>
    <h2 style="position: absolute; left: 700px; top: 250px">
        Light Status:
    </h2>
    <h2 style="position: absolute; left: 400px; top: 450px">
        Fan Status:
    </h2>
    <h2 style="position: absolute; left: 700px; top: 450px">
        Heater Status:
    </h2>
    <h3 id="s2light" style="position: absolute; left: 745px; top: 275px; color: """+ led_Light_color +""";">
        <strong id="led_Light_status">""" + led_Light_status + """</strong>
    </h3>
    <h3 id="s2fan" style="position: absolute; left: 435px; top: 475px; color: """ + led_Temp2_color + """;">
        <strong id="led_Temp2_status">""" + led_Temp2_status + """</strong>
    </h3>
    <h3 id="s2heater" style="position: absolute; left: 745px; top: 475px; color: """ + led_Temp1_color + """;">
        <strong id="led_Temp1_status">""" + led_Temp1_status + """</strong>
    </h3>
</body>
</html>
"""
    return html

def aboutus():
    html = """ <html>
    <head>
    <link rel="icon" type="image/x-icon" href="assets/favicon.ico" />
    <!-- website little icon on the tab-->
    <link href="https://upload.wikimedia.org/wikipedia/commons/a/ae/Bus_icon_white_and_blue_background.svg" rel="shortcut icon" />
    <style>
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
        body {background-color: #fdf2e3;}
        h1 {
            color: #d44038;
            font-family: 'Courier New', Courier, monospace;
            font-weight: bolder;
            font-size: 600%;
            text-align: center;
        }
        p {
            color: #702521;
            font-family: 'Trebuchet MS';
            font-size: 150%;
            text-align: center;
        }
    </style>
</head>
<body>
    <div id="navbar">
        <a class="active" href="index.html">Home</a>
        <a href="busstoplist.html">Bus Stop list</a></a>
        <a href="aboutus.html">About Us</a>
    </div>
    <h1>
        About Us
    </h1>
    <p>
        Our goal is to integrate smart bus stops across Victoria to encourage.........
    </p>
</body>
</html>"""
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
    elif request.find("/aboutus.html")==6:
        response = aboutus()
        conn.send("HTTP/1.1 200 OK\n")
        conn.send("Content-Type: text/html\n")
        conn.send("Connection: close\n\n")
        conn.sendall(response)
    conn.close()
   




