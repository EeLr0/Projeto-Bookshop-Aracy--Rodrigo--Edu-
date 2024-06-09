from flask import jsonify, request, abort, make_response,app,Flask
from book import Book, db,CD_DVD, Cliente
import os
import sqlalchemy

# Instância do Flask
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'new_database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#inicializa banco de dados
db.init_app(app)

# Classe BookShop
class BookShop:

    """CRUD da Classe Book"""
    def get(self, isbn):
        return Book.query.get(isbn)

    def add_book(self, book):
        db.session.add(book)
        db.session.commit()

    def delete_book(self, isbn):
        book = self.get(isbn)
        if book:
            db.session.delete(book)
            db.session.commit()

    def get_author_books(self, author):
        return Book.query.filter_by(author=author).all()

    def remove_books_by_author(self, author):
        books_to_remove = Book.query.filter_by(author=author).all()
        for book in books_to_remove:
            db.session.delete(book)
        db.session.commit()

    def get_most_expensive_books(self, limit=1):
        return Book.query.order_by(Book.price.desc()).limit(limit).all()

    def get_cheapest_books(self, limit=1):
        return Book.query.order_by(Book.price.asc()).limit(limit).all()

    def get_total_books(self):
        return Book.query.count()
    def delete_by_gender(self, gender):
        books = Book.query.filter_by(gender = gender).all()
        for book in books:
            db.session.delete(book)
        db.session.commit()
    
##(EXERCICIO 2)Implementaçõe do Projeto Pratico 
## TODO: f) Remoção de todos os livros associados a um determinado género;
##       g) Informação sobre o(s) livro(s) mais caro(s);
##       h) Informação sobre o(s) livro(s) mais barato(s);
##       i) Informação sobre o no total de títulos na livraria.


#######Implementação da classe CD na livraria do aula passada################
    """CRUD da classe CD_DVD"""
    def get_cd_dvd(self, artist):
        return CD_DVD.query.get(artist)

    def add_cd_dvd(self, cd_dvd):
        db.session.add(cd_dvd)
        db.session.commit()

    def delete_cd_dvd(self, artist):
        cd_dvd = self.get_cd_dvd(artist)
        if cd_dvd:
            db.session.delete(cd_dvd)
            db.session.commit()

    def get_artist_cd_dvds(self, artist):
        return CD_DVD.query.filter_by(artist=artist).all()

    def remove_cd_dvds_by_artist(self, artist):
        cds_to_remove = CD_DVD.query.filter_by(artist=artist).all()
        for cd in cds_to_remove:
            db.session.delete(cd)
        db.session.commit()

    def get_most_expensive_cd_dvds(self, limit=1):
        return CD_DVD.query.order_by(CD_DVD.price.desc()).limit(limit).all()

    def get_cheapest_cd_dvds(self, limit=1):
        return CD_DVD.query.order_by(CD_DVD.price.asc()).limit(limit).all()

    def get_total_cd_dvds(self):
        return CD_DVD.query.count()
    


#######Implementação da classe Cliente na livraria ################    
    """CRUD da classe cliente"""
##TODO: Implementar os seguintes recursos de CRUD
##      
##      a. Inserção, remoção e edição de um cliente;
##      b. Obtenção de informação de todos os livros adquiridos por um determinado cliente;
##      c. Indicação do cliente mais antigo e do número de livros por ele adquiridos;
##      d. Lista dos clientes que compraram um determinado livro;
##      e. Indicação do género preferido dos clientes;

    def add_cliente(self, cliente):
        db.session.add(cliente)
        db.session.commit()
    
    def delete_cliente(self,nome_cliente):
        cliente = self.get_cd_dvd(nome_cliente)
        if cliente:
            db.session.delete(cliente)
            db.session.commit()

    def edit_cliente(self, nome_cliente, novos_dados):
        cliente = Cliente.query.get(nome_cliente)
        if cliente:
            for key, value in novos_dados.items():
                setattr(cliente, key, value)
            db.session.commit()
            return cliente
        return None
    
##      e. Indicação do género preferido dos clientes;
    def get_genero_preferido_cliente( self, nome_cliente):
        cliente = Cliente.query.get(nome_cliente)
        if cliente:
            return cliente.genero_preferido()
        return None
    

# Instância do BookShop
bookshop = BookShop()

with app.app_context():
        db.create_all()

############Implementação das rotas da classe Bookshop##########################
# Rotas e serviços de book
@app.route('/book/list', methods=['GET'])
def get_books():
    books = Book.query.all()
    return jsonify({'books': [book.to_json() for book in books]})

