import config.webserver_conf as CONF
from microdot import Microdot
from static.rfid_test import HTML_CONTENT
from utils.led import DualColorLED
from utils.logger import Logger
from utils.rfid import RFIDReader

app = Microdot()
logger = Logger(CONF.LOG_LEVEL)
reader = RFIDReader(CONF.RFID_READER_GPIO)
led = DualColorLED(CONF.LED_GREEN_GPIO, CONF.LED_RED_GPIO)

DEFAULT_TIMEOUT = 30


def get_client_timeout(req):
    clientTimeout = req.form.get("timeout") if req.form is not None else None

    logger.debug(f"Client timeout is {clientTimeout}")
    timeout = int(clientTimeout) if clientTimeout is not None else DEFAULT_TIMEOUT

    logger.debug(f"Using timeout set to {timeout}")
    return timeout


def get_response(chip_id: str | None, successful: bool):
    code = 200 if successful else 404

    return (
        {"found": successful, "id": chip_id},
        code,
        {"Content-Type": "application/json"},
    )


@app.route("/")
async def hello(req):
    return HTML_CONTENT, 200, {"Content-Type": "text/html"}


@app.route("/read", methods=["GET"])
async def read_single_chip(req):
    timeout = get_client_timeout(req)

    led.blink("green", "+-", 100, continuous=True)
    chip_id_result = reader.read_single_chip(timeout_ms=timeout * 1000)
    led.stop_blink()
    logger.debug(f"Read returned with data {chip_id_result}")

    if chip_id_result is None:
        led.red_on(2000)
        return get_response(None, False)

    return get_response(chip_id_result, True)


@app.route("/read/chip/<chip_id>", methods=["GET"])
async def wait_for_chip(req, chip_id):
    timeout = get_client_timeout(req)

    led.blink("green", "+-", 100, continuous=True)
    chip_id_result = reader.detect_chip_with_id(
        target_id=chip_id, timeout_ms=timeout * 1000
    )
    led.stop_blink()
    logger.debug(f"Read returned with data {chip_id_result}")

    if chip_id_result is None:
        led.red_on(2000)
        return get_response(chip_id, False)

    return get_response(chip_id_result, True)


@app.route("/read/stream", methods=["GET"])
async def read_continuous(req):
    timeout = get_client_timeout(req)

    def continuous_chip_reader():
        for id in reader.read_continuously(timeout_ms=timeout * 1000):
            yield f'{{"found": True, "id": {id}}}\n'

    return continuous_chip_reader()


def start_rfid_api_webserver():
    logger.info("Starting webserver at {}:{}".format(CONF.HOST, CONF.PORT))

    # Signal that the webserver is booting...
    led.blink("red", "+-+---", time_ms=200, n_times=2)

    app.run(host=CONF.HOST, port=CONF.PORT, debug=CONF.MICRODOT_DEBUG)
