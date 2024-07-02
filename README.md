# skeleton-car

## Другие компоненты общей системы

[Webview for car control](https://github.com/KostikShutov/skeleton-webview)

[Autonomous command generator](https://github.com/KostikShutov/skeleton-autonomous)

## Docker

Поднять docker контейнеры

 ```bash
make d-up
 ```

Остановить docker контейнеры

```bash
make d-down
```

Перезапустить docker контейнеры

```bash
make d-restart
```

Зайти в контейнер с Python

```bash
make d-python
```

## Запуск

Поднять сервер (<http://localhost:2001>):

```bash
make server
```

Запустить worker:

```bash
make worker
```

## Raspberry

Проверить i2c на raspberry pi:

```bash
python i2c.py
```

Запустить камеру:

```bash
cd mjpg-streamer/mjpg-streamer-experimental
bash start.sh
```
