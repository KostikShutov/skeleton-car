import json
import socketio
from celery import current_task
from car.service.StateService import stateService
from executor.CommandExecutor import CommandExecutor
from executor.celery import app
from utils.Env import env

sio = socketio.RedisManager('redis://%s:%s' % (env['REDIS_HOST'], env['REDIS_PORT']), write_only=True)


@app.task
def commandTask(body: str) -> None:
    payload: dict = json.loads(body)
    commandId: str = current_task.request.id

    try:
        CommandExecutor().execute(payload)
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
