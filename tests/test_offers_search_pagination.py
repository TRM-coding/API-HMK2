import pytest
from app import create_app, db
from app.models import Offer

@pytest.fixture
def app():
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        # 准备 4 条数据
        db.session.add_all([
            Offer(company_name='TechCorp',   position='Backend Engineer',   salary_min=15000, salary_max=25000, currency='CNY', location='Beijing',  description='...', tags=['Java']),
            Offer(company_name='HealthPlus', position='Data Analyst',       salary_min=12000, salary_max=18000, currency='CNY', location='Shanghai', description='...', tags=['Python']),
            Offer(company_name='EduFuture',  position='Frontend Developer', salary_min=10000, salary_max=20000, currency='CNY', location='Guangzhou',description='...', tags=['Vue.js']),
            Offer(company_name='GlobalLink', position='DevOps Engineer',    salary_min=20000, salary_max=30000, currency='CNY', location='Shenzhen',description='...', tags=['AWS']),
        ])
        db.session.commit()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_search_offers_by_company_name(client):
    # 使用 q 参数部分匹配
    rv = client.get('/offers?q=Tech')
    assert rv.status_code == 200
    data = rv.get_json()
    assert data['total'] == 1
    items = data['items']
    assert len(items) == 1
    assert items[0]['company_name'] == 'TechCorp'

def test_paginate_offers(client):
    # per_page=2,page=2 应返回第3、4条
    rv = client.get('/offers?per_page=2&page=2')
    assert rv.status_code == 200
    data = rv.get_json()
    assert data['page'] == 2
    assert data['per_page'] == 2
    assert data['total'] == 4
    # 共 2 页，每页2条
    assert data['pages'] == 2
    items = data['items']
    assert len(items) == 2
    names = [o['company_name'] for o in items]
    assert set(names) == {'EduFuture','GlobalLink'}
