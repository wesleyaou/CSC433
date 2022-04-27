from flask import Flask

app = Flask(__name__, static_folder="web/static", template_folder="web/templates")
app.config['SECRET_KEY'] = 'a_plus_labs'
app.config['SECURITY_PASSWORD_HASH'] = 'bcrypt'