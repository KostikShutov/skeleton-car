from socketio import RedisManager
from executor.CommandCoordinator import CommandCoordinator
from utils.DeadHand import iAmAlive


class DeadHandCommandCoordinator(CommandCoordinator):
    def __init__(self, sio: RedisManager):
        iAmAlive()
        super().__init__(sio)

    def pushCommands(self, payloads: list[object], algorithmName: str) -> list[str]:
        iAmAlive()

        return super().pushCommands(payloads, algorithmName)

    def pushCommand(self, payload: object, algorithmName: str) -> str:
        iAmAlive()

        return super().pushCommand(payload, algorithmName)

    def revokeCommand(self, commandId: str) -> None:
        iAmAlive()
        super().revokeCommand(commandId)

    def getCommandStatus(self, commandId: str) -> str:
        iAmAlive()

        return super().getCommandStatus(commandId)

    def purgeCommands(self) -> None:
        iAmAlive()
        super().purgeCommands()
