import gpiozero
from enum import StrEnum
from .log import logger
import sys
import os

if sys.platform == "darwin":
    logger.info("Using mock GPIO for MacOS")
    os.environ["GPIOZERO_PIN_FACTORY"] = "MOCK"


def round_percentage(percentage: int | float) -> int:
    p = int(percentage / 10) * 10
    if percentage > 0 and p < 10:
        return 5
    if percentage > 100:
        return 100
    return p


class BlinkState(StrEnum):
    OFF = "off"
    ON = "on"
    BLINK = "blink"


class Blink:
    def __init__(self, gpio_pin: int = 17):
        self.led = gpiozero.LED(gpio_pin)
        self.state = BlinkState.OFF
        self.perc_blink = 0

    def percentage(
        self, percentage: int | float, on_time_sec: int = 0.5, max_off_sec: int = 0.2
    ):
        if self.state == BlinkState.BLINK and self.perc_blink == round_percentage(
            percentage
        ):
            return
        self.perc_blink = round_percentage(percentage)
        if self.perc_blink < 1:
            self.led.off()
            return
        if self.perc_blink > 99:
            self.led.on()
            return
        off_time_secs = (
            (100 - self.perc_blink) / 100 * max_off_sec
        ) * 10  # TODO: improve this logic
        self.led.blink(on_time=on_time_sec, off_time=off_time_secs, background=True)
        self.state = BlinkState.BLINK
        logger.info(f"Blinking LED on for {on_time_sec}s and off {off_time_secs}s")

    def off(self):
        self.led.off()
        self.state = BlinkState.OFF
        logger.info("Turning LED off")

    def on(self):
        self.led.on()
        self.state = BlinkState.ON
        logger.info("Turning LED on")

    def close(self):
        self.led.close()
