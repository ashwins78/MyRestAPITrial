import os
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *

database_url = None

def create_app(test_config=None):
    global database_url

    app = Flask(__name__)
    if 'RDS_HOSTNAME' in os.environ:
        print('Using rds db')
        DATABASE = {
            'NAME': os.environ['RDS_DB_NAME'],
            'USER': os.environ['RDS_USERNAME'],
            'PASSWORD': os.environ['RDS_PASSWORD'],
            'HOST': os.environ['RDS_HOSTNAME'],
            'PORT': os.environ['RDS_PORT'],
        }
        database_url = 'postgresql://' + DATABASE['USER']
        database_url += ':' + DATABASE['PASSWORD']
        database_url += '@' + DATABASE['HOST']
        database_url += ':' + DATABASE['PORT']
        database_url += '/' + DATABASE['NAME']

    else:
        print('Using local db')
        DATABASE = {
            'NAME': "asampath",
            'HOST': "localhost",
            'PORT': "5432",
        }
        database_url = 'postgresql://'
        database_url += DATABASE['HOST']
        database_url += ':' + DATABASE['PORT']
        database_url += '/' + DATABASE['NAME']

    print(database_url)

    app.config.from_mapping(
        SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev_key',
        SQLALCHEMY_DATABASE_URI = database_url,
        SQLALCHEMY_TRACK_MODIFICATIONS = False
    )

    return app

application = create_app()

def init_db():
    global application

    db = SQLAlchemy(application)
    return db

db = init_db()

class ProdBag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), unique=True, nullable=False)
    use_count = db.Column(db.Integer)

    def __repr__(self):
       return f"{self.id} - {self.name} - {self.use_count}"

def init_db_tables():
    global db
    tbl_names = db.engine.table_names()


    #bag1 = ProdBag(name = "bag1", use_count = 0)
    #db.session.add(bag1)
    #db.session.commit()

    if (len(tbl_names) == 0):
        db.create_all()
        bag1 = ProdBag(name = "bag1", use_count = 0)
        db.session.add(bag1)
        db.session.commit()
    else:
        print(tbl_names)

init_db_tables()

@application.route('/')
def index():
    return 'REST WEB SERVER'

@application.route('/bags')
def get_bags():
    result = []
    bags = ProdBag.query.all()
    for bag in bags:
        bag_data = {'id': bag.id, 'name': bag.name, 'use_count': bag.use_count}
        result.append(bag_data)

    return {"bags" : result}

@application.route('/bags/<id>')
def get_bag(id):
    bag = ProdBag.query.get(id)
    if bag is None:
        return {"error": "Unknown bag id"}

    bag_data = {'id': bag.id, 'name': bag.name, 'use_count': bag.use_count}
    return {"bag": bag_data}

@application.route('/bags', methods=['POST'])
def add_bag():
    bag_nm = request.json['name']
    bag = ProdBag(name = bag_nm, use_count = 1)
    db.session.add(bag)
    db.session.commit()

    bag_data = {}
    bag = ProdBag.query.filter_by(name=bag_nm).first()
    if not bag is None:
        bag_data = {'id': bag.id, 'name': bag.name, 'use_count': bag.use_count}

    return {"bag": bag_data}

@application.route('/bags/<id>', methods=['PUT'])
def bag_used(id):
    bag = ProdBag.query.get(id)
    if bag is None:
        return {"error": "Unknown bag id"}

    bag.use_count = ProdBag.use_count + 1
    db.session.commit()

    bag = ProdBag.query.get(id)
    bag_data = {'id': bag.id, 'name': bag.name, 'use_count': bag.use_count}
    return {"result": bag_data}

if __name__ == '__main__':
    application.run()
