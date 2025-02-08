import gpsd


class _GpsService:
    def __init__(self) -> None:
        self.error: bool = False

        try:
            gpsd.connect(host='localhost')
        except ConnectionRefusedError:
            self.error: bool = True

    def getLatitude(self) -> float:
        if self.error:
            return 43.114422076554

        return gpsd.get_current().lat

    def getLongitude(self) -> float:
        if self.error:
            return 131.898333122618

        return gpsd.get_current().lon


gpsService: _GpsService = _GpsService()
