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
SERVO_FULL_LEFT_DC = 50
SERVO_FULL_RIGHT_DC = 100
TURN_FACTOR = 5

MOTOR_IN1 = 13
MOTOR_IN2 = 14



#Use BOARD numbering for pin numbers
GPIO.setmode(GPIO.BCM)


#Initialize GPIOs
GPIO.setup(SERVO_PIN, GPIO.OUT, initial=GPIO.LOW)
# GPIO.setup(CH2_PIN, GPIO.OUT, initial=GPIO.LOW)


#Initalize as PWM
servoControl = GPIO.PWM(SERVO_PIN, PWM_FREQUENCY_SERVO_HZ)
# ch2Control = GPIO.PWM(CH2_PIN, PWM_FREQUENCY)

servoDirection = 0

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
    global ch1SpeedPromille
    global ch2SpeedPromille
    try:
        if direction == "up":
            accelerate()
        elif direction == "down":
            brake()
        elif direction == "left":
            turnLeft()
        elif direction == "right":
            turnRight()
        else:
            goNeutral()
            log.info("Invalid direction")
        log.info(direction)
        return f"ch1Speed={ch1SpeedPromille/10} ch2Speed={ch2SpeedPromille/10}"
    except Exception as e:
        servoControl.stop()
        # ch2Control.stop()
        return f"exception {e}"


#pass -100 for full left, pass +100 for full right
def getServoPwm(direction):
    if(direction < -100):
        return 50
    if(direction > 100):
        return 100
    #converts -100 (full left) to 50% duty cycle, and +100 to 100% duty cycle
    return ((((direction+100)/100)*25) + 50)

def updateSpeeds():
    global servoDirection
    if servoDirection > -1 or servoDirection < 1:
        servoControl.stop()
    else:
        servoControl.ChangeDutyCycle(getServoPwm(servoDirection))

# def accelerate():
    # global ch1SpeedPromille
    # global ch2SpeedPromille
    # if (ch1SpeedPromille < MAX_SPEED) or (ch2SpeedPromille < MAX_SPEED):
    #     if ch1SpeedPromille < MAX_SPEED:
    #         #Start PWM if not already started
    #         if ch1SpeedPromille == 0:
    #             ch1Control.start(0.1)
    #         ch1SpeedPromille = ch1SpeedPromille+ACCELERATION_FACTOR
    #     if ch2SpeedPromille < MAX_SPEED:
    #         #Start PWM if not already started
    #         if ch2SpeedPromille == 0:
    #             ch2Control.start(0.1)
    #         ch2SpeedPromille = ch2SpeedPromille+ACCELERATION_FACTOR
    #     updateSpeeds()

# def brake():
    # global ch1SpeedPromille
    # global ch2SpeedPromille
    # if ch1SpeedPromille > 0:
    #     ch1SpeedPromille = ch1SpeedPromille-BRAKE_FACTOR
    # if ch2SpeedPromille > 0:
    #     ch2SpeedPromille = ch2SpeedPromille-BRAKE_FACTOR
    # updateSpeeds()

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
    updateSpeeds()