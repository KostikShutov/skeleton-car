import os
import xml.etree.ElementTree as ET
from utils.Env import env


class _OverrideService:
    def getConfig(self) -> str:
        defaultConfig: str = self.__getDefaultConfig()
        overrideConfig: str = self.__getOverrideConfig(defaultConfig)

        if os.path.isfile(overrideConfig):
            return overrideConfig

        return defaultConfig

    def uploadConfig(self, xml: str) -> None:
        defaultConfig: str = self.__getDefaultConfig()
        overrideConfig: str = self.__getOverrideConfig(defaultConfig)

        if xml.strip() == '':
            os.remove(overrideConfig)

            return

        try:
            ET.fromstring(xml)
        except ET.ParseError:
            return

        with open(overrideConfig, 'w', encoding='utf-8') as file:
            file.write(xml)

    def __getDefaultConfig(self) -> str:
        return env['CONFIG']

    def __getOverrideConfig(self, defaultConfig: str) -> str:
        return defaultConfig.replace('.xml', '.override.xml')


overrideService: _OverrideService = _OverrideService()
