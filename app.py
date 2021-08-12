from bson import json_util
from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient

from bson.objectid import ObjectId

#client = MongoClient('localhost', 27017)
client = MongoClient('mongodb://test:test@localhost', 27017)
db = client.dbmemory

@app.route('/')
def home():
   return render_template('index.html')

## API 역할을 하는 부분
@app.route('/memory_register', methods=['POST'])
def register_memory():
    latitude_receive = request.form['latitude_give']
    longitude_receive = request.form['longitude_give']
    title_receive = request.form['title_give']
    writer_receive = request.form['writer_give']
    comment_receive = request.form['comment_give']
    image_receive = request.form['image_give']
    id_receive = request.form['id_give']

    dic = {
        'latitude': latitude_receive,
        'longitude': longitude_receive,
        'title': title_receive,
        'writer': writer_receive,
        'comment': comment_receive,
        'image': image_receive
    }

    if id_receive == '' :
        db.memory.insert_one(dic)
        msg = "등록 완료!"
    else :
        db.memory.update_one ({"_id": ObjectId(id_receive)}, { '$set': {'title': title_receive,'writer': writer_receive,'comment': comment_receive,'image': image_receive}})
        msg = "수정 완료!"

    return jsonify({'msg': msg})


@app.route('/memory_read', methods=['GET'])
def read_memory():
    markers = objectIdDecoder(list(db.memory.find({})))

    return jsonify({'all_markers': markers})

def objectIdDecoder(list):
    results=[]
    for document in list:
        document['_id'] = str(document['_id'])
        results.append(document)
    return results

@app.route('/memory_delete', methods=['POST'])
def delete_memory():
    id_receive = request.form['id_give']

    db.memory.delete_one({"_id": ObjectId(id_receive)})

    return jsonify({'msg': '삭제 완료!'})

if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)