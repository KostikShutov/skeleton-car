#!/usr/bin/python

import time
import logging
import socketio
from skeleton_xml.ConfigService import ConfigService
from config.OverrideService import overrideService
from executor.CommandCoordinator import CommandCoordinator
from utils.Env import env
from utils.DeadHand import isDead
from utils.Logger import configureLogger

configureLogger()
sio = socketio.RedisManager('redis://%s:%s' % (env['REDIS_HOST'], env['REDIS_PORT']), write_only=True)
commandCoordinator: CommandCoordinator = CommandCoordinator(sio=sio)
lastTime: float | None = None

while True:
    if isDead():
        try:
            config: str = overrideService.getConfig()
            payloads: list[dict] = ConfigService(config=config).executeAlgorithm(
                algorithmName='AUTO',
                entry={
                    'lastTime': lastTime,
                    'needShowFrames': str(env['DEBUG_AUTO_ALGORITHM']) == '1',
                },
            )

            if payloads:
                lastTime: float = time.time()
                logging.info('Commands: %s' % payloads)

            commandCoordinator.pushCommands(payloads, 'AUTO')
        except Exception as e:
            logging.error('Failed to execute auto algorithm: %s' % e)
