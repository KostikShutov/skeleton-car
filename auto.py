#!/usr/bin/python

import time
import logging
from skeleton_xml.ConfigService import ConfigService
from config.OverrideService import overrideService
from executor.CommandCoordinator import CommandCoordinator
from utils.DeadHand import isDead
from utils.Logger import configureLogger

configureLogger()
commandCoordinator: CommandCoordinator = CommandCoordinator()

while True:
    if isDead():
        logging.info('Executed auto algorithm')

        try:
            config: str = overrideService.getConfig()
            payloads: list[dict] = ConfigService(config=config).executeAlgorithm(algorithmName='AUTO')
            commandCoordinator.pushCommands(payloads)
        except Exception as e:
            logging.error('Failed to execute auto algorithm: ', e)

    time.sleep(1)
