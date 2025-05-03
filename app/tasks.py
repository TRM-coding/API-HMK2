from .extensions import celery, db
from .models import ImportExportTask, TaskStatus
from flask import current_app, has_app_context
import os, shutil, time

@celery.task(name='app.tasks.process_import_export')
def process_import_export(task_id):
    # 使用现有 Flask 上下文（同步执行时）或手动创建（真正 worker）
    if has_app_context():
        ctx = current_app.app_context()
    else:
        from app import create_app
        app = create_app(os.getenv('FLASK_ENV', 'development'))
        ctx = app.app_context()

    with ctx:
        t = db.session.get(ImportExportTask, task_id)
        if t is None:
            # 如果不存在该任务，则明确失败
            raise LookupError(f"ImportExportTask id={task_id} not found")
        t.status = TaskStatus.RUNNING
        db.session.commit()

        params = t.params or {}
        src = params.get('file_path')
        if src and os.path.exists(src):
            # 模拟耗时处理
            time.sleep(2)
            os.makedirs(current_app.config['RESULT_FOLDER'], exist_ok=True)
            dest = os.path.join(
                current_app.config['RESULT_FOLDER'],
                f"{task_id}_{os.path.basename(src)}"
            )
            shutil.copy(src, dest)
            t.result_url = dest
            t.status = TaskStatus.SUCCESS
        else:
            t.status = TaskStatus.FAIL

        db.session.commit()
