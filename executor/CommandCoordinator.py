import json
from socketio import RedisManager
from executor.celery import app
from executor.tasks import commandTask


class CommandCoordinator:
    def __init__(self, sio: RedisManager):
        self.sio: RedisManager = sio

    def pushCommands(self, payloads: list[object], algorithmName: str) -> list[str]:
        tasks: list[str] = []

        for payload in payloads:
            task: str = self.pushCommand(payload, algorithmName)
            tasks.append(task)

        return tasks

    def pushCommand(self, payload: object, algorithmName: str) -> str:
        body: str = json.dumps(payload)
        result = commandTask.delay(body=body)
        commandId: str = result.task_id
        self.sio.emit('addCommand', data=json.dumps({
            'id': commandId,
            'status': 'received',
            'algorithmName': algorithmName,
            'commandName': payload['commandName'],
        }))

        return commandId

    def revokeCommand(self, commandId: str) -> None:
        app.control.revoke(commandId, terminate=True)
        self.sio.emit('updateCommand', data=json.dumps({
            'id': commandId,
            'status': 'revoked',
        }))

    def getCommandStatus(self, commandId: str) -> str:
        return app.AsyncResult(commandId).state

    def purgeCommands(self) -> None:
        i = app.control.inspect()
        self.__revokeJobs(i.active())
        self.__revokeJobs(i.scheduled())
        self.__revokeJobs(i.reserved())
        self.__revokeJobs(i.registered())
        app.control.purge()
        self.sio.emit('purgeCommands', data=json.dumps({}))

    def __revokeJobs(self, jobs: list | None) -> None:
        if jobs is None:
            return

        for hostname in jobs:
            tasks = jobs[hostname]

            for task in tasks:
                self.revokeCommand(task['id'])
