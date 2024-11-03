# models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Hotel(db.Model):
    __tablename__ = 'hoteis'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    estrelas = db.Column(db.Float(precision=1))
    diaria = db.Column(db.Float(precision=2))
    cidade = db.Column(db.String(40))

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "estrelas": self.estrelas,
            "diaria": self.diaria,
            "cidade": self.cidade
        }

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(50), nullable=False, unique=True)
    senha = db.Column(db.String(255), nullable=False)
    ativado = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {
            "id": self.id,
            "login": self.login,
            "ativado": self.ativado
        }
