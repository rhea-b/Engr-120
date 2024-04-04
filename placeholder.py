"""<html><head>
    <title>Pico Web Server</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="icon" href="data:,">
    <style>
        html {
            font-family: Helvetica;
            text-align: center;
            background-color: #b0b2b2;
        }
        h1 {
            color: #0F3376;
            padding: 2vh;
        }
        p {
            font-size: 1.5rem;
        }
        

        .circle {
            width: 20px;
            height: 20px;
            border-radius: 50%;
            display: inline-block;
            margin-left: 10px;
        }
    </style>
    <script>
        document.getElementById("s1light").style.color= s1light;
        var s1light = data.RedLEDStatus === "On" ? "greenyellow" : "red";
        document.getElementById("s1fan").style.color= s1fan;
        var s1fan = data.RedLEDStatus === "On" ? "greenyellow" : "red";
        document.getElementById("s1heater").style.color= s1heater;
        var s1heater = data.RedLEDStatus === "On" ? "greenyellow" : "red";
        document.getElementById("s2light").style.color= s2light;
        var s2light = data.RedLEDStatus === "On" ? "greenyellow" : "red";
        document.getElementById("s2fan").style.color= s2fan;
        var s2fan = data.RedLEDStatus === "On" ? "greenyellow" : "red";
        document.getElementById("s2heater").style.color= s2heater;
        var s2heater = data.RedLEDStatus === "On" ? "greenyellow" : "red";
    </script>
    
    </head>
    <body>
     
    <p>RedLED Status: <p id="textonoff" style="color: """ + LED_color + """;" ><strong id="RedLEDStatus">""" + redLED_status + """</strong></p>
    <div class="circle" id="buzzerIndicator" style="background-color: """ + LED_color + """;"></div></p>    
  
    </body>
    </html>"""