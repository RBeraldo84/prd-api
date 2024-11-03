# resources.py
from flask import request
from flask_restful import Resource, reqparse 
from flask_jwt_extended import create_access_token, jwt_required
from models import db, Hotel, Usuario
from werkzeug.security import generate_password_hash    

# Parser para Hotel
hotel_parser = reqparse.RequestParser()
hotel_parser.add_argument('nome', type=str, required=True, help="The field 'nome' cannot be left blank.")
hotel_parser.add_argument('estrelas', type=float)
hotel_parser.add_argument('diaria', type=float)
hotel_parser.add_argument('cidade', type=str)

# Parser para Usuario
usuario_parser = reqparse.RequestParser()
usuario_parser.add_argument('login', type=str, required=True, help="The field 'login' cannot be left blank.")
usuario_parser.add_argument('senha', type=str, required=True, help="The field 'senha' cannot be left blank.")
usuario_parser.add_argument('ativado', type=bool)

# Recursos para Hotel
class HotelResource(Resource):
    
    @jwt_required()
    def get(self, hotel_id=None):
        if hotel_id:
            hotel = Hotel.query.get(hotel_id)
            if hotel:
                return hotel.to_dict(), 200
            return {'message': 'Hotel not found'}, 404
        return [hotel.to_dict() for hotel in Hotel.query.all()], 200
    
    @jwt_required()
    def post(self):
        data = hotel_parser.parse_args()
        
        # Verifica se o hotel já existe pelo nome
        if Hotel.query.filter_by(nome=data['nome']).first():
            return {'message': f"Hotel '{data['nome']}' já está cadastrado."}, 400
        
        # Criação do novo hotel caso não exista
        hotel = Hotel(**data)
        db.session.add(hotel)
        db.session.commit()
        return hotel.to_dict(), 201

    @jwt_required()
    def put(self, hotel_id):
        data = hotel_parser.parse_args()
        hotel = Hotel.query.get(hotel_id)
        if hotel:
            for key, value in data.items():
                setattr(hotel, key, value)
            db.session.commit()
            return hotel.to_dict(), 200
        return {'message': 'Hotel not found'}, 404

    @jwt_required()
    def delete(self, hotel_id):
        hotel = Hotel.query.get(hotel_id)
        if hotel:
            db.session.delete(hotel)
            db.session.commit()
            return {'message': 'Hotel deleted'}, 200
        return {'message': 'Hotel not found'}, 404

class UsuarioRegister(Resource):
    def post(self):
        data = request.get_json()

        # Verifica se os campos obrigatórios estão presentes
        if 'login' not in data or 'senha' not in data:
            return {'message': 'Os campos "login" e "senha" são obrigatórios.'}, 400

        # Verifica se o login já existe no banco de dados
        if Usuario.query.filter_by(login=data['login']).first():
            return {'message': f"Usuário com o login '{data['login']}' já está registrado."}, 400

        # Hasheia a senha antes de salvar
        hashed_password = generate_password_hash(data['senha'])

        # Cria o novo usuário
        novo_usuario = Usuario(login=data['login'], senha=hashed_password)
        db.session.add(novo_usuario)
        db.session.commit()

        return {'message': 'Usuário criado com sucesso!'}, 201

class UsuarioLogin(Resource):
    def post(self):
        data = request.get_json()
        usuario = Usuario.query.filter_by(login=data['login']).first()

        # Verifique a senha (simples comparação; você pode usar hash de senha para maior segurança)
        if usuario and usuario.senha == data['senha']:
            access_token = create_access_token(identity=usuario.id)
            return {'access_token': access_token}, 200

        return {'message': 'Credenciais inválidas'}, 401


# Atualiza o campo "ativado" na tabela
class UsuarioConfirmacao(Resource):
    def post(self, usuario_id):
        # Busque o usuário pelo ID
        usuario = Usuario.query.get(usuario_id)
        
        if usuario:
            # Atualize o campo 'ativado' para True
            usuario.ativado = True
            db.session.commit()
            return {'message': 'Usuário ativado com sucesso!'}, 200
        return {'message': 'Usuário não encontrado'}, 404


# Recursos para Usuario
class UsuarioResource(Resource):
    def get(self, usuario_id=None):
        if usuario_id:
            usuario = Usuario.query.get(usuario_id)
            if usuario:
                return {'id': usuario.id, 'login': usuario.login, 'ativado': usuario.ativado}, 200
            return {'message': 'Usuario not found'}, 404
        return [usuario.to_dict() for usuario in Usuario.query.all()], 200    
    
class UsuarioLogin(Resource):
    def post(self):
        data = request.get_json()

        # Verificar se os campos 'login' e 'senha' estão presentes
        if 'login' not in data or 'senha' not in data:
            return {'message': 'Os campos "login" e "senha" são obrigatórios.'}, 400
        
        usuario = Usuario.query.filter_by(login=data['login']).first()

        # Verifique a senha
        if usuario and usuario.senha == data['senha']:
            access_token = create_access_token(identity=usuario.id)
            return {'access_token': access_token}, 200

        return {'message': 'Credenciais inválidas'}, 401

    def put(self, usuario_id):
        data = usuario_parser.parse_args()
        usuario = Usuario.query.get(usuario_id)
        if usuario:
            for key, value in data.items():
                setattr(usuario, key, value)
            db.session.commit()
            return usuario.to_dict(), 200
        return {'message': 'Usuario not found'}, 404

    def delete(self, usuario_id):
        usuario = Usuario.query.get(usuario_id)
        if usuario:
            db.session.delete(usuario)
            db.session.commit()
            return {'message': 'Usuario deleted'}, 200
        return {'message': 'Usuario not found'}, 404

