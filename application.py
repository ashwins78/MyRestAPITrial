import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app_initialized = False
application = create_app()
#application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
#db = SQLAlchemy(application)

def create_app(test_config=None):
    app = Flask(__name__)
    #app.config.from_mapping(
    #    SECRET_KEY='dev',
    #    DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    #)

    #if test_config is None:
        # load the instance config, if it exists, when not testing
    #    app.config.from_pyfile('config.py', silent=True)
    #else:
        # load the test config if passed in
    #    app.config.from_mapping(test_config)

    #try:
    #    os.makedirs(app.instance_path)
    #except OSError:
    #    pass

    app_initialized = True
    return app
#class Bag(db.Model):
#    id = db.Column(db.Integer, primary_key=True)
#    name = db.Column(db.String(10), unique=True, nullable=False)
#    use_count = db.Column(db.Integer)

#    def __repr__(self):
#       return f"{self.id} - {self.name} - {self.use_count}"

@application.route('/')
def index():
    if app_initialized is True:
        return 'REST WEB SERVER'
    else:
        return 'Uninitialized wed server'
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

#main_called = False
if __name__ == '__main__':
    application.run()
