# app.py
from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from config import DATABASE_URI
from models import db
from resources import HotelResource, UsuarioResource, UsuarioLogin, UsuarioRegister, UsuarioConfirmacao

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'DontTellAnyone'
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db.init_app(app)
api = Api(app)
jwt = JWTManager(app)

# Rotas para Hotel
api.add_resource(HotelResource, '/hoteis', '/hoteis/<int:hotel_id>')

# Rotas para Usuario
api.add_resource(UsuarioResource, '/usuarios', '/usuarios/<int:usuario_id>')

# Rotas para Login
api.add_resource(UsuarioRegister, '/cadastro')

# Rotas para Login
api.add_resource(UsuarioLogin, '/login')

# Confirma usuario
api.add_resource(UsuarioConfirmacao, '/confirmacao/<int:usuario_id>')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Cria as tabelas no banco de dados
    app.run(debug=True)
