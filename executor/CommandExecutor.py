import logging
from skeleton_xml.ConfigService import ConfigService
from config.OverrideService import overrideService


class CommandExecutor:
    def __init__(self) -> None:
        self.configService: ConfigService = ConfigService(config=overrideService.getConfig())

    def execute(self, payload: dict) -> None:
        logging.info('Received command: %s' % payload)
        commandName: str = payload.pop('commandName')
        self.configService.executeCommand(commandName=commandName, request=payload)
