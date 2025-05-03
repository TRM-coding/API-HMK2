from flask import Blueprint, request, jsonify, abort
from ..extensions import db
from ..models import Offer
from ..utils import to_dict

offers_bp = Blueprint('offers', __name__)

@offers_bp.route('', methods=['GET'])
def list_offers():
    offers = Offer.query.all()
    return jsonify([to_dict(o) for o in offers])

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

@offers_bp.route('/<int:offer_id>', methods=['DELETE'])
def delete_offer(offer_id):
    o = db.session.get(Offer, offer_id)
    if o is None:
        return jsonify({'error': 'not found'}), 404
    db.session.delete(o)
    db.session.commit()
    return '', 204
