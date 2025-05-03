import io
import os
import pytest
import json
from app import create_app, db
from app.models import Offer

@pytest.fixture
def app():
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    # 覆盖上传/下载及 Celery 同步
    app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'tmp_uploads')
    app.config['RESULT_FOLDER'] = os.path.join(os.getcwd(), 'tmp_results')
    app.config['CELERY_TASK_ALWAYS_EAGER'] = True
    return app.test_client()

def test_import_csv_creates_offers(client):
    # 构造 CSV 内容，双引号内的引号采用双写的方式进行转义
    csv_content = """\
company_name,position,salary_min,salary_max,currency,location,description,tags
CorpA,Dev,1000,2000,CNY,Beijing,DescA,"[""Tag1"",""Tag2""]"
CorpB,QA,1500,2500,CNY,Shanghai,DescB,"[""Tag3""]"
"""
    data = {
        'file': (io.BytesIO(csv_content.encode('utf-8')), 'offers.csv'),
        'type': 'IMPORT'
    }
    # 上传并处理
    rv = client.post('/tasks', data=data, content_type='multipart/form-data')
    assert rv.status_code == 201
    resp = rv.get_json()
    assert resp['status'] == 'SUCCESS'

    # 验证 offers 被写入
    rv2 = client.get('/offers')
    assert rv2.status_code == 200
    result = rv2.get_json()
    # 修改：从分页数据中获取 items 列表
    offers = result['items'] if 'items' in result else result
    names = [o['company_name'] for o in offers]
    assert 'CorpA' in names and 'CorpB' in names

    # 检查字段值
    oa = next(o for o in offers if o['company_name']=='CorpA')
    assert oa['position']=='Dev'
    assert oa['salary_min']=='1000.00'  # Numeric values are formatted with two decimals
    assert oa['tags']==["Tag1","Tag2"]
