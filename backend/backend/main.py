from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
import RPi.GPIO as GPIO
import time

import logging
from rich.logging import RichHandler


FORMAT = "%(message)s"
logging.basicConfig(
    level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)

log = logging.getLogger("rich")

UP_PIN = 5
DOWN_PIN = 6
LEFT_PIN = 12
RIGHT_PIN = 13

#Use BOARD numbering for pin numbers
GPIO.setmode(GPIO.BCM)

#Initialize GPIOs
GPIO.setup(UP_PIN, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(DOWN_PIN, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(LEFT_PIN, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(RIGHT_PIN, GPIO.OUT, initial=GPIO.LOW)

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
        #depending on direction, output a 10ms pulse on according output
        if direction == "up":
            GPIO.output(UP_PIN, GPIO.HIGH)
            time.sleep(0.01)
            GPIO.output(UP_PIN, GPIO.LOW)
        elif direction == "down":
            GPIO.output(DOWN_PIN, GPIO.HIGH)
            time.sleep(0.01)
            GPIO.output(DOWN_PIN, GPIO.LOW)
        elif direction == "left":
            GPIO.output(LEFT_PIN, GPIO.HIGH)
            time.sleep(0.01)
            GPIO.output(LEFT_PIN, GPIO.LOW)
        elif direction == "right":
            GPIO.output(RIGHT_PIN, GPIO.HIGH)
            time.sleep(0.01)
            GPIO.output(RIGHT_PIN, GPIO.LOW)
        else:
            log.info("Invalid direction")
        log.info(direction)
        return "success"
    except Exception as e:
        return f"exception {e}"

