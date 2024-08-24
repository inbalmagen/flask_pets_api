from flask import Flask, jsonify, request
import psycopg2

app = Flask(__name__)

# Database connection settings
DB_HOST = 'dpg-cr4vmr52ng1s73e8j78g-a.frankfurt-postgres.render.com'
DB_NAME = 'db_pets_k5jh'
DB_USER = 'db_pets_k5jh_user'
DB_PASS = 'EkjGLCXC10SpVN9WjQLx2iaV3NaFoucl'
DB_PORT = '5432'  # Default PostgreSQL port

def get_db_connection():
    conn = psycopg2.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        port=DB_PORT
    )
    return conn

@app.route('/')
def root():
    return "Welcome to the Pet Shop API!"

@app.route('/pets')
def pets_list():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM pets;')
    pets = cur.fetchall()
    cur.close()
    conn.close()

    return jsonify([{
        'id': pet[0],
        'name': pet[1],
        'age': pet[2],
        'url': pet[3]
    } for pet in pets])

@app.route('/pets/<int:id>')
def pet_detail(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM pets WHERE id = %s;', (id,))
    pet = cur.fetchone()
    cur.close()
    conn.close()

    if pet:
        return jsonify({
            'id': pet[0],
            'name': pet[1],
            'age': pet[2],
            'url': pet[3]
        })
    else:
        return jsonify({"error": "Pet not found"}), 404

@app.route('/pets', methods=['POST'])
def add_pet():
    data = request.get_json()

    if not all(k in data for k in ("id", "name", "age", "url")):
        return jsonify({"error": "Missing data"}), 400

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute('SELECT * FROM pets WHERE id = %s;', (data['id'],))
    existing_pet = cur.fetchone()

    if existing_pet:
        cur.close()
        conn.close()
        return jsonify({"error": "Pet with this ID already exists"}), 400

    cur.execute(
        'INSERT INTO pets (id, name, age, url) VALUES (%s, %s, %s, %s);',
        (data['id'], data['name'], data['age'], data['url'])
    )
    conn.commit()
    cur.close()
    conn.close()

    return jsonify(data), 201

@app.route('/pets/<int:id>', methods=['DELETE'])
def delete_pet(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM pets WHERE id = %s;', (id,))
    pet = cur.fetchone()

    if pet:
        cur.execute('DELETE FROM pets WHERE id = %s;', (id,))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": "Pet deleted successfully"}), 200
    else:
        cur.close()
        conn.close()
        return jsonify({"error": "Pet not found"}), 404

@app.route('/pets/<int:id>/', methods=['PUT'])
def edit_pet(id):
    data = request.get_json()
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM pets WHERE id = %s;', (id,))
    pet = cur.fetchone()

    if pet:
        cur.execute(
            'UPDATE pets SET name = %s, age = %s, url = %s WHERE id = %s;',
            (data.get('name', pet[1]), data.get('age', pet[2]), data.get('url', pet[3]), id)
        )
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({
            'id': id,
            'name': data.get('name', pet[1]),
            'age': data.get('age', pet[2]),
            'url': data.get('url', pet[3])
        }), 200
    else:
        cur.close()
        conn.close()
        return jsonify({"error": "Pet not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
