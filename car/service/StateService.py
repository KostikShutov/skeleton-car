from car.service.AngleService import angleService
from car.service.SpeedService import speedService
from car.service.GpsService import gpsService


class _StateService:
    def state(self) -> dict:
        return {
            'ok': True,
            'minAngle': angleService.getMinAngle(),
            'maxAngle': angleService.getMaxAngle(),
            'currentAngle': angleService.getCurrentAngle(),
            'minSpeed': speedService.getMinSpeed(),
            'maxSpeed': speedService.getMaxSpeed(),
            'currentSpeed': speedService.getCurrentSpeed(),
            'latitude': gpsService.getLatitude(),
            'longitude': gpsService.getLongitude(),
        }


stateService: _StateService = _StateService()
