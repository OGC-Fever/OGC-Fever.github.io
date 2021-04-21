from flask import Flask

from config import msg

from apps.image_route import *
from apps.info import *
from apps.msg_db import msg_db
from apps.msg import *

msg_db.init_app(msg)
msg_db.create_all()


if __name__ == "__main__":
    msg.run(host="0.0.0.0", debug=True)
