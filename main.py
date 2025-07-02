from flask import Flask, jsonify, request
import time
from huawei_last_update import get_huawei_info
from juniper_last_update import get_juniper_info

app = Flask(__name__)

def home():
    return jsonify({
        "mensaje": "¡Bienvenido a mi API básica!",
        "estado": "funcionando"
    })

@app.route('/get_updates', methods=['GET'])
async def get_updates():
    info = []
    if request.method in ['GET']:
        if not request.args.get('brand'): brand = ''
        else: brand = request.args.get('brand').lower()
        if not request.args.get('model'): model = ''
        else: model = request.args.get('model').lower()
        match brand:
            case 'huawei':
                info = get_huawei_info(model)
            case 'juniper':
                info = get_juniper_info(['MX10003','PTX10004','QFX5120-32C','EX2200','SRX300'])
            case _:
                info = get_huawei_info(model)
                info2 = get_juniper_info(['MX10003','PTX10004','QFX5120-32C','EX2200','SRX300'])
                for i in info2: info.append(i)
        return jsonify({'info': info})

if __name__ == "__main__":
    try:
        app.run(host='0.0.0.0', port=8002, debug=True)
    except BaseException as e:
        print('BaseException en main: '+str(e))