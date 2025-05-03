import pytest
from app import create_app, db
from app.models import Offer

@pytest.fixture
def app():
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        # 插入模拟数据
        from app.models import Offer
        db.session.add_all([
            Offer(company_name='TechCorp',   position='Backend Engineer',   salary_min=15000, salary_max=25000, currency='CNY', location='Beijing',  description='负责后端服务开发与维护。', tags=['Java','Spring','MySQL']),
            Offer(company_name='HealthPlus', position='Data Analyst',       salary_min=12000, salary_max=18000, currency='CNY', location='Shanghai', description='数据分析与报告。',         tags=['Python','SQL','Tableau']),
            Offer(company_name='EduFuture',  position='Frontend Developer', salary_min=10000, salary_max=20000, currency='CNY', location='Guangzhou',description='负责前端页面开发。',        tags=['JavaScript','Vue.js']),
            Offer(company_name='GlobalLink', position='DevOps Engineer',    salary_min=20000, salary_max=30000, currency='CNY', location='Shenzhen', description='CI/CD 管道搭建与维护。',   tags=['Docker','Kubernetes','AWS']),
        ])
        db.session.commit()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_create_and_get_offer(client):
    data = {"company_name": "TestCo", "position": "Engineer"}
    rv = client.post('/offers', json=data)
    assert rv.status_code == 201
    obj = rv.get_json()
    assert obj['company_name'] == "TestCo"
    assert obj['position']     == "Engineer"
    # 新增字段默认值校验
    assert obj['currency']     == 'CNY'
    assert obj['salary_min']   is None
    assert obj['salary_max']   is None
    assert obj['location']     is None
    assert obj['description']  is None
    assert obj['tags']         == []
    assert 'created_at' in obj and 'updated_at' in obj

    # fetch it back
    rv2 = client.get(f"/offers/{obj['id']}")
    assert rv2.status_code == 200
    obj2 = rv2.get_json()
    assert obj2['position'] == "Engineer"

def test_list_offers(client):
    rv = client.get('/offers')
    assert rv.status_code == 200
    data = rv.get_json()
    assert isinstance(data, dict)
    # 分页主体
    assert 'items' in data and isinstance(data['items'], list)
    assert data['total'] == 4
    assert data['page'] == 1
    assert data['per_page'] == 10
    assert data['pages'] == 1
    items = data['items']
    assert len(items) == 4
    for o in items:
        assert 'company_name' in o
        assert 'position' in o
        assert 'currency' in o
        assert 'tags' in o
        assert 'created_at' in o
    names = [o['company_name'] for o in items]
    for name in ['TechCorp','HealthPlus','EduFuture','GlobalLink']:
        assert name in names