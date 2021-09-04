import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app(test_config=None):
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
        database_url = 'sqlite:///' + os.path.join(app.instance_path, 'test.db')

    app.config.from_mapping(
        SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev_key',
        SQLALCHEMY_DATABASE_URI = database_url,
        SQLALCHEMY_TRACK_MODIFICATIONS = False
    )

    db.init_app(app)
    return app

application = create_app()

class Bag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), unique=True, nullable=False)
    use_count = db.Column(db.Integer)

    def __repr__(self):
       return f"{self.id} - {self.name} - {self.use_count}"

@application.route('/')
def index():
    return 'REST WEB SERVER'

#@application.route('/bags')
#def get_bags():
#    result = []

#    bags = Bag.query.all()
#    for bag in bags:
#        bag_data = {'id': bag.id, 'name': bag.name, 'use_count': bag.use_count}
#        result.append(bag_data)

#    return {"bags" : result}

#@application.route('/bags/<id>')
#def get_bag(id):
#    bag = Bag.query.get(id)
#    if bag is None:
#        return {"error": "Unknown bag id"}

#    bag_data = {'id': bag.id, 'name': bag.name, 'use_count': bag.use_count}
#    return {"bag": bag_data}

#@application.route('/bags/<id>', methods=['PUT'])
#def bag_used(id):
#    bag = Bag.query.get(id)
#    if bag is None:
#        return {"error": "Unknown bag id"}

#    bag.use_count = Bag.use_count + 1
#    db.session.commit()

    #bag = Bag.query.get(id)
    #bag_data = {'id': new_bag.id, 'name': new_bag.name, 'use_count': new_bag.use_count}

#    bag_data = {'id': bag.id, 'name': bag.name, 'use_count': bag.use_count}
#    return {"result": bag_data}

if __name__ == '__main__':
    application.run()
