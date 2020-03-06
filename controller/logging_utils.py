import logging
import os
from logging.handlers import RotatingFileHandler

os.makedirs('./.logs', exist_ok=True)

fh = RotatingFileHandler('./.logs/log', mode='a', maxBytes=5*1024*1024, backupCount=2)
logging.basicConfig(format='[%(name)s %(levelname)s: %(asctime)s] %(message)s', 
                    handlers=[fh], level=logging.INFO)