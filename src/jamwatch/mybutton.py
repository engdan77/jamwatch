import time
from typing import Callable

import gpiozero
from .log import logger
from dataclasses import dataclass, field

gpiozero.Button.was_held = False

@dataclass
class ButtonConfig:
    gpio_pin: int = 22
    hold_time: int = 2
    pressed_func: Callable = None
    pressed_func_args: tuple = ()
    pressed_func_kwargs: dict = field(default_factory=dict)


class MyButton:
    def __init__(self, config: ButtonConfig):
        self.config = config
        self.event_loop_running = False

        self.button = gpiozero.Button(config.gpio_pin, hold_time=config.hold_time)
        logger.info(
            f"Button initialized on pin {config.gpio_pin} with hold time {config.hold_time} seconds"
        )
        self.button.when_held = self.held
        self.button.when_released = self.released

    def start_event_loop(self):
        """Start listening for button events."""
        self.event_loop_running = True
        while self.event_loop_running:
            time.sleep(1)

    def stop_event_loop(self):
        """Stop listening for button events."""
        self.event_loop_running = False

    def held(self):
        self.button.was_held = True
        logger.info("Button was HELD not just pressed")

    def released(self):
        if not self.button.was_held:
            self.pressed()
        self.button.was_held = False

    def pressed(self):
        logger.info("Button was PRESSED not held")
        self.config.pressed_func(*self.config.pressed_func_args, **self.config.pressed_func_kwargs)

    def add_pressed_func(self, func: Callable, *args, **kwargs):
        self.config.pressed_func = func
        self.config.pressed_func_args = args
        self.config.pressed_func_kwargs = kwargs
