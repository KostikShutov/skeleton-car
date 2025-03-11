#!/usr/bin/python

import socketio
from executor.CommandCoordinator import CommandCoordinator
from utils.Env import env

sio = socketio.RedisManager('redis://%s:%s' % (env['REDIS_HOST'], env['REDIS_PORT']), write_only=True)
commandCoordinator: CommandCoordinator = CommandCoordinator(sio=sio)

for _ in range(100):
    commandCoordinator.pushCommand(
        payload={
            'commandName': 'FORWARD',
            'speed': 60,
            'duration': 1.0,
        },
        algorithmName='AUTO',
    )
