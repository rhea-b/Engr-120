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
    
    
    </head>
    <body>
     
    <p>RedLED Status: <p id="textonoff" style="color: """ + LED_color + """;" ><strong id="RedLEDStatus">""" + redLED_status + """</strong></p>
    <div class="circle" id="buzzerIndicator" style="background-color: """ + LED_color + """;"></div></p>    
  
    </body>
    </html>"""