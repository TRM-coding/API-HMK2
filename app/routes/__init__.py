from flask import Blueprint

from .offers     import offers_bp
from .tasks      import tasks_bp
from .stats_logs import stats_logs_bp

__all__ = ['offers_bp', 'tasks_bp', 'stats_logs_bp']
