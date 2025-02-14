import json
import socketio
import logging
from celery import current_task
from executor.celery import app
from utils.Env import env
from skeleton_xml.ConfigService import ConfigService
from config.OverrideService import overrideService

sio = socketio.RedisManager('redis://%s:%s' % (env['REDIS_HOST'], env['REDIS_PORT']), write_only=True)


@app.task
def commandTask(body: str) -> None:
    payload: dict = json.loads(body)
    logging.info('Received command: %s' % payload)
    commandName: str = payload.pop('commandName')
    commandId: str = current_task.request.id

    try:
        config: str = overrideService.getConfig()
        sio.emit('updateCommand', data=json.dumps({
            'id': commandId,
            'status': 'started',
        }))
        ConfigService(config=config).executeCommand(commandName=commandName, request=payload)
        sio.emit('updateCommand', data=json.dumps({
            'id': commandId,
            'status': 'succeeded',
        }))
    except Exception as e:
        logging.error('Failed to execute command: %s' % e)
        sio.emit('updateCommand', data=json.dumps({
            'id': commandId,
            'status': 'failed',
        }))