@app.route('/book/<int:isbn>', methods=['GET'])
def get_book(isbn):
    book = bookshop.get(isbn)
    if not book:
        abort(404)
    return jsonify({'book': book.to_json()})

@app.route('/book', methods=['POST'])
def create_book():
    print('create book') 
    if not request.json or not 'isbn' in request.json: 
        abort(400, description="ISBN is required.")
    
    isbn = request.json['isbn']
    existing_book = Book.query.filter_by(isbn=isbn).first()
    
    if existing_book:
        return jsonify({'error': 'Book with this ISBN already exists.'}), 400
    
    book = Book(
        isbn=isbn,
        title=request.json['title'],
        gender=request.json['gender'],  # genero adicionado
        author=request.json.get('author', ""), 
        price=float(request.json['price'])
    )
    db.session.add(book)
    db.session.commit()
    
    return jsonify({'book': book.to_json()}), 201  # Use to_json() method here

@app.route('/book/<int:isbn>', methods=['DELETE'])
def delete_book(isbn):
    bookshop.delete_book(isbn)
    return jsonify({'result': True})

'''Exercicios 2-'''
@app.route('/author/<author>/books', methods=['GET'])
def get_books_by_author(author):
    books = bookshop.get_author_books(author)
    return jsonify({'books': [book.to_json() for book in books]})

@app.route('/author/<author>/remove', methods=['DELETE'])
def remove_books_by_author(author):
    bookshop.remove_books_by_author(author)
    return jsonify({'result': True})

@app.route('/book/most_expensive', methods=['GET'])
def get_most_expensive_books():
    limit = request.args.get('limit', 1, type=int)
    books = bookshop.get_most_expensive_books(limit)
    return jsonify({'books': [book.to_json() for book in books]})

@app.route('/book/cheapest', methods=['GET'])
def get_cheapest_books():
    limit = request.args.get('limit', 1, type=int)
    books = bookshop.get_cheapest_books(limit)
    return jsonify({'books': [book.to_json() for book in books]})

@app.route('/book/total_count', methods=['GET'])
def get_total_books_count():
    count = bookshop.get_total_books()
    return jsonify({'total_books': count})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

##(EXERCICIO 2) Implementaçõe do Projeto Pratico
## TODO: Implementar rotas das alineas f),g),h),i)
@app.route('/remove/<string:gender>', methods=['DELETE'])
def remove_from_gender(gender):
    bookshop.delete_by_gender(gender)
    return jsonify({'result': True}), 200


##########Rotas e serviços do CD-DVD##############
@app.route('/cd_dvd/list', methods=['GET'])
def get_cd_dvds():
    cds = CD_DVD.query.all()
    return jsonify({'cd_dvds': [cd.to_json() for cd in cds]})

@app.route('/cd_dvd/<artist>', methods=['GET'])
def get_cd_dvd(artist):
    cd_dvd = bookshop.get_cd_dvd(artist)
    if not cd_dvd:
        abort(404)
    return jsonify({'cd_dvd': cd_dvd.to_json()})

@app.route('/cd_dvd', methods=['POST'])
def create_cd_dvd():
    if not request.json or not 'artist' in request.json:
        abort(400)
    cd_dvd = CD_DVD(
        album_title=request.json['album_title'],
        artist=request.json['artist'],
        genre=request.json['genre'],
        release_year=request.json['release_year'],
        disc_number=request.json['disc_number'],
        duration=request.json['duration'],
        price=float(request.json['price'])
    )
    bookshop.add_cd_dvd(cd_dvd)
    return jsonify({'cd_dvd': cd_dvd.to_json()}), 201

@app.route('/cd_dvd/<artist>', methods=['DELETE'])
def delete_cd_dvd(artist):
    bookshop.delete_cd_dvd(artist)
    return jsonify({'result': True})

@app.route('/artist/<artist>/cd_dvds', methods=['GET'])
def get_cd_dvds_by_artist(artist):
    cds = bookshop.get_artist_cd_dvds(artist)
    return jsonify({'cd_dvds': [cd.to_json() for cd in cds]})

@app.route('/artist/<artist>/cd_dvds/remove', methods=['DELETE'])
def remove_cd_dvds_by_artist(artist):
    bookshop.remove_cd_dvds_by_artist(artist)
    return jsonify({'result': True})

@app.route('/cd_dvd/most_expensive', methods=['GET'])
def get_most_expensive_cd_dvds():
    limit = request.args.get('limit', 1, type=int)
    cds = bookshop.get_most_expensive_cd_dvds(limit)
    return jsonify({'cd_dvds': [cd.to_json() for cd in cds]})

