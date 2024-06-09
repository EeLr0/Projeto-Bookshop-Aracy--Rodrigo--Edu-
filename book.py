import os
from flask import Flask, jsonify, request, abort, make_response
from flask_sqlalchemy import SQLAlchemy
from json import JSONEncoder
from datetime import datetime, time
# Instância do SQLAlchemy
db = SQLAlchemy()
cliente_livro = db.Table('cliente_livro',
        db.Column('cliente_nome', db.String, db.ForeignKey('cliente.nome_cliente'),primary_key=True),
        db.Column('book_id', db.Integer, db.ForeignKey('books.isbn'), primary_key=True)
        )
        


class Book(db.Model):
    __tablename__ = 'books'

    isbn = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(100), nullable = False)
    author = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)


    def to_json(self):
        return {
            "isbn": self.isbn,
            "title": self.title,
            "gender":self.gender, #genero adicionado
            "author": self.author,
            "price": self.price
        }

    def __repr__(self):
        return f'<Book {self.title} by {self.author}>'
    
# Classe de codificador JSON personalizado
class BookJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Book):
            return {
                'isbn': obj.isbn,
                'title': obj.title,
                'gender': obj.gender, #genero adicionado
                'author': obj.author,
                'price': obj.price
            }
        return super().default(obj)

class CD_DVD(db.Model):
    __tablename__ = 'cd_dvds'

    album_title = db.Column(db.String(100), nullable=False)
    artist = db.Column(db.String(100), primary_key=True)
    genre = db.Column(db.String(100), nullable=False)
    release_year = db.Column(db.String, nullable=False) # Convertel p String mod el tv dam erro( TODO later, pass to DAte type)
    disc_number = db.Column(db.Integer, nullable=False) # Convertel p String mod el tv dam erro( TODO later, pass to DAte type)
    duration = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)

    def to_json(self):
        return {
            "album_title": self.album_title,
            "artist": self.artist,
            "genre": self.genre,
            "release_year": self.release_year,
            "disc_number": self.disc_number,
            "duration": self.duration,
            "price": self.price
        }

class CD_DVDJsonEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, CD_DVD):
            return {
                'album_title': obj.album_title,
                'artist': obj.artist,
                'genre': obj.genre,
                'release_year': obj.release_year,
                'disc_number': obj.disc_number,
                'duration': obj.duration,
                'price': obj.price
            }
        return super().default(obj)



##Implementaçõe do Projeto Pratico (Exercicio 3)
##TODO: Implementar classe cliente
##      (nome, apelido, no BI/CNI, ano subscrição, morada, etc.).

class Cliente(db.Model):
    __tablename__ = 'cliente'
    
    nome_cliente = db.Column(db.String(100), primary_key = True)
    apelido_cliente = db.Column(db.String(100),nullable = False)
    bi_cni_cliente = db.Column(db.Integer,nullable = False)
    ano_subscricao = db.Column(db.Integer, nullable = False)
    morada = db.Column(db.String, nullable = False )
    livros = db.relationship('Book', secondary=cliente_livro, lazy='subquery', backref=db.backref('clientes', lazy=True))

    def to_json(self):
        return{
            "nome_cliente": self.nome_cliente,
            "apelido_cliente": self.apelido_cliente,
            "bi_cni_cliente": self.bi_cni_cliente,
            "ano_subscricao" : self.ano_subscricao,
            "morada": self.morada
        }
    #Função para obter o genero preferido do utilizador
    def genero_preferido (self):
        generos = [livro.gender for livro in self.livros]
        if generos:
            return max(set(generos), key = generos.count)
        return None

class Cliente_JSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Cliente):
            return{
                'nome_cliente': obj.nome_cliente,
                'apelido_cliente': obj.apelido_cliente,
                'bi_cni_cliente' : obj.bi_cni_cliente,
                'ano_subscricao': obj.ano_subscricao,
                'morada' : obj.morada
            }
        return super().default(obj)
    

