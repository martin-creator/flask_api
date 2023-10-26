from flask import Flask, jsonify


app = Flask(__name__)

stores = [
    {
        'name': 'My Wonderful Store',
        'items': [
            {
                'name': 'My Item',
                'price': 15.99
            }
        ]
    }
]

@app.route('/store', methods=['GET'])
def get_stores():
    return jsonify({'stores': stores})