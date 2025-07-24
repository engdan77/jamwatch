import gpiozero
from .log import logger


class Button:
    def __init__(self, gpio_pin: int = 22, hold_time: int = 2):

        self.button = gpiozero.Button(gpio_pin, hold_time=hold_time)
        logger.info(
            f"Button initialized on pin {gpio_pin} with hold time {hold_time} seconds"
        )
        gpiozero.Button.was_held = False

        self.button.when_held = self.held
        self.button.when_released = self.released

    def held(self):
        self.button.was_held = True
        logger.info("button was held not just pressed")

    def released(self):
        if not self.button.was_held:
            self.pressed()
        self.button.was_held = False

    def pressed(self):
        logger.info("button was pressed not held")

