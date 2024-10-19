import os
import unittest
from skeleton_xml.ConfigService import ConfigService


class ValidateConfigsTest(unittest.TestCase):
    def testValidateCarRemoteConfig(self) -> None:
        self.__createConfigService('../config.car_remote.xml').validate(
            algorithmName='MANUAL',
            commandName='FORWARD',
            request={
                'speed': 60,
                'duration': 0.5,
            },
        )

    def testValidateCarStubConfig(self) -> None:
        self.__createConfigService('../config.car_stub.xml').validate(
            algorithmName='MANUAL',
            commandName='FORWARD',
            request={
                'speed': 60,
                'duration': 0.5,
            },
        )

    def __createConfigService(self, file: str) -> ConfigService:
        path: str = os.path.dirname(os.path.realpath(__file__)) + '/' + file

        return ConfigService(config=path)
