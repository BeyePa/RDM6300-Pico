import time

import ubinascii
from machine import UART, Pin, Timer


class RFIDReader:
    def __init__(self, gpioPin, logEnabled=False):
        self.uart = UART(0)
        self.uart.init(
            baudrate=9600, bits=8, parity=None, stop=1, rx=Pin(gpioPin, mode=Pin.IN)
        )

        self.read_allowed = True
        self.last_chip_id = ""
        self.log_enabled = logEnabled

    def reset_last_chip(self, timer):
        self.read_allowed = True
        self.last_chip_id = ""

    def start_reset_timer(self):
        self.reset_timer = Timer()
        self.reset_timer.deinit()
        self.reset_timer.init(
            period=1000, mode=Timer.PERIODIC, callback=self.reset_last_chip
        )

    def stop_reset_timer(self):
        if self.reset_timer == None:
            return

        self.reset_timer.deinit()
        self.reset_timer = None

    def parse_packet(self, packet):
        length = 14
        header = 0x02
        stop_byte = 0x03

        header_position = 0
        stop_byte_position = 13

        raw_data_start = header_position + 1
        raw_data_end = raw_data_start + 10

        checksum_start = raw_data_end
        checksum_end = checksum_start + 2

        # check for the packet length
        if len(packet) != length:
            self.log(
                "WARNING: RFID packet has an invalid length ({}).".format(len(packet))
            )
            self.log("Packet was: ", packet)
            return None

        # check for the packet header
        if packet[header_position] != header:
            self.log("WARNING: RFID packet header is invalid.")
            return None

        # check for the packet stop byte
        if packet[stop_byte_position] != stop_byte:
            self.log("WARNING: RFID packet stop byte is invalid.")
            return None

        card_data = packet[raw_data_start:raw_data_end]  # raw bytes of the card data
        checksum = packet[checksum_start:checksum_end]  # checksum sent by RFID reader
        calculated_checksum = 0  # holds the checksum we calculate from the card id

        # loop through each byte in the card data and calculate the checksum by XORing them all
        for x in ubinascii.unhexlify(card_data):
            calculated_checksum = calculated_checksum ^ x

        checksum_hex_int = int(chr(checksum[0]) + chr(checksum[1]), 16)

        # check that the calculated checksum matches the one sent by the RFID reader
        if checksum_hex_int != calculated_checksum:
            self.log("WARNING: RFID checksum verification failed.")
            return None

        # if we get to here it means we received a valid packet
        # lets remove the first byte (not part of the card ID) and convert it to a string
        card_id = card_data[2:].decode("ascii")

        # return a string of the decimal (integer) representation
        return str(int(card_id, 16))

    def read_single_chip(self, timeout_ms=None):
        self.read_allowed = True
        start_time = time.ticks_ms()

        while True:
            if (
                timeout_ms is not None
                and time.ticks_diff(time.ticks_ms(), start_time) > timeout_ms
            ):
                self.log("Timeout reached for single chip read.")
                return None

            data = self.uart.read()

            if data is not None and self.read_allowed:
                parsed = self.parse_packet(data)

                if parsed is None:
                    # Handle errors here
                    continue

                self.last_chip_id = parsed
                self.read_allowed = False

                self.log("Single shot run: The chip id is:", parsed)
                return parsed

    def detect_chip_with_id(self, target_id, timeout_ms=None):
        self.read_allowed = True
        start_time = time.ticks_ms()

        while True:
            if (
                timeout_ms is not None
                and time.ticks_diff(time.ticks_ms(), start_time) > timeout_ms
            ):
                self.log("Timeout reached for specific chip read.")
                return None
            data = self.uart.read()

            if data is not None and self.read_allowed:
                parsed = self.parse_packet(data)

                if parsed is None:
                    # Handle errors here
                    continue

                self.last_chip_id = parsed

                if parsed == target_id:
                    self.read_allowed = False
                    self.log("Run until {}: The chip id is:".format(target_id), parsed)
                    return parsed

    def read_continuously(self, shouldStop=False, timeout_ms=None):
        self.read_allowed = True
        start_time = time.ticks_ms()

        self.start_reset_timer()

        while not shouldStop:
            if not self.read_allowed:
                continue

            if (
                timeout_ms is not None
                and time.ticks_diff(time.ticks_ms(), start_time) > timeout_ms
            ):
                self.log("Timeout reached for continuous chip read.")
                return None

            data = self.uart.read()

            if data is not None:
                parsed = self.parse_packet(data)

                if parsed is None:
                    # Handle errors here
                    continue

                self.last_chip_id = parsed
                self.read_allowed = False
                self.log("Run indefinitely: The chip id is:", parsed)
                yield parsed

    def enable_logging(self):
        self.log_enabled = True

    def disable_logging(self):
        self.log_enabled = False

    def log(self, *args):
        if self.log_enabled:
            print("[RFIDReader]", *args)


# Example usage:

# rfid_reader = RFIDReader()

# # Single shot run
# chip_id = rfid_reader.single_shot_run()
# print("Single shot run result:", chip_id)

# # Run until a specific ID is detected
# target_id = "ABCDEF012345"
# chip_id = rfid_reader.run_until(target_id)
# print("Run until {} result:".format(target_id), chip_id)

# # Run indefinitely
# for chip_id in rfid_reader.run_indefinitely():
#     print("Run indefinitely result:", chip_id)
#     # Add your custom handling logic here
