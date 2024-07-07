import utime


class Logger:
    def __init__(self, log_level="INFO"):
        self.log_levels = {
            "DEBUG": 0,
            "INFO": 1,
            "WARNING": 2,
            "ERROR": 3,
            "CRITICAL": 4,
        }
        self.current_level = log_level  # Default log level
        self.enabled_levels = {level: True for level in self.log_levels}

    def set_level(self, level: str):
        if level in self.log_levels:
            self.current_level = level
        else:
            raise ValueError(f"Invalid log level '{level}'")

    def enable_level(self, level):
        if level in self.log_levels:
            self.enabled_levels[level] = True
        else:
            raise ValueError(f"Invalid log level '{level}'")

    def disable_level(self, level):
        if level in self.log_levels:
            self.enabled_levels[level] = False
        else:
            raise ValueError(f"Invalid log level '{level}'")

    def log(self, level, message):
        if level in self.log_levels:
            if (
                self.log_levels[level] >= self.log_levels[self.current_level]
                and self.enabled_levels[level]
            ):
                timestamp = utime.localtime()
                timestamp_str = "{:04}-{:02}-{:02} {:02}:{:02}:{:02}".format(
                    timestamp[0],
                    timestamp[1],
                    timestamp[2],
                    timestamp[3],
                    timestamp[4],
                    timestamp[5],
                )
                print("[{}] [{}] {}".format(timestamp_str, level, message))

    def debug(self, message):
        self.log("DEBUG", message)

    def info(self, message):
        self.log("INFO", message)

    def warning(self, message):
        self.log("WARNING", message)

    def error(self, message):
        self.log("ERROR", message)

    def critical(self, message):
        self.log("CRITICAL", message)
