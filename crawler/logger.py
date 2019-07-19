import logging
from datetime import datetime

class Logger:
    debug_level_list = [logging.DEBUG, logging.INFO, logging.ERROR]

    def __init__(self, platform_name, debug_level):
        self.logger = None
        self.platform_name = str(platform_name)
        self.debug_level = self.debug_level_list[int(debug_level)]

    def set_logger(self):
        file_name = "{platform_name}_{datetime}.{extension}".format(
            platform_name=self.platform_name,
            datetime=str(datetime.now().strftime("%Y\%m\%d_%H:%M:%S")),
            extension="log"
        )
        self.logger = logging.basicConfig(
            filename=file_name,
            level=self.debug_level
        )
        self.logger = logging.getLogger(self.platform_name)
        self.logger.setLevel(self.debug_level)
        formatter = logging.Formatter('[%(funcName)s/%(filename)s:%(lineno)s] %(asctime)s > %(message)s')
        # https://docs.python.org/ko/3/library/logging.html#logrecord-attributes
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        self.logger.addHandler(stream_handler)

        return self.logger
