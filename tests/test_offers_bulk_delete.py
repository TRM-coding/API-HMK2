import pytest
from app import create_app, db
from app.models import Offer

@pytest.fixture
def app():
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        # 插入 3 条测试数据
        db.session.add_all([
            Offer(company_name='A', position='P1'),
            Offer(company_name='B', position='P2'),
            Offer(company_name='C', position='P3'),
        ])
        db.session.commit()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_bulk_delete_offers(client):
    # 获取所有 ID
    rv = client.get('/offers')
    data = rv.get_json()
    ids = [o['id'] for o in data['items']]
    # 删除前两条
    rv2 = client.delete('/offers', json={'ids': ids[:2]})
    assert rv2.status_code == 204

    # 确认只剩最后一条
    rv3 = client.get('/offers')
    remaining = [o['id'] for o in rv3.get_json()['items']]
    assert remaining == [ids[2]]

def test_bulk_delete_invalid_payload(client):
    rv = client.delete('/offers', json={'ids': 'notalist'})
    assert rv.status_code == 400
    assert rv.get_json()['error'] == 'ids must be a list'
