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


CH1_PIN = 12
CH2_PIN = 13
PWM_FREQUENCY = 100000

PWM_MAX_DC_PROMILLE = 1000
PWM_75_DC_PROMILLE = 750
PWM_NOM_DC_PROMILLE = 500
PWM_MIN_DC_PROMILLE = 1

MAX_SPEED = 500
ACCELERATION_FACTOR = 1
BRAKE_FACTOR = 1
TURN_FACTOR = 5

#Use BOARD numbering for pin numbers
GPIO.setmode(GPIO.BCM)


#Initialize GPIOs
GPIO.setup(CH1_PIN, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(CH2_PIN, GPIO.OUT, initial=GPIO.LOW)


#Initalize as PWM
ch1Control = GPIO.PWM(CH1_PIN, PWM_FREQUENCY)
ch2Control = GPIO.PWM(CH2_PIN, PWM_FREQUENCY)

ch1SpeedPromille = 0
ch2SpeedPromille = 0

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
            log.info("Invalid direction")
        log.info(direction)
        return f"ch1Speed={ch1SpeedPromille/10} ch2Speed={ch2SpeedPromille/10}"
    except Exception as e:
        ch1Control.stop()
        ch2Control.stop()
        return f"exception {e}"


def updateSpeeds():
    global ch1SpeedPromille
    global ch2SpeedPromille
    if ch1SpeedPromille > 0:
        ch1Control.ChangeDutyCycle(ch1SpeedPromille/10)
        log.info("CH1 running: " + str(ch1SpeedPromille/10) + "%")
    else:
        ch1Control.stop()
        log.info("CH1 stopped.")
    if ch2SpeedPromille > 0:
        ch2Control.ChangeDutyCycle(ch2SpeedPromille/10)
        log.info("CH2 running: " + str(ch2SpeedPromille/10) + "%")
    else:
        ch2Control.stop()
        log.info("CH2 stopped.")

def accelerate():
    global ch1SpeedPromille
    global ch2SpeedPromille
    if (ch1SpeedPromille < MAX_SPEED) or (ch2SpeedPromille < MAX_SPEED):
        if ch1SpeedPromille < MAX_SPEED:
            #Start PWM if not already started
            if ch1SpeedPromille == 0:
                ch1Control.start(0.1)
            ch1SpeedPromille = ch1SpeedPromille+ACCELERATION_FACTOR
        if ch2SpeedPromille < MAX_SPEED:
            #Start PWM if not already started
            if ch2SpeedPromille == 0:
                ch2Control.start(0.1)
            ch2SpeedPromille = ch2SpeedPromille+ACCELERATION_FACTOR
        updateSpeeds()

def brake():
    global ch1SpeedPromille
    global ch2SpeedPromille
    if ch1SpeedPromille > 0:
        ch1SpeedPromille = ch1SpeedPromille-BRAKE_FACTOR
    if ch2SpeedPromille > 0:
        ch2SpeedPromille = ch2SpeedPromille-BRAKE_FACTOR
    updateSpeeds()

def turnLeft():
    global ch1SpeedPromille
    global ch2SpeedPromille
    if ch1SpeedPromille < MAX_SPEED:
        ch1SpeedPromille = ch1SpeedPromille+TURN_FACTOR
        updateSpeeds()

def turnRight():
    global ch1SpeedPromille
    global ch2SpeedPromille
    if ch2SpeedPromille < MAX_SPEED:
        ch2SpeedPromille = ch2SpeedPromille+TURN_FACTOR
        updateSpeeds()