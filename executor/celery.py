from utils.Env import env
from celery import Celery

host: str = env['RABBITMQ_HOST']

app = Celery('commands',
             broker=host,
             backend='rpc://',
             include=['executor.tasks'])

app.conf.update(
    result_expires=3600,
)

if __name__ == '__main__':
    app.start()
