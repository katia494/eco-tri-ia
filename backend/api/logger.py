import logging
import sys
from datetime import datetime

def setup_logger(name: str = "eco_tri") -> logging.Logger:
    """
    Configure et retourne un logger pour l'application.
    
    Args:
        name: Nom du logger
    
    Returns:
        logging.Logger: Logger configuré
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Format des messages
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Affichage dans la console
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(console_handler)

    return logger

# Logger global de l'application
logger = setup_logger()