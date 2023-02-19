from flask import Flask, request, make_response, jsonify
from flask_mongoengine import MongoEngine
from marshmallow import Schema, fields, post_load
from bson import ObjectId

app = Flask(__name__)

app.config['MONGODB_SETTINGS'] = {
    'db': 'authors',
    'host': 'mongodb',
    'port': 27017,
    'username': 'root',
    'password': 'pass'
}

db = MongoEngine(app)

Schema.TYPE_MAPPING[ObjectId] = fields.String

class Authors(db.Document):
    name = db.StringField()
    specialisation = db.StringField()

class AuthorsSchema(Schema):
    id = fields.String(dump_only=True)
    name = fields.String(required=True)
    specialisation = fields.String(required=True)

@app.route('/authors', methods=['GET'])
def index():
    get_authors = Authors.objects.all()
    author_schema = AuthorsSchema(many=True)
    authors = author_schema.dump(get_authors)
    return make_response(jsonify({'authors': authors}))


@app.route('/authors/<id>', methods=['GET'])
def get_author_by_id(id):
    get_author = Authors.objects.get(id=ObjectId(id))
    author_schema = AuthorsSchema()
    author = author_schema.dump(get_author)
    return make_response(jsonify({'author': author}))

@app.route('/authors', methods=['POST'])
def create_author():
    data = request.get_json()
    new_author = Authors(name=data['name'], specialisation=data['specialisation'])
    new_author.save()
    author_schema = AuthorsSchema()
    author = author_schema.dump(new_author)
    return make_response(jsonify({'author': author}), 201)

@app.route('/authors/<id>', methods=['PUT'])
def update_author_by_id(id):
    data = request.get_json()
    get_author = Authors.objects.get(id=ObjectId(id))
    if data.get('name'):
        get_author.name = data['name']
    if data.get('specialisation'):
        get_author.specialisation = data['specialisation']
    get_author.save()
    get_author.reload()
    author_schema = AuthorsSchema()
    author = author_schema.dump(get_author)
    return make_response(jsonify({'author': author}))

@app.route('/authors/<id>', methods=['DELETE'])
def delete_author_by_id(id):
    Authors.objects(id=ObjectId(id)).delete()
    return make_response('', 204)

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
