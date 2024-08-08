import logging


class CustomFormatter(logging.Formatter):
    PURPLE = "\033[35m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    RESET = "\033[0m"

    FORMAT = "%(asctime)s: %(name)s: %(levelname)s: %(message)s"

    def __init__(self, fmt=FORMAT):
        super().__init__(fmt)

    def format(self, record):
        levelname = record.levelname
        if levelname == "EXCEPTION":
            record.levelname = f"{self.PURPLE}{levelname}{self.RESET}"
            record.msg = f"{self.PURPLE}{record.msg}{self.RESET}"
        elif levelname == "INFO":
            record.levelname = f"{self.YELLOW}{levelname}{self.RESET}"
            record.msg = f"{self.YELLOW}{record.msg}{self.RESET}"
        elif levelname == "DEBUG":
            record.levelname = f"{self.BLUE}{levelname}{self.RESET}"
        return super().format(record)
