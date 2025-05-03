from flask import Blueprint, request, jsonify, abort
from ..extensions import db
from ..models import Offer
from ..utils import to_dict

offers_bp = Blueprint('offers', __name__)

@offers_bp.route('', methods=['GET'])
def list_offers():
    # 新增：支持部分检索和分页
    q = request.args.get('q', type=str)
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    query = Offer.query
    if q:
        query = query.filter(Offer.company_name.ilike(f'%{q}%'))
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    items = [to_dict(o) for o in pagination.items]
    return jsonify({
        'items': items,
        'total': pagination.total,
        'page': pagination.page,
        'per_page': pagination.per_page,
        'pages': pagination.pages
    })

@offers_bp.route('/<int:offer_id>', methods=['GET'])
def get_offer(offer_id):
    offer = db.session.get(Offer, offer_id)
    if offer is None:
        return jsonify({'error': 'not found'}), 404
    return jsonify(to_dict(offer))

@offers_bp.route('', methods=['POST'])
def create_offer():
    data = request.get_json()
    o = Offer(**data)
    db.session.add(o)
    db.session.commit()
    return jsonify(to_dict(o)), 201

@offers_bp.route('/<int:offer_id>', methods=['PUT'])
def update_offer(offer_id):
    o = db.session.get(Offer, offer_id)
    if o is None:
        return jsonify({'error': 'not found'}), 404
    data = request.get_json()
    for k, v in data.items():
        if hasattr(o, k):
            setattr(o, k, v)
    db.session.commit()
    return jsonify(to_dict(o))

@offers_bp.route('', methods=['DELETE'])
def bulk_delete_offers():
    data = request.get_json() or {}
    ids = data.get('ids')
    if not isinstance(ids, list):
        return jsonify({'error': 'ids must be a list'}), 400
    offers = Offer.query.filter(Offer.id.in_(ids)).all()
    for o in offers:
        db.session.delete(o)
    db.session.commit()
    return '', 204

@offers_bp.route('/<int:offer_id>', methods=['DELETE'])
def delete_offer(offer_id):
    o = db.session.get(Offer, offer_id)
    if o is None:
        return jsonify({'error': 'not found'}), 404
    db.session.delete(o)
    db.session.commit()
    return '', 204
