import RPi.GPIO as GPIO
import subprocess
import time

#cancels out warnings for now
GPIO.setwarnings(False)


#Setting mode for GPIO to use [Board(pin number) or BCM(gpio number)]
GPIO.setmode(GPIO.BOARD)
time.sleep(1)


"""Setting up Button on Pin #7 on the pi, Setting to input,
    using pull up/down to set the inital value, looking for a down
"""

GPIO.setup(7, GPIO.IN, pull_up_down=GPIO.PUD_UP)


#Setting up RED LED on Pin #32 on the pi, setting to output, and setting initial to off

GPIO.setup(32, GPIO.OUT, initial=GPIO.LOW)


#Setting up GREEN LED on Pin #16 on the pi, setting to output, and setting initial to off

GPIO.setup(16, GPIO.OUT, initial=GPIO.LOW)


#Setting up BLUE LED on Pin #22 on the pi, setting to output, and setting initial to on

GPIO.setup(22, GPIO.OUT, initial=GPIO.HIGH)

time.sleep(1)



"""Runs a continuous loop, checking for the status of kismet.service. 
    When the Buttons are up, if kismet is running = Green LED. Kismet not running = Red LED
    If the button is pressed and kismet is running, it
    stops kismet. 
    If kismet is not running, it starts it.

    Blue - 22
    Red - 32
    Green - 16
"""
try:
    while True:
        time.sleep(0.1)
        result = subprocess.run(['pgrep', 'kismet'], 
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                text=True)

        status = result.stdout.strip()


        if len(status) > 0:
            if GPIO.input(7) == GPIO.HIGH:
                GPIO.output(16, GPIO.HIGH)
                GPIO.output(32, GPIO.LOW)

            elif GPIO.input(7) == GPIO.LOW:
                pids = status.splitlines()
                for pid in pids:
                    subprocess.run(['kill', '-14', pid])

                print("Stopping Kismet")
                time.sleep(0.5)



        else:
            if GPIO.input(7) == GPIO.HIGH:
                GPIO.output(32, GPIO.HIGH)
                GPIO.output(16, GPIO.LOW)

            elif GPIO.input(7) == GPIO.LOW:
                subprocess.run(['sudo', 'airmon-ng', 'start', 'wlan1'])
                subprocess.Popen(['/usr/local/bin/kismet-autolog.sh'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                print("Starting Kismet")
                time.sleep(0.5)



except KeyboardInterrupt:
    print("Exiting on Ctrl+C...")

finally:
    GPIO.cleanup()


