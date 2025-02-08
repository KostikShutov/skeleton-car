#!/usr/bin/python

import time
import logging
from skeleton_xml.ConfigService import ConfigService
from config.OverrideService import overrideService
from utils.DeadHand import isDead

while True:
    if isDead():
        logging.info('Executed auto algorithm')

        try:
            config: str = overrideService.getConfig()
            ConfigService(config=config).executeAlgorithm(algorithmName='AUTO')
        except Exception:
            pass

    time.sleep(1)
