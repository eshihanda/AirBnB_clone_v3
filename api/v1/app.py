#!/usr/bin/python3
"""
create a flask api and mark its blueprint to an instance
"""

from flask import Flask
from models import storage
from os import getenv
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(self):
    """
    closes current db session
    """
    storage.close()


if __name__ == '__main__':
    host_vr = getenv('HBNB_API_HOST', '0.0.0.0')
    port_vr = int(getenv('HBNB_API_PORT', 5000))
    app.run(host=host_vr, port=port_vr, threaded=True)
