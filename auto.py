#!/usr/bin/python

import time
import logging
from skeleton_xml.ConfigService import ConfigService
from config.OverrideService import overrideService
from utils.DeadHand import isDead

configService: ConfigService = ConfigService(config=overrideService.getConfig())

while True:
    if isDead():
        logging.info('Executed auto algorithm')
        configService.executeAlgorithm(algorithmName='AUTO')

    time.sleep(1)
