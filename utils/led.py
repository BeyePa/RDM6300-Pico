import _thread

import machine
import utime


class LED:
    def __init__(self, pin_number):
        self.__pin = machine.Pin(pin_number, machine.Pin.OUT)
        self.__state = False  # Internal state: False means off, True means on
        self.__blinking = False
        self.__timeout_timer = None

    def on(self, timeout_ms=None):
        self.__pin.value(1)
        self.__state = True  # Update internal state to reflect LED is on
        if timeout_ms is not None:
            self.__timeout_timer = machine.Timer()
            self.__timeout_timer.init(
                period=timeout_ms,
                mode=machine.Timer.ONE_SHOT,
                callback=self.__timeout_callback,
            )

    def __timeout_callback(self, timer):
        self.off()
        self.timeout_timer = None

    def off(self):
        self.__pin.value(0)
        self.__state = False  # Update internal state to reflect LED is off
        if self.__timeout_timer is not None:
            self.__timeout_timer.deinit()
            self.__timeout_timer = None

    def blink(self, pattern, time_ms, continuous=False, n_times=1):
        self.stop_blink()

        def blink_thread():
            self.__blinking = True
            while self.__blinking:
                for _ in range(n_times):
                    if not self.__blinking:
                        break
                    for state in pattern:
                        if not self.__blinking:
                            break
                        if state == "+":
                            self.on()
                        elif state == "-":
                            self.off()
                        utime.sleep_ms(time_ms)
                if not continuous:
                    break
            self.off()

        _thread.start_new_thread(blink_thread, ())

    def stop_blink(self):
        self.__blinking = False
        utime.sleep_ms(10)  # Ensure thread has time to stop
        self.off()

    def is_on(self):
        return self.__state

    def is_blinking(self):
        return self.__blinking


class DualColorLED:
    def __init__(self, green_pin_number, red_pin_number):
        self.__green_led = LED(green_pin_number)
        self.__red_led = LED(red_pin_number)

    def green_on(self, timeout_ms=None):
        self.__red_led.off()  # Ensure the red LED is off
        self.__green_led.on(timeout_ms=timeout_ms)

    def red_on(self, timeout_ms=None):
        self.__green_led.off()  # Ensure the green LED is off
        self.__red_led.on(timeout_ms=timeout_ms)

    def off(self):
        self.__green_led.off()
        self.__red_led.off()

    def blink(self, color, pattern, time_ms, continuous=False, n_times=1):
        self.stop_blink()

        def blink_thread(led):
            led.blink(pattern, time_ms, continuous, n_times)

        if color == "green":
            # _thread.start_new_thread(blink_thread, (self.__green_led,))
            self.__green_led.blink(pattern, time_ms, continuous, n_times)
        elif color == "red":
            # _thread.start_new_thread(blink_thread, (self.__red_led,))
            self.__red_led.blink(pattern, time_ms, continuous, n_times)

    def stop_blink(self):
        self.__green_led.stop_blink()
        self.__red_led.stop_blink()

    def is_green_on(self):
        return self.__green_led.is_on()

    def is_red_on(self):
        return self.__red_led.is_on()

    def is_green_blinking(self):
        return self.__green_led.is_blinking()

    def is_red_blinking(self):
        return self.__red_led.is_blinking()


# Example usage:
# dual_led = DualColorLED(25, 26)  # Assuming the green LED is connected to GPIO 25 and red LED to GPIO 26
# dual_led.green_on()  # Turn on the green LED
# utime.sleep(1)
# dual_led.red_on()  # Turn on the red LED (this will turn off the green LED)
# utime.sleep(1)
# dual_led.blink('green', "+++--", 500, continuous=True)  # Blink green LED with pattern
# utime.sleep(10)  # Let it blink for 10 seconds
# dual_led.stop_blink()  # Stop blinking

# Check the internal state of green LED
# print(dual_led.is_green_on())  # Should be False if green LED is off
# Check the internal state of red LED
# print(dual_led.is_red_on())  # Should be False if red LED is off
# Check if green LED is blinking
# print(dual_led.is_green_blinking())  # Should be False if green LED is not blinking
# Check if red LED is blinking
# print(dual_led.is_red_blinking())  # Should be False if red LED is not blinking
