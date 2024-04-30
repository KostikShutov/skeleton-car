import time


def microSleep(duration: float) -> None:
    timer = time.time()

    while timer + duration > time.time():
        pass


def singleton(class_) -> object:
    instances: dict[str, object] = {}

    def getinstance(*args, **kwargs) -> object:
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)

        return instances[class_]

    return getinstance
