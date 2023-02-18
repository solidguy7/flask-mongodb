from flask import Flask, request, make_response, jsonify
from flask_mongoengine import MongoEngine
from marshmallow import Schema, fields, post_load
from bson import ObjectId

app = Flask(__name__)
app.config['MONGODB_DB'] = 'authors'
db = MongoEngine(app)

Schema.TYPE_MAPPING[ObjectId] = fields.String

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
