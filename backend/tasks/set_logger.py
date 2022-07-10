import logging
import os

root_logger = logging.getLogger()
handler = root_logger.handlers[0]

instance_name = os.environ.get("INSTANCE_NAME", "")
root_logger.handlers[0]._JournaldLogHandler__identifier = f"Cronjobs[{instance_name}]"
