from flask import Blueprint, request, jsonify

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