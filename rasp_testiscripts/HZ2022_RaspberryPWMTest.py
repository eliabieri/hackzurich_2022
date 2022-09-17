try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Error importing RPi.GPIO!  This is probably because you need superuser privileges.  You can achieve this by using 'sudo' to run your script")

import time
import math

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
try:
    while 1:
        for i in range(6):
            #Increment Duty Cycle by 20% every pass
            motorControl.ChangeDutyCycle(i*20)

            steeringAngleOffset = (i/5)*(2*math.pi)
            #Steering angle offset somewhere between +/-25% DC value
            steeringAngleOffset = math.sin(steeringAngleOffset)*(25)
            #DC value between 50% and 100%
            steeringControl.ChangeDutyCycle(PWM_75_DC+steeringAngleOffset)

            print("Step " + str(i+1) + "/6, ")
            print("motorPin = " + str(i*20) + "%, ")
            print("steeringPin = " + str(PWM_75_DC+steeringAngleOffset) + "%\n")

            time.sleep(3)
except KeyboardInterrupt:
    GPIO.cleanup()
    print("Cleaned up\n")

