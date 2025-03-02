import os
import tempfile
import xml.etree.ElementTree as ET
from utils.Env import env
from skeleton_xml.ConfigService import ConfigService


class _OverrideService:
    def getConfig(self) -> str:
        defaultConfig: str = self.__getDefaultConfig()
        overrideConfig: str = self.__getOverrideConfig(defaultConfig)

        if os.path.isfile(overrideConfig):
            return overrideConfig

        return defaultConfig

    def uploadConfig(self, xml: str) -> str:
        defaultConfig: str = self.__getDefaultConfig()
        overrideConfig: str = self.__getOverrideConfig(defaultConfig)

        if xml.strip() == '':
            os.remove(overrideConfig)

            return 'Config has been reset'

        try:
            ET.fromstring(xml)
        except Exception as e:
            return 'Invalid xml: ' + str(e)

        tmp = tempfile.NamedTemporaryFile(mode='w', encoding='utf-8')

        try:
            tmp.write(xml)

            try:
                ConfigService(config=tmp.name)
            except Exception as e:
                return 'Invalid config: ' + str(e)

            with open(overrideConfig, mode='w', encoding='utf-8') as file:
                file.write(xml)
        finally:
            tmp.close()

        return 'Config is loaded'

    def __getDefaultConfig(self) -> str:
        return env['CONFIG']

    def __getOverrideConfig(self, defaultConfig: str) -> str:
        return defaultConfig.replace('.xml', '.override.xml')


overrideService: _OverrideService = _OverrideService()
