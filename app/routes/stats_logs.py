from flask import Blueprint, request, jsonify, abort
from ..extensions import db
from ..models import StatsLog
from ..utils import to_dict
from datetime import date

stats_logs_bp = Blueprint('stats_logs', __name__)

@stats_logs_bp.route('', methods=['GET'])
def list_stats():
    logs = StatsLog.query.all()
    return jsonify([to_dict(l) for l in logs])

@stats_logs_bp.route('/<int:log_id>', methods=['GET'])
def get_stats(log_id):
    l = db.session.get(StatsLog, log_id)
    if l is None:
        abort(404)
    return jsonify(to_dict(l))

@stats_logs_bp.route('', methods=['POST'])
def create_stats():
    data = request.get_json()
    if 'date' in data and isinstance(data['date'], str):
        data['date'] = date.fromisoformat(data['date'])
    # Check for an existing record with the same date to avoid duplicates.
    existing = StatsLog.query.filter_by(date=data['date']).first()
    if existing:
        for k, v in data.items():
            setattr(existing, k, v)
        db.session.commit()
        return jsonify(to_dict(existing)), 200
    l = StatsLog(**data)
    db.session.add(l)
    db.session.commit()
    return jsonify(to_dict(l)), 201

@stats_logs_bp.route('/<int:log_id>', methods=['PUT'])
def update_stats(log_id):
    l = db.session.get(StatsLog, log_id)
    if l is None:
        abort(404)
    data = request.get_json()
    for k, v in data.items():
        # on update, also convert date strings
        if k == 'date' and isinstance(v, str):
            v = date.fromisoformat(v)
        if hasattr(l, k):
            setattr(l, k, v)
    db.session.commit()
    return jsonify(to_dict(l))

@stats_logs_bp.route('/<int:log_id>', methods=['DELETE'])
def delete_stats(log_id):
    l = db.session.get(StatsLog, log_id)
    if l is None:
        abort(404)
    db.session.delete(l)
    db.session.commit()
    return '', 204
