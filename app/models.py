from .extensions import db
from datetime import datetime
import enum

class ImportExportType(enum.Enum):
    IMPORT = 'IMPORT'
    EXPORT = 'EXPORT'

class TaskStatus(enum.Enum):
    PENDING = 'PENDING'
    RUNNING = 'RUNNING'
    SUCCESS = 'SUCCESS'
    FAIL = 'FAIL'

class Offer(db.Model):
    __tablename__ = 'offers'
    id           = db.Column(db.Integer, primary_key=True, autoincrement=True)
    company_name = db.Column(db.String(100), nullable=False)
    position     = db.Column(db.String(100), nullable=False)
    salary_min   = db.Column(db.Numeric(12,2))
    salary_max   = db.Column(db.Numeric(12,2))
    currency     = db.Column(db.String(3), nullable=False, default='CNY')
    location     = db.Column(db.String(100))
    description  = db.Column(db.Text)
    tags         = db.Column(db.JSON, default=list)
    created_at   = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at   = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class ImportExportTask(db.Model):
    __tablename__ = 'import_export_tasks'
    task_id    = db.Column(db.String(36), primary_key=True)
    type       = db.Column(db.Enum(ImportExportType), nullable=False)
    status     = db.Column(db.Enum(TaskStatus), nullable=False)
    params     = db.Column(db.JSON)
    result_url = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class StatsLog(db.Model):
    __tablename__ = 'stats_logs'
    log_id      = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date        = db.Column(db.Date, nullable=False, unique=True)
    offer_count = db.Column(db.Integer, nullable=False)
    avg_salary  = db.Column(db.Numeric(12,2))
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)
