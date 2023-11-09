from time import sleep

import ubinascii
from machine import UART, Pin, Timer


def parse_packet(packet):
    """Attempts to parse a packet from the RFID chip.

    Args:
        packet (bytes): The packet to try and parse.
    """
    length = 14
    header = 0x02
    stop_byte = 0x03

    headerPosition = 0
    stopBytePosition = 13

    rawDataStart = headerPosition + 1
    rawDataEnd = rawDataStart + 10

    checksumStart = rawDataEnd
    checksumEnd = checksumStart + 2

    # check for the packet length
    if len(packet) != length:
        print("WARNING: RFID packet has an invalid length ({}).".format(len(packet)))
        print("Packet was: ", packet)
        return None

    # check for the packet header
    if packet[headerPosition] != header:
        print("WARNING: RFID packet header is invalid.")
        return None

    # check for the packet stop byte
    if packet[stopBytePosition] != stop_byte:
        print("WARNING: RFID packet stop byte is invalid.")
        return None

    card_data = packet[rawDataStart:rawDataEnd]  # raw bytes of the card data
    checksum = packet[checksumStart:checksumEnd]  # checksum sent by RFID reader
    calculated_checksum = 0  # holds the checksum we calculate from the card id

    # loop through each byte in the card data and calculate the checksum by XORing them all
    for x in ubinascii.unhexlify(card_data):
        calculated_checksum = calculated_checksum ^ x

    checksumHexInt = int(chr(checksum[0]) + chr(checksum[1]), 16)

    # check that the calculated checksum matches the one sent by the RFID reader
    if checksumHexInt != calculated_checksum:
        print("WARNING: RFID checksum verification failed.")
        return None

    # if we get to here it means we received a valid packet, hurray!
    # lets remove the first byte (not part of the card ID) and convert it to a string
    card_id = card_data[2:].decode("ascii")

    # return a string of the decimal (integer) representation
    return str(int(card_id, 16))


readAllowed = True


def resetLastChip(self):
    global readAllowed
    readAllowed = True


uart = UART(0)
uart.init(baudrate=9600, bits=8, parity=None, stop=1, rx=Pin(1, mode=Pin.IN))

resetTimer = Timer()
resetTimer.deinit()
resetTimer.init(period=1000, mode=Timer.PERIODIC, callback=resetLastChip)

lastChipId = ""
while True:
    data = uart.read()

    if data != None and readAllowed:
        parsed = parse_packet(data)

        if parsed == None:
            # Handle errors here
            break
        elif parsed != lastChipId:
            lastChipId = parsed
            readAllowed = False

            print("The chip id is: ", parsed)
