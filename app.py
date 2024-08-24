from flask import Flask, jsonify, request

app = Flask(__name__)

# Sample data for pets
pets = [
    {
        "id": 1,
        "name": "Bella",
        "age": 3,
        "url": "https://thumbor.forbes.com/thumbor/fit-in/900x510/https://www.forbes.com/advisor/wp-content/uploads/2023/07/top-20-small-dog-breeds.jpeg.jpg"
    },
    {
        "id": 2,
        "name": "Charlie",
        "age": 4,
        "url": "https://www.thesprucepets.com/thmb/hxWjs7evF2hP1Fb1c1HAvRi_Rw0=/2765x0/filters:no_upscale():strip_icc()/chinese-dog-breeds-4797219-hero-2a1e9c5ed2c54d00aef75b05c5db399c.jpg"
    },
    {
        "id": 3,
        "name": "Max",
        "age": 2,
        "url": "https://s3.amazonaws.com/cdn-origin-etr.akc.org/wp-content/uploads/2017/11/02151216/Afghan-Hound-standing-in-a-garden-400x267.jpg"
    },
    {
        "id": 4,
        "name": "Luna",
        "age": 5,
        "url": "https://media-cldnry.s-nbcnews.com/image/upload/t_nbcnews-fp-1200-630,f_auto,q_auto:best/rockcms/2022-08/220805-border-collie-play-mn-1100-82d2f1.jpg"
    }
]

# Define a route for the root URL
@app.route('/')
def root():
    return "Welcome to the Pet Shop API!"

@app.route('/pets')
def pets_list():
    return jsonify(pets)

@app.route('/<int:id>')
def pet_detail(id):
    # Find the pet by id
    pet = next((pet for pet in pets if pet['id'] == id), None)
    if pet:
        return jsonify(pet)
    else:
        return jsonify({"error": "Pet not found"}), 404

@app.route('/pets', methods=['POST'])
def add_pet():
    # Get the request data
    data = request.get_json()

    # Check if required fields are present
    if not all(k in data for k in ("id", "name", "age", "url")):
        return jsonify({"error": "Missing data"}), 400

    # Check if pet with the same id already exists
    if any(pet['id'] == data['id'] for pet in pets):
        return jsonify({"error": "Pet with this ID already exists"}), 400

    # Add the new pet to the list
    pets.append(data)
    return jsonify(data), 201

@app.route('/pets/<int:id>', methods=['DELETE'])
def delete_pet(id):
    global pets
    # Find the pet by id
    pet = next((pet for pet in pets if pet['id'] == id), None)
    if pet:
        # Remove the pet from the list
        pets = [pet for pet in pets if pet['id'] != id]
        return jsonify({"message": "Pet deleted successfully"}), 200
    else:
        return jsonify({"error": "Pet not found"}), 404

@app.route('/pets/<int:id>/', methods=['PUT'])
def edit_pet(id):
    # Get the request data
    data = request.get_json()

    # Find the pet by id
    pet = next((pet for pet in pets if pet['id'] == id), None)
    if pet:
        # Update pet details
        pet.update(data)
        return jsonify(pet), 200
    else:
        return jsonify({"error": "Pet not found"}), 404


if __name__ == '__main__':
    app.run(debug=True)