@app.route('/cd_dvd/cheapest', methods=['GET'])
def get_cheapest_cd_dvds():
    limit = request.args.get('limit', 1, type=int)
    cds = bookshop.get_cheapest_cd_dvds(limit)
    return jsonify({'cd_dvds': [cd.to_json() for cd in cds]})

@app.route('/cd_dvd/total_count', methods=['GET'])
def get_total_cd_dvds_count():
    count = bookshop.get_total_cd_dvds()
    return jsonify({'total_cd_dvds': count})

"""Lista todos os CD_DVDs e os books dados pelos author ou artista"""
@app.route('/works/<author_or_artist>', methods=['GET'])
def get_works_by_author_or_artist(author_or_artist):
    books = bookshop.get_author_books(author_or_artist)
    cds = bookshop.get_artist_cd_dvds(author_or_artist)
    return jsonify({
        'books': [book.to_json() for book in books],
        'cd_dvds': [cd.to_json() for cd in cds]
    })

####### Rotas dos serviços Do Cliente ##############

@app.route('/cliente', methods=['POST'])
def create_cliente():
    data = request.get_json()
    new_cliente = Cliente(
        nome_cliente=data['nome_cliente'],
        apelido_cliente=data['apelido_cliente'],
        bi_cni_cliente=data['bi_cni_cliente'],
        ano_subscricao=data['ano_subscricao'],
        morada=data['morada']
    )
    try:
        bookshop.add_cliente(new_cliente)
        return jsonify(new_cliente.to_json()), 201
    except sqlalchemy.exc.IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Cliente with this nome_cliente already exists"}), 400

@app.route('/cliente/delete/<nome_cliente>', methods=['DELETE'])
def delete_cliente(nome_cliente):
    bookshop.delete_cliente(nome_cliente)
    return jsonify({'result': True})

@app.route('/cliente/update/<nome_cliente>', methods=['PUT'])
def edit_cliente(nome_cliente):
    data = request.get_json()
    updated_cliente = bookshop.edit_cliente(nome_cliente, data)
    if updated_cliente:
        return jsonify(updated_cliente.to_json())
    return jsonify({"error": "Cliente not found"}), 404

@app.route('/adicionar_livros/<nome_cliente>', methods=['POST'])
def adicionar_livros(nome_cliente):
    cliente = Cliente.query.get(nome_cliente)
    if not cliente:
        return jsonify({"error": "Cliente não encontrado"}), 404

    data = request.get_json()
    isbn_list = data.get('isbn_list', [])
    
    if not isbn_list:
        return jsonify({"error": "Lista de ISBNs não fornecida"}), 400

    for isbn in isbn_list:
        livro = Book.query.get(isbn)
        if livro:
            cliente.livros.append(livro)
        else:
            return jsonify({"error": f"Livro com ISBN {isbn} não encontrado"}), 404

    db.session.commit()
    return jsonify({"message": "Livros adicionados com sucesso"}), 200

@app.route('/cliente/livros/<string:cliente_nome>', methods=['GET'])
def get_livros_cliente(cliente_nome):
    cliente = Cliente.query.get(cliente_nome)
    if not cliente:
        return jsonify({"error": "Cliente não encontrado"}), 404
    livros = cliente.livros
    return jsonify({'livros': [livro.to_json() for livro in livros]})

##  c. Indicação do cliente mais antigo e do número de livros por ele adquiridos;
@app.route('/cliente/maisAntigo', methods=['GET'])
def get_cliente_mais_anigo():
    cliente = Cliente.query.order_by(Cliente.ano_subscricao).first_or_404()
    return jsonify({"cliente": cliente.to_json()})


#d. Lista dos clientes que compraram um determinado livro;
@app.route('/cliente/livros/clientes/<string:title>', methods=['GET'])
def get_lista_livro_obtido_clientes(title):
    livro = Book.query.filter_by(title=title).first()
    if not livro:
        return jsonify({"error": "Livro não encontrado"}), 404
    
    clientes = Cliente.query.filter(Cliente.livros.any(Book.isbn == livro.isbn)).all()
    return jsonify({"clientes": [cliente.to_json() for cliente in clientes]})

##e. Rota Indicação do género preferido dos clientes;    
@app.route('/cliente/genero_preferido/<string:nome_cliente>', methods = ['GET'])
def get_genero_preferido_cliente(nome_cliente):
    genero_preferido = bookshop.get_genero_preferido_cliente(nome_cliente)
    if genero_preferido:
        return jsonify({'genero_preferido': genero_preferido})
    return jsonify({"erro": "Cliente nao encontrado ou nenhum genero preferido encontrado"}),404       





if __name__ == '__main__':
    # Criar tabelas antes do primeiro pedido
    app.run(debug=True, host= '0.0.0.0', port=5000)

    
