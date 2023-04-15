import machine
from PIN_DEFS import LED_PINS
import time


def light(LED_PIN):
    machine.pin(LED_PIN, machine.pin.OUT).on()


def lightShow(LEDS, REPETITIONS=2):
    for LIGHT in LEDS:
        blink(LIGHT, REPETITIONS)


def dim(LEDS=LED_PINS):
    for LIGHT in LEDS:
        machine.pin(LIGHT, machine.pin.OUT).off()


def blink(LED_NAME, REPETITIONS):
    # NEED TO DELEGATE BLINKABILITY SO AS NOT TO USE RESOURCES TOO MUCH
    while REPETITIONS:
        led = Pin(LED_NAME, machine.pin.OUT)
        led.on()
        time.sleep(0.5)
        led.off()
        time.sleep(0.5)
        REPETITIONS -= 1