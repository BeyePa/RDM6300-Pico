from machine import Timer

from utils.rfid import RFIDReader


def test_single_shot_run():
    print("\nTesting single shot run...")
    rfid_reader = RFIDReader()
    chip_id = rfid_reader.read_single_chip()
    print("Single shot run result:", chip_id)


def test_run_until():
    print("\nTesting run until specific ID is detected...")
    rfid_reader = RFIDReader()
    target_id = "6373576"
    chip_id = rfid_reader.detect_chip_with_id(target_id)
    print("Run until {} result:".format(target_id), chip_id)


def test_run_indefinitely():
    print("\nTesting run indefinitely...")
    rfid_reader = RFIDReader(True)

    shouldStop = False

    def stopContinuousRead(timer):
        shouldStop = True

    stopTimer = Timer()
    stopTimer.init(period=10000, mode=Timer.ONE_SHOT, callback=stopContinuousRead)

    for chip_id in rfid_reader.read_continuously(shouldStop):
        print("Run indefinitely result:", chip_id)
        # Add your custom handling logic here
        # break  # Uncomment to limit the indefinite run for testing purposes


if __name__ == "__main__":
    test_single_shot_run()
    test_run_until()
    test_run_indefinitely()
