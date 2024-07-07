# File: test.py
from time import sleep

import utime

from utils.led import LED, DualColorLED


def test_led():
    # Example usage of the LED class
    led = LED(15)  # Example GPIO pin number
    led.on()
    sleep(1)
    led.off()
    sleep(1)
    led.on(2000)
    sleep(4)
    led.blink("+-+-+---", 100, continuous=True)
    sleep(10)
    led.stop_blink()
    print(f"LED is on: {led.is_on()}")
    print(f"LED is blinking: {led.is_blinking()}")


def test_dual_color_led():
    # Example usage of the DualColorLED class
    dual_led = DualColorLED(10, 15)  # Example GPIO pin numbers for green and red LEDs
    print("Turning green on...")
    dual_led.green_on()
    sleep(1)
    dual_led.green_on(2000)
    print("Turning red on...")
    dual_led.red_on()
    sleep(1)
    dual_led.red_on(2000)
    print("Starting green blink...")
    dual_led.blink("green", "+++--", 500, continuous=True)
    sleep(10)
    print("Starting red blink...")
    dual_led.blink("red", "++--", 500, continuous=True)
    sleep(10)
    print("Stopping blink...")
    dual_led.stop_blink()
    print(f"Green LED is on: {dual_led.is_green_on()}")
    print(f"Red LED is on: {dual_led.is_red_on()}")
    print(f"Green LED is blinking: {dual_led.is_green_blinking()}")
    print(f"Red LED is blinking: {dual_led.is_red_blinking()}")


if __name__ == "__main__":
    test_led()
    test_dual_color_led()
