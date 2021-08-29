#import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

application = Flask(__name__)
application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(application)

class Bag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), unique=True, nullable=False) 
    use_count = db.Column(db.Integer)

    def __repr__(self):
       return f"{self.id} - {self.name} - {self.use_count}"

@application.route('/')
def index():
    return 'MyWebserver!'

@application.route('/bags')
def get_bags():
    bags = Bag.query.all()

    result = []

    for bag in bags:
        bag_data = {'id': bag.id, 'name': bag.name, 'use_count': bag.use_count}
        result.append(bag_data)

    return {"bags" : result}

#@application.route('/bags/<id>')
#def get_bag(id):
#    bag = Bag.query.get(id)
#    if bag is None:
#        return {"error": "Unknown bag id"}
#
#    bag_data = {'id': bag.id, 'name': bag.name, 'use_count': bag.use_count}
#    return {"bag": bag_data}

#@application.route('/bags/<id>', methods=['PUT'])
#def bag_used(id):
#    bag = Bag.query.get(id)
#    if bag is None:
#        return {"error": "Unknown bag id"}
#
#    bag.use_count = Bag.use_count + 1
#    db.session.commit()
#
#    #bag = Bag.query.get(id)
#    #bag_data = {'id': new_bag.id, 'name': new_bag.name, 'use_count': new_bag.use_count}
#
#    bag_data = {'id': bag.id, 'name': bag.name, 'use_count': bag.use_count}
#    return {"result": bag_data}
