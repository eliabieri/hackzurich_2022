try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Error importing RPi.GPIO!  This is probably because you need superuser privileges.  You can achieve this by using 'sudo' to run your script")

import time
import math
import keyboard

MOTOR_CONTROL_PIN = 13
STEERING_CONTROL_PIN = 12
PWM_FREQUENCY = 10000

PWM_MAX_DC = 100
PWM_75_DC = 75
PWM_NOM_DC = 50
PWM_MIN_DC = 0

#Use BOARD numbering for pin numbers
GPIO.setmode(GPIO.BCM)

#Initialize GPIOs
GPIO.setup(MOTOR_CONTROL_PIN, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(STEERING_CONTROL_PIN, GPIO.OUT, initial=GPIO.LOW)

#Initalize as PWM
motorControl = GPIO.PWM(MOTOR_CONTROL_PIN, PWM_FREQUENCY)
steeringControl = GPIO.PWM(STEERING_CONTROL_PIN, PWM_FREQUENCY)

motorControl.start(0)
steeringControl.start(0)

motorSpeed = 0

try:
    while 1:
        if keyboard.read_key() == "w":
            if motorSpeed < 21:
                motorSpeed = motorSpeed+1
        if keyboard.read_key() == "s":
            if motorSpeed > 0:
                motorSpeed = motorSpeed-1
        motorControl.ChangeDutyCycle(motorSpeed)
        print(f"motorSpeed = {motorSpeed} %")
        time.sleep(0.01)
except KeyboardInterrupt:
    GPIO.cleanup()
    print("Cleaned up\n")

