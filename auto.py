#!/usr/bin/python

import cv2
import time
import logging
from skeleton_xml.ConfigService import ConfigService
from config.OverrideService import overrideService
from executor.CommandCoordinator import CommandCoordinator
from utils.DeadHand import isDead
from utils.Logger import configureLogger

configureLogger()
commandCoordinator: CommandCoordinator = CommandCoordinator()
cap = None
lastTime: float | None = None

while True:
    if isDead():
        if cap is None:
            cap = cv2.VideoCapture('http://192.168.3.11:8080/?action=stream')

        try:
            config: str = overrideService.getConfig()
            payloads: list[dict] = ConfigService(config=config).executeAlgorithm(
                algorithmName='AUTO',
                entry={
                    'cap': cap,
                    'lastTime': lastTime,
                },
            )
            lastTime: float = lastTime if payloads == [] else time.time()
            logging.info('Commands: %s' % payloads)
            commandCoordinator.pushCommands(payloads)
        except Exception as e:
            logging.error('Failed to execute auto algorithm: ', e)
    else:
        cap.release()
        cv2.destroyAllWindows()
        cap = None
