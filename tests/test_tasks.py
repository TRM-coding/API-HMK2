import io
import os
import pytest
from app import create_app, db
from app.models import ImportExportTask, ImportExportType, TaskStatus

@pytest.fixture
def app():
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        # 插入模拟数据
        from app.models import ImportExportTask, ImportExportType, TaskStatus
        db.session.add_all([
            ImportExportTask(task_id='a1b2c3d4-e5f6-7a8b-9c0d-e1f2a3b4c5d6', type=ImportExportType.IMPORT, status=TaskStatus.PENDING, params={'source':'/uploads/data1.csv'}),
            ImportExportTask(task_id='f1e2d3c4-b5a6-7c8d-9e0f-a1b2c3d4e5f6', type=ImportExportType.EXPORT, status=TaskStatus.RUNNING, params={'destination':'/exports/report1.xlsx'}),
            ImportExportTask(task_id='11112222-3333-4444-5555-666677778888', type=ImportExportType.EXPORT, status=TaskStatus.SUCCESS, params={'destination':'/exports/report2.xlsx'}, result_url='/downloads/report2.xlsx'),
            ImportExportTask(task_id='9999aaaa-bbbb-cccc-dddd-eeeeffff0000', type=ImportExportType.IMPORT, status=TaskStatus.FAIL,    params={'source':'/uploads/data2.csv','error':'文件格式错误'}),
        ])
        db.session.commit()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

# 新增：在测试时覆盖上传/下载目录并让 Celery 任务同步执行
@pytest.fixture(autouse=True)
def override_paths(tmp_path, app):
    app.config['UPLOAD_FOLDER'] = str(tmp_path / "uploads")
    app.config['RESULT_FOLDER'] = str(tmp_path / "results")
    app.config['CELERY_TASK_ALWAYS_EAGER'] = True

def test_create_and_get_task(client):
    payload = {
        "task_id": "123e4567-e89b-12d3-a456-426614174000",
        "type": "IMPORT",
        "status": "PENDING"
    }
    rv = client.post('/tasks', json=payload)
    assert rv.status_code == 201
    data = rv.get_json()
    assert data['task_id'] == payload['task_id']
    # fetch
    rv2 = client.get(f"/tasks/{payload['task_id']}")
    assert rv2.status_code == 200
    obj2 = rv2.get_json()
    assert obj2['status'] == "PENDING"

# 新增：测试文件异步导入并下载结果
def test_import_export_file(client):
    content = b"hello world"
    data = {
        'file': (io.BytesIO(content), 'hello.txt'),
        'type': 'IMPORT'
    }
    rv = client.post('/tasks', data=data, content_type='multipart/form-data')
    assert rv.status_code == 201
    obj = rv.get_json()
    assert obj['status'] == 'SUCCESS'
    assert obj.get('result_url')
    task_id = obj['task_id']

    # 测试下载接口
    rv2 = client.get(f"/tasks/{task_id}/download")
    assert rv2.status_code == 200
    assert rv2.data == content
    assert 'attachment' in rv2.headers.get('Content-Disposition', '')

def test_list_tasks(client):
    rv = client.get('/tasks')
    assert rv.status_code == 200
    data = rv.get_json()
    assert isinstance(data, list) and len(data) == 4
    statuses = {t['status'] for t in data}
    assert statuses == {'PENDING','RUNNING','SUCCESS','FAIL'}
