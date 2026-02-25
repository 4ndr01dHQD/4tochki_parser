from logging import (
    Logger,
    getLogger,
    INFO,
    basicConfig,
)

import structlog

from config import BASE_DIR

#TODO изучить ротацию логово

def get_logger(name: str) -> Logger:
    logger = getLogger(name)
    basicConfig(
        filename=f"{BASE_DIR}/logs/{name}.log",
        filemode='a',
        format="%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s",
        datefmt="%H:%M:%S",
        level=INFO,
    )

    log = structlog.wrap_logger(
        logger,
        processors=[
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.add_log_level,
            structlog.processors.JSONRenderer(
                indent=4, sort_keys=True, ensure_ascii=False
            ),
        ],
    )
    return log


logger = get_logger(name='fortochki-parser')
logger.info("Logging initialized successfully")