from flask import jsonify, request
from main import app, con


@app.route('/Livro', methods=['GET'])
def livro():
    try:
        cur = con.cursor()
        cur.execute("SELECT id_livro, titulo, autor, ano_publicacao FROM livro")
        livros = cur.fetchall()

        livros_list = []

        for livro in livros:
            livros_list.append({
                'id_livro': livro[0],
                'titulo': livro[1],
                'autor': livro[2],
                'ano_publicacao': livro[3]
            })

        return jsonify(
            mensagem='Lista de Livros',
            livros=livros_list
        ), 200

    except Exception as e:
        return jsonify(
            mensagem=f'Erro ao acessar o banco de dados: {e}'
        ), 500
    finally:
        cur.close()


@app.route('/livro', methods=['POST'])
def criar_livro():
    try:
        data = request.get_json()

        titulo = data.get('titulo')
        autor = data.get('autor')
        ano_publicacao = data.get('ano_publicacao')

        if not all([titulo, autor, ano_publicacao]):
            return jsonify({'erro': 'Todos os campos são obrigatórios'}), 400

        cur = con.cursor()

        cur.execute('SELECT 1 FROM livro WHERE titulo = ?', (titulo,))
        if cur.fetchone():
            return jsonify({'erro': 'Livro já cadastrado'}), 400

        cur.execute("""INSERT INTO livro (titulo, autor, ano_publicacao) 
                    VALUES (?, ?, ?)""", (titulo, autor, ano_publicacao))

        con.commit()

        cur.execute("SELECT id_livro FROM livro WHERE titulo = ?", (titulo,))
        livro_id = cur.fetchone()[0]

        return jsonify({
            'mensagem': "Livro cadastrado com sucesso",
            'livro': {
                'id_livro': livro_id,
                'titulo': titulo,
                'autor': autor,
                'ano_publicacao': ano_publicacao
            }
        }), 201

    except Exception as e:
        con.rollback()
        return jsonify({
            'mensagem': f'Erro ao cadastrar livro: {e}'
        }), 500
    finally:
        if 'cur' in locals():
            cur.close()