import os
from flask import Flask, jsonify
from .config import config_by_name
from .extensions import db, migrate
from .routes import offers_bp, tasks_bp, stats_logs_bp

def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    # init extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # 配置 Celery，避免整体 update 导致新旧配置混用
    from .extensions import celery
    # 只单独设置必要的三项
    celery.conf.broker_url         = app.config.get('CELERY_BROKER_URL')
    celery.conf.result_backend     = app.config.get('CELERY_RESULT_BACKEND')
    celery.conf.task_always_eager  = app.config.get('CELERY_TASK_ALWAYS_EAGER', False)

    # register blueprints
    app.register_blueprint(offers_bp,   url_prefix='/offers')
    app.register_blueprint(tasks_bp,    url_prefix='/tasks')
    app.register_blueprint(stats_logs_bp, url_prefix='/stats_logs')

    # Add error handler to return JSON for 404 errors.
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": "not found"}), 404

    return app
