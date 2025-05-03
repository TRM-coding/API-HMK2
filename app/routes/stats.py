from flask import Blueprint, request, jsonify
from ..extensions import db
from ..models import StatsLog

stats_bp = Blueprint('stats', __name__)

@stats_bp.route('/stats/<int:stats_id>', methods=['GET'])
def get_stats(stats_id):
    stats = db.session.get(StatsLog, stats_id)
    if stats is None:
        return jsonify({'error': 'not found'}), 404
    # ...existing code...