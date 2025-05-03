import pytest
from datetime import date
from app import create_app, db
from app.models import StatsLog

@pytest.fixture
def app():
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        # 插入模拟数据
        from app.models import StatsLog
        db.session.add_all([
            StatsLog(date=date.fromisoformat('2025-04-28'), offer_count=120, avg_salary=18500.50),
            StatsLog(date=date.fromisoformat('2025-04-29'), offer_count=135, avg_salary=19200.75),
            StatsLog(date=date.fromisoformat('2025-04-30'), offer_count=110, avg_salary=17850.00),
            StatsLog(date=date.fromisoformat('2025-05-01'), offer_count=140, avg_salary=20000.00),
            StatsLog(date=date.fromisoformat('2025-05-02'), offer_count=130, avg_salary=19500.25),
        ])
        db.session.commit()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_create_and_get_stats(client):
    payload = {"date": date.today().isoformat(), "offer_count": 5, "avg_salary": "12345.67"}
    rv = client.post('/stats_logs', json=payload)
    assert rv.status_code == 201
    data = rv.get_json()
    assert data['offer_count'] == 5
    # fetch
    rv2 = client.get(f"/stats_logs/{data['log_id']}")
    assert rv2.status_code == 200
    obj2 = rv2.get_json()
    assert obj2['avg_salary'] == "12345.67"

def test_list_stats_logs(client):
    rv = client.get('/stats_logs')
    assert rv.status_code == 200
    data = rv.get_json()
    assert isinstance(data, list) and len(data) == 5
    dates = [l['date'] for l in data]
    for d in ['2025-04-28','2025-04-29','2025-04-30','2025-05-01','2025-05-02']:
        assert d in dates
