import logging

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s][%(levelname)s][%(message)s]",
    datefmt="%Y-%m-%d %H:%m:%s",
    handlers=[
        logging.StreamHandler(),
    ]
)
logger = logging.getLogger(__name__)