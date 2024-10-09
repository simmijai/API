from flask import Flask,jsonify
from route1 import bp as main_bp  


app = Flask(__name__)
app.secret_key = 'supersecret'


app.register_blueprint(main_bp)

if __name__ == '__main__':
    app.run(debug=True)


