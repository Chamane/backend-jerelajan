from flask import Blueprint, request, jsonify

from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash

from app.models import User, db

auth_bp = Blueprint('user', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({"message": "Non itilizatè ak modpas obligatwa!"}), 400
    
    hashed_password = generate_password_hash(password)
    new_user = User(username=username, password=hashed_password)
    
    db.session.add(new_user)
    db.session.commit()
    
    just_created_user = User.query.filter_by(username=username).first()
    
    return jsonify({
        "message": "Itilizatè anrejistre avèk siksè!",
        "user": {
            "id": just_created_user.id,
            "username": just_created_user.username
        }
    }), 201
    
@auth_bp.route('/login', methods=['POST']) 
def login():
    data = request.get_json()

    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"message": "Non itilizatè ak modpas obligatwa!"}), 400

    user = User.query.filter_by(username=username).first()

    if not user or not check_password_hash(user.password, password):
        return jsonify({"message": "Non itilizatè oswa modpas ki pa kòrèk!"}), 401

    access_token = create_access_token(identity=user.id)

    return jsonify({
        "message": "Koneksyon avèk siksè!",
        "access_token": access_token,
        "user": {
            "id": user.id,
            "username": user.username
        }
    }), 200