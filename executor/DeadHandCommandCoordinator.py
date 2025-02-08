from executor.CommandCoordinator import CommandCoordinator
from utils.DeadHand import iAmAlive


class DeadHandCommandCoordinator(CommandCoordinator):
    def __init__(self) -> None:
        iAmAlive()

    def pushCommands(self, payloads: list[object]) -> list[str]:
        iAmAlive()

        return super().pushCommands(payloads)

    def pushCommand(self, payload: object) -> str:
        iAmAlive()

        return super().pushCommand(payload)

    def revokeCommand(self, commandId: str) -> None:
        iAmAlive()
        super().revokeCommand(commandId)

    def getCommandStatus(self, commandId: str) -> str:
        iAmAlive()

        return super().getCommandStatus(commandId)

    def purgeCommands(self) -> None:
        iAmAlive()
        super().purgeCommands()
