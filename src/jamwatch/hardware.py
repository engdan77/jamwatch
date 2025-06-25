import gpiozero

green_led = gpiozero.PWMLED(17)
red_led = gpiozero.PWMLED(27)

gpiozero.Button.was_held = False

button = gpiozero.Button(22)


def held(btn):
    btn.was_held = True
    print("button was held not just pressed")


def released(btn):
    if not btn.was_held:
        pressed()
    btn.was_held = False


def pressed():
    print("button was pressed not held")


button.when_held = held
button.when_released = released
