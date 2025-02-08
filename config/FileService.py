import os
import base64


class _FileService:
    DIR: str = 'car'

    def uploadFile(self, payload: object) -> None:
        name: str = payload['name']
        data: any = base64.b64decode(payload['data'])
        path: str = os.path.join(self.DIR, name)

        with open(path, 'wb') as file:
            file.write(data)

    def downloadFile(self, name: str) -> bytes | None:
        path: str = os.path.join(self.DIR, name)

        if os.path.exists(path):
            with open(path, 'rb') as file:
                return file.read()

        return None

    def getFiles(self) -> list[str]:
        return [file for file in os.listdir(self.DIR) if file != '__pycache__']

    def deleteFile(self, name: str) -> None:
        path: str = os.path.join(self.DIR, name)

        if os.path.exists(path):
            os.remove(path)


fileService: _FileService = _FileService()
