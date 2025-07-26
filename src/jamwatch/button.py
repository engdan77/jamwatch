from typing import Callable

import gpiozero
from .log import logger
from dataclasses import dataclass, field


class ButtonConfig:
    gpio_pin: int = 22
    hold_time: int = 2
    pressed_func: Callable = None
    pressed_func_args: tuple = ()
    pressed_func_kwargs: dict = field(default_factory=dict)


class Button:
    def __init__(self, config: ButtonConfig):
        self.config = config

        self.button = gpiozero.Button(config.gpio_pin, hold_time=config.hold_time)
        logger.info(
            f"Button initialized on pin {config.gpio_pin} with hold time {config.hold_time} seconds"
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
        self.config.pressed_func(*self.config.pressed_func_args, **self.config.pressed_func_kwargs)

    def add_pressed_func(self, func: Callable, *args, **kwargs):
        self.config.pressed_func = func
        self.config.pressed_func_args = args
        self.config.pressed_func_kwargs = kwargs


if __name__ == "__main__":
    button = Button(ButtonConfig())
    button.button.wait_for_press()