import gpiozero
from enum import StrEnum
from .log import logger
import sys
import os

if sys.platform == 'darwin':
    logger.info("Using mock GPIO for MacOS")
    os.environ['GPIOZERO_PIN_FACTORY'] = 'MOCK'


def round_to_quarter(percentage: int | float) -> int:
    match percentage:
        case x if 1 < x <= 25:
            return 25
        case x if 25 < x <= 50:
            return 50
        case x if 50 < x <= 75:
            return 75
        case x if 75 < x <= 100:
            return 100
    return 0


class BlinkState(StrEnum):
    OFF = "off"
    ON = "on"
    BLINK = "blink"


class Blink:
    def __init__(self, gpio_pin: int = 17):
        self.led = gpiozero.LED(gpio_pin)
        self.state = BlinkState.OFF
        self.perc_blink = 0

    def percentage(self, percentage: int | float, on_time_ms: int = 500, max_off_ms: int = 1000):
        if self.state == BlinkState.BLINK and self.perc_blink == round_to_quarter(percentage):
            return
        self.perc_blink = round_to_quarter(percentage)
        if self.perc_blink < 1:
            self.led.off()
            return
        if self.perc_blink > 99:
            self.led.on()
            return
        off_time_ms = (100 - self.perc_blink) / 100 * max_off_ms
        self.led.blink(on_time=on_time_ms, off_time=off_time_ms, background=True)
        self.state = BlinkState.BLINK
        logger.info(f"Blinking LED on for {on_time_ms}ms and off {off_time_ms}ms")

    def off(self):
        self.led.off()
        self.state = BlinkState.OFF
        logger.info("Turning LED off")

    def on(self):
        self.led.on()
        self.state = BlinkState.ON
        logger.info("Turning LED on")
