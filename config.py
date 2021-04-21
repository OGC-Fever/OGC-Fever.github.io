from flask.app import Flask

msg = Flask(__name__)
# msg.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/message.db'
msg.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
msg.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
msg.config['JSON_AS_ASCII'] = False
