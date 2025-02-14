#!/usr/bin/python

import json
import eventlet
import socketio
from car.StateService import stateService
from config.OverrideService import overrideService
from config.FileService import fileService
from executor.DeadHandCommandCoordinator import DeadHandCommandCoordinator
from utils.Env import env

eventlet.monkey_patch()
mgr = socketio.RedisManager('redis://%s:%s' % (env['REDIS_HOST'], env['REDIS_PORT']))
sio = socketio.Server(cors_allowed_origins='*', client_manager=mgr)
app = socketio.WSGIApp(sio)
configToken: str = env['TOKEN']
commandCoordinator: DeadHandCommandCoordinator = DeadHandCommandCoordinator(sio=mgr)


@sio.event
def connect(sid: str, environ: str, auth: dict) -> None:
    requestToken: str = auth['token']

    if requestToken != configToken:
        raise ConnectionRefusedError('Authentication failed')

    sio.save_session(sid, {'token': requestToken})
    print('Connect (%s)' % sid)


@sio.event
def disconnect(sid: str) -> None:
    print('Disconnect (%s)' % sid)


@sio.event
def state(sid: str) -> str:
    return json.dumps(stateService.state())


@sio.event
def pushCommands(sid: str, payloads: list) -> str:
    return json.dumps(commandCoordinator.pushCommands(payloads))


@sio.event
def pushCommand(sid: str, payload: object) -> str:
    return str(commandCoordinator.pushCommand(payload))


@sio.event
def revokeCommand(sid: str, commandId: str) -> None:
    commandCoordinator.revokeCommand(commandId)


@sio.event
def statusCommand(sid: str, commandId: str) -> str:
    return commandCoordinator.getCommandStatus(commandId)


@sio.event
def purgeCommands(sid: str) -> None:
    commandCoordinator.purgeCommands()


@sio.event
def getConfig(sid: str) -> str:
    with open(overrideService.getConfig(), 'r', encoding='utf-8') as file:
        return json.dumps({'xml': file.read()})


@sio.event
def uploadConfig(sid: str, payload: object) -> None:
    overrideService.uploadConfig(payload['xml'])


@sio.event
def uploadFile(sid: str, payload: object) -> None:
    fileService.uploadFile(payload)


@sio.event
def downloadFile(sid: str, filename: str) -> bytes | None:
    return fileService.downloadFile(filename)


@sio.event
def getFiles(sid: str) -> list[str]:
    return fileService.getFiles()


@sio.event
def deleteFile(sid: str, filename: str) -> None:
    fileService.deleteFile(filename)


if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)
