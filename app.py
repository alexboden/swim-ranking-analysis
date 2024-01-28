from database import Database
from flask import Flask
import routes  

db = Database()
app = Flask(__name__)
app.debug = True


