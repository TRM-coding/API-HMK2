from app import create_app
from app.extensions import celery
import os

flask_app = create_app(os.getenv('FLASK_ENV', 'development'))
celery.conf.update(flask_app.config)
celery.conf.broker_url = flask_app.config['CELERY_BROKER_URL']
celery.autodiscover_tasks(['app.tasks'])

app = celery

if __name__ == '__main__':
    app.start()
