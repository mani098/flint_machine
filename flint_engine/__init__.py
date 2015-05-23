from flask import Flask
import os
from flask.ext.sqlalchemy import SQLAlchemy

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
app = Flask(__name__, template_folder=tmpl_dir, static_folder=static_dir)

from flint_engine import views
views.DashboardView.register(app, '/')

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://adminlqABQFN:PTMIeHJ8na5S@127.8.129.2/flint'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://adminlqABQFN:PTMIeHJ8na5S@127.0.0.1:3307/flint'
db = SQLAlchemy(app)
BaseModel = db.Model

app.config.from_pyfile('app.cfg')
db.init_app(app)

db.create_all()
