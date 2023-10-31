from urllib import request
import uu
import uuid
from flask_smorest import abort
from flask import Flask, jsonify
from db import stores, items

app = Flask(__name__)


@app.route('/store', methods=['GET'])
def get_stores():
    return jsonify({'stores': list(stores.values())})


@app.route('/store', methods=['POST'])
def create_store():
    store_data = request.get_json()
    if "name" not in store_data:
        abort(400, message='Bad request. Please provide name in json format')
    
    for store in stores.values():
        if store['name'] == store_data['name']:
            abort(409, message='store already exists')
    
    store_id = uuid.uuid4().hex
    store = {**store_data, 'id': store_id
    }
    stores[store_id] = store
    stores.append(store)
    return jsonify(store), 201
    

@app.route('/item', methods=['POST'])
def create_item_in_store(name):
    item_data = request.get_json()

    if(
        "price" not in item_data or
        "store_id" not in item_data or
        "name" not in item_data
    ):
        abort(400, 
        message='Bad request. Please provide price, store_id and name in json format')

    for item in items.values():
        if item['name'] == item_data['name']:
            abort(409, message='item already exists')

    if item_data['store_id'] not in stores:
        abort(404, message='store not found')
    

    
    if item_data['store_id'] not in stores:
        abort(404, message='store not found')
    
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
        abort(404, message='item not found')


@app.route('/item/<string:name>', methods=['DELETE'])
def delete_item(name):
    try:
        del items[int(name)]
        return jsonify({'message': 'item deleted'})
    except IndexError:
        abort(404, message='item not found')


@app.route('/item/<string:item_id>', methods=['PUT'])
def update_item(item_id):
    item_data = request.get_json()
    if "price" not in item_data or "name" not in item_data:
        abort(400, message='Bad request. Please provide price in json format')

    try:
        item = items[int(item_id)]
        item |= item_data
        return jsonify(item)
    except IndexError:
        abort(404, message='item not found')


if __name__ == '__main__':
    app.run(port=5000, debug=True)
