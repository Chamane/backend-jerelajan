from flask import Blueprint

auth_bp = Blueprint('user', __name__)

@auth_bp.route('/register', methods=['GET'])
def anrejistre_kliyan():
    return "Kliyan anrejistre avèk siksè!"