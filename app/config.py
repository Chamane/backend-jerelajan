

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///expenses.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'uyt78t78y098hbi8yg87ty79y89y89yu89'
    JWT_SECRET_KEY = "jhebuhdb3beihdbjebwrdhjbjqw"
    SWAGGER = {
        "title": "Jerelajan API",
        "uiversion": 3,
        "securityDefinitions": {
            "Bearer": {
                "type": "apiKey",
                "name": "Authorization",
                "in": "header",
                "description": "JWT Authorization header using the Bearer scheme. Example: 'Authorization: Bearer {token}'"
            }
        }
    }