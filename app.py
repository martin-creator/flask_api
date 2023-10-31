from urllib import request
import uu
import uuid
from flask import Flask, jsonify
from db import stores, items

app = Flask(__name__)


@app.route('/store', methods=['GET'])
def get_stores():
    return jsonify({'stores': list(stores.values())})


@app.route('/store', methods=['POST'])
def create_store():
    store_data = request.get_json()
    store_id = uuid.uuid4().hex
    store = {**store_data, 'id': store_id
    }
    stores[store_id] = store
    stores.append(store)
    return jsonify(store), 201
    

@app.route('/item', methods=['POST'])
def create_item_in_store(name):
    item_data = request.get_json()
    if item_data['store_id'] not in stores:
        return jsonify({'message': 'store not found'}), 404
    
    item_id = uuid.uuid4().hex
    item = {**item_data, 'id': item_id}
    items[item_id] = item
    return jsonify(item), 201


@app.route('/items', methods=['GET'])
def get_all_items():
    return jsonify({'items': list(items.values())})


@app.route('/store/<string:store_id>', methods=['GET'])
def get_store(store_id):
    try:
        return jsonify(stores[int(store_id)])
    except IndexError:
        return jsonify({'message': 'store not found'}), 404

@app.route('/item/<string:name>/item_id', methods=['GET'])
def get_item(item_id):
    try:
        return jsonify(items[int(item_id)])
    except IndexError:
        return jsonify({'message': 'item not found'}), 404



if __name__ == '__main__':
    app.run(port=5000, debug=True)
