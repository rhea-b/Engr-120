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
        document.getElementById("s1light").innerHTML = data.RedLEDStatus;
        document.getElementById("s1fan").innerHTML = data.RedLEDStatus;
        document.getElementById("s1heater").innerHTML = data.RedLEDStatus;
        document.getElementById("s2light").innerHTML = data.RedLEDStatus;
        document.getElementById("s2fan").innerHTML = data.RedLEDStatus;
        document.getElementById("s2heater").innerHTML = data.RedLEDStatus;
    </script>
    
    </head>
    <body>
     
    <p>RedLED Status: <p id="textonoff" style="color: """ + LED_color + """;" ><strong id="RedLEDStatus">""" + redLED_status + """</strong></p>
    <div class="circle" id="buzzerIndicator" style="background-color: """ + LED_color + """;"></div></p>    
  
    </body>
    </html>"""