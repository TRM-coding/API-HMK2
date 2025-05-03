from flask import Blueprint, request, jsonify, current_app, send_file, abort
from werkzeug.utils import secure_filename
from uuid import uuid4
import os

from ..extensions import db
from ..models import ImportExportTask, ImportExportType, TaskStatus
from ..utils import to_dict
from app.tasks import process_import_export

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('', methods=['GET'])
def list_tasks():
    tasks = ImportExportTask.query.all()
    return jsonify([to_dict(t) for t in tasks])

@tasks_bp.route('/<string:task_id>', methods=['GET'])
def get_task(task_id):
    t = db.session.get(ImportExportTask, task_id)
    if t is None:
        abort(404)
    return jsonify(to_dict(t))

@tasks_bp.route('', methods=['POST'])
def create_task():
    # 新增：处理 application/json 请求，允许直接按 test 用例提交 JSON 创建任务
    if request.is_json:
        data = request.get_json()
        t = ImportExportTask(
            task_id=data['task_id'],
            type=ImportExportType(data['type']),
            status=TaskStatus(data['status']),
            params=data.get('params')
        )
        db.session.add(t)
        db.session.commit()
        return jsonify(to_dict(t)), 201

    if 'file' not in request.files:
        return jsonify({'error': 'file required'}), 400
    f = request.files['file']
    fname = secure_filename(f.filename)
    os.makedirs(current_app.config['UPLOAD_FOLDER'], exist_ok=True)
    path = os.path.join(current_app.config['UPLOAD_FOLDER'], fname)
    f.save(path)

    task_id = str(uuid4())
    t = ImportExportTask(
        task_id=task_id,
        type=ImportExportType(request.form.get('type', 'IMPORT')),
        status=TaskStatus.PENDING,
        params={'file_path': path}
    )
    db.session.add(t)
    db.session.commit()

    # 根据 EAGER 配置，同步运行或异步调度
    if current_app.config.get('CELERY_TASK_ALWAYS_EAGER'):
        process_import_export.run(t.task_id)
    else:
        process_import_export.delay(t.task_id)

    # 同步执行/异步调度后刷新，拿到最新状态和 result_url
    db.session.refresh(t)
    return jsonify(to_dict(t)), 201

@tasks_bp.route('/<string:task_id>', methods=['PUT'])
def update_task(task_id):
    t = db.session.get(ImportExportTask, task_id)
    if t is None:
        abort(404)

    data = request.get_json()
    for k, v in data.items():
        if hasattr(t, k):
            setattr(t, k, v)
    db.session.commit()
    return jsonify(to_dict(t))

@tasks_bp.route('/<string:task_id>', methods=['DELETE'])
def delete_task(task_id):
    t = db.session.get(ImportExportTask, task_id)
    if t is None:
        abort(404)

    db.session.delete(t)
    db.session.commit()
    return '', 204

@tasks_bp.route('/<string:task_id>/download', methods=['GET'])
def download_result(task_id):
    t = db.session.get(ImportExportTask, task_id)
    if t is None:
        abort(404)

    if t.status != TaskStatus.SUCCESS or not t.result_url:
        return jsonify({'error': 'result not ready'}), 404

    return send_file(t.result_url, as_attachment=True)
