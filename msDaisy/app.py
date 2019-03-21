from flask import Flask, jsonify


app = Flask(__name__)


@app.route('/hello', methods=['GET'])

def hello_world():

    hello = "Hello, World!"

    return(hello)


#ERROR ROUTE
@app.errorhandler(404)

def not_found(error):
	return jsonify({'code':404,'message': 'Not Found'}),404


if (__name__ == "__main__"):
    app.run(host='0.0.0.0', port=5003)
