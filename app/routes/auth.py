from flask import Blueprint, request, jsonify

from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash

from app.models import User, db

auth_bp = Blueprint('user', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Register a new user
    ---
    tags:
      - Authentication
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required:
            - username
            - password
          properties:
            username:
              type: string
              example: testuser
            password:
              type: string
              example: "1234"
    responses:
      201:
        description: User registered successfully
        schema:
          type: object
          properties:
            message:
              type: string
              example: Itilizatè anrejistre avèk siksè!
            user:
              type: object
              properties:
                id:
                  type: integer
                  example: 1
                username:
                  type: string
                  example: testuser
      400:
        description: Missing or invalid data
        schema:
          type: object
          properties:
            message:
              type: string
              example: Non itilizatè ak modpas obligatwa!
    """
    
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
    """
    User login
    ---
    tags:
      - Authentication
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required:
            - username
            - password
          properties:
            username:   
              type: string
              example: testuser
            password:
              type: string
              example: "1234"
    responses:
      200:
        description: User logged in successfully      
        schema:
          type: object
          properties:
            message:
              type: string
              example: Koneksyon avèk siksè!
            access_token:
              type: string
              example: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
            user:
              type: object
              properties:
                id:
                  type: integer
                  example: 1
                username:
                  type: string
                  example: testuser
      400:
        description: Missing data
        schema:
          type: object
          properties:
            message:  
              type: string
              example: Non itilizatè oswa modpas ki pa kòrèk! 
    """
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