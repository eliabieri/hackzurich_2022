from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
import RPi.GPIO as GPIO

import logging
from rich.logging import RichHandler


FORMAT = "%(message)s"
logging.basicConfig(
    level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)

log = logging.getLogger("rich")


SERVO_PIN = 12
PWM_FREQUENCY_SERVO_HZ = 500
SERVO_MAX_DUTYCYCLE_CHANGE = 10

TURN_FACTOR = 5

MOTOR_IN1 = 14
MOTOR_IN2 = 15

#Use BOARD numbering for pin numbers
GPIO.setmode(GPIO.BCM)

#Initialize GPIOs
GPIO.setup(SERVO_PIN, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(MOTOR_IN1, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(MOTOR_IN2, GPIO.OUT, initial=GPIO.LOW)

#Initalize servo pin as PWM
servoControl = GPIO.PWM(SERVO_PIN, PWM_FREQUENCY_SERVO_HZ)

servoDirection = 0
motorState = "brake"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/drive/{direction}")
def drive(direction: str):
    global servoDirection
    try:
        if direction == "up":
            driveForward()
        elif direction == "down":
            driveBackwards()
        elif direction == "left":
            turnLeft()
        elif direction == "right":
            turnRight()
        else:
            goNeutral()
        print(f"direction={direction}, servoDirection={servoDirection}, motorState={motorState}")
        return f"servoDirection={servoDirection}, motorState={motorState}"
    except Exception as e:
        servoControl.stop()
        GPIO.cleanup()
        print("Cleaned up\n")
        return f"exception {e}"


#pass -100 for full left, pass +100 for full right
def getServoPwm(direction):
    if(direction < -100):
        return 65
    if(direction > 100):
        return 85
    #converts -100 (full left) to 50% duty cycle, and +100 to 100% duty cycle
    return (((direction/100) * SERVO_MAX_DUTYCYCLE_CHANGE) + 75)

def updateSpeeds():
    global servoDirection
    if servoDirection > -1 or servoDirection < 1:
        servoControl.stop()
    else:
        servoControl.ChangeDutyCycle(getServoPwm(servoDirection))

def driveForward():
    global motorState
    if(motorState != "forward"):
        motorState = "forward"
        GPIO.output(MOTOR_IN1, GPIO.HIGH)
        GPIO.output(MOTOR_IN2, GPIO.LOW)

def driveBackwards():
    global motorState
    if (motorState != "backwards"):
        motorState = "backwards"
        GPIO.output(MOTOR_IN1, GPIO.LOW)
        GPIO.output(MOTOR_IN2, GPIO.HIGH)

def turnLeft():
    global servoDirection
    if servoDirection > (-100+TURN_FACTOR):
        servoDirection = servoDirection - TURN_FACTOR
    else:
        servoDirection = -100
        updateSpeeds()

def turnRight():
    global servoDirection
    if servoDirection < (100-TURN_FACTOR):
        servoDirection = servoDirection + TURN_FACTOR
    else:
        servoDirection = 100
        updateSpeeds()

def goNeutral():
    global servoDirection
    if(servoDirection < (2.5*TURN_FACTOR) or servoDirection > (-2.5*TURN_FACTOR)):
        servoDirection = 0
    else:
        if(servoDirection > 0):
            servoDirection = servoDirection - 2*TURN_FACTOR
        elif(servoDirection < 0):
            servoDirection = servoDirection + 2*TURN_FACTOR
    global motorState
    if(motorState != "brake"):
        motorState = "brake"
        GPIO.output(MOTOR_IN1, GPIO.LOW)
        GPIO.output(MOTOR_IN2, GPIO.LOW)
    updateSpeeds()