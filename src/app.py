"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
# from models import Person


app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# Create the jackson family object
jackson_family = FamilyStructure("Jackson")


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code



# Generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members/<int:member_id>', methods=['GET'])
def traerpersona(member_id):
    miembro_encontrado = jackson_family.get_member(member_id)
    if not miembro_encontrado:
        return jsonify({"error":"no se encontro el miembro error 400"})
    return jsonify(miembro_encontrado), 200




@app.route('/members', methods=['GET'])
def handle_hello():
    # This is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    response_body = {"hello": "world",
                     "family": members}
    return jsonify(response_body), 200

@app.route('/members/<int:member_id>',methods=['DELETE'])
def eliminarusuario(member_id):
    miembro_eliminado = jackson_family.delete_member(member_id)
    if not miembro_eliminado:
        return jsonify({"error":"no se elimino el miembro error 400"})
    return jsonify(miembro_eliminado), 200


@app.route('/members', methods=['POST'])
def add_member():
    # This is how you can use the Family datastructure by calling its methods
    newmember = request.json
    jackson_family.add_member(newmember)   
    return jsonify({"done":"Usuario encontrado YUHU" }), 200


# This only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
