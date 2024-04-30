import logging
from skeleton_xml.ConfigService import ConfigService


class CommandExecutor:
    def __init__(self, config: str) -> None:
        self.configService: ConfigService = ConfigService(config=config)

    def execute(self, payload: dict) -> None:
        logging.info('Received command: %s' % payload)
        commandName: str = payload.pop('name')
        self.configService.execute(commandName=commandName, request=payload)
