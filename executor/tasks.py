import json
import socketio
import logging
from celery import current_task
from car.StateService import stateService
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
        ConfigService(config=config).executeCommand(commandName=commandName, request=payload)
        sio.emit('getCommand', data=json.dumps({
            'id': commandId,
            'status': 'success',
            'state': stateService.state(),
        }))
    except Exception:
        sio.emit('getCommand', data=json.dumps({
            'id': commandId,
            'status': 'error',
            'state': stateService.state(),
        }))
