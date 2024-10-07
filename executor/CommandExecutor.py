import logging
from skeleton_xml.ConfigService import ConfigService


class CommandExecutor:
    def __init__(self, config: str) -> None:
        self.configService: ConfigService = ConfigService(config=config)

    def execute(self, payload: dict) -> None:
        logging.info('Received command: %s' % payload)
        algorithmName: str = payload.pop('algorithmName')
        commandName: str = payload.pop('commandName')
        self.configService.execute(algorithmName=algorithmName, commandName=commandName, request=payload)
