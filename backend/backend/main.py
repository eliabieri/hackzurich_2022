from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
import RPi.GPIO as GPIO


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
    try:
        match direction:
            case "up":
                accelerate()
            case "down":
                brake()
            case "left":
                turnLeft()
            case "right":
                turnRight()
            case _:
                print("Invalid direction", flush=True)
        print(direction, flush=True)
        return "Success"
    except Exception as e:
        ch1Control.stop()
        ch2Control.stop()
        return f"exception {e}"


def updateSpeeds():
    if ch1SpeedPromille > 0:
        ch1Control.ChangeDutyCycle(ch1SpeedPromille/10)
        print("CH1 running: " + str(ch1SpeedPromille/10) + "%", flush=True)
    else:
        ch1Control.stop()
        print("CH1 stopped.", flush=True)
    if ch2SpeedPromille > 0:
        ch2Control.ChangeDutyCycle(ch2SpeedPromille/10)
        print("CH2 running: " + str(ch2SpeedPromille/10) + "%", flush=True)
    else:
        ch2Control.stop()
        print("CH2 stopped.", flush=True)

def accelerate():
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
    if ch1SpeedPromille > 0:
        ch1SpeedPromille = ch1SpeedPromille-BRAKE_FACTOR
    if ch2SpeedPromille > 0:
        ch2SpeedPromille = ch2SpeedPromille-BRAKE_FACTOR
    updateSpeeds()

def turnLeft():
    if ch1SpeedPromille < MAX_SPEED:
        ch1SpeedPromille = ch1SpeedPromille+TURN_FACTOR
        updateSpeeds()

def turnRight():
    if ch2SpeedPromille < MAX_SPEED:
        ch2SpeedPromille = ch2SpeedPromille+TURN_FACTOR
        updateSpeeds()