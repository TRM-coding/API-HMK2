from .extensions import celery, db
from .models import ImportExportTask, TaskStatus, ImportExportType, Offer  # add Offer, ImportExportType
from flask import current_app, has_app_context
import os, shutil, time, csv, json  # add csv, json

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

            # 新增：如果是 IMPORT 类型，解析 CSV 并写入 Offer 表
            if t.type == ImportExportType.IMPORT:
                with open(dest, newline='', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    offers = []
                    for row in reader:
                        raw_tags = row.get('tags', '[]').strip()
                        if not raw_tags:
                            tags = []
                        else:
                            # If raw_tags does not start with '[' assume extra quotes are present.
                            if not raw_tags.startswith('['):
                                raw_tags = raw_tags.strip('"')
                            try:
                                tags = json.loads(raw_tags)
                            except json.JSONDecodeError:
                                # As a fallback, decode escape sequences and try again.
                                try:
                                    raw_tags_decoded = raw_tags.encode('utf-8').decode('unicode_escape')
                                    tags = json.loads(raw_tags_decoded)
                                except Exception:
                                    tags = []
                        offers.append(Offer(
                            company_name=row['company_name'],
                            position=row['position'],
                            salary_min=row.get('salary_min') or None,
                            salary_max=row.get('salary_max') or None,
                            currency=row.get('currency') or None,
                            location=row.get('location') or None,
                            description=row.get('description') or None,
                            tags=tags
                        ))
                    if offers:
                        db.session.add_all(offers)
            t.status = TaskStatus.SUCCESS
        else:
            t.status = TaskStatus.FAIL

        db.session.commit()
