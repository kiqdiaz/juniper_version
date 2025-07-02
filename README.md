1. Instala requirements.txt en tu entorno de desarrollo: 
    pip -r install requirements.txt
2. Ejecuta el archivo python con los modelos exactos como argumentos: 
    python main.py
3. Para activar la API:
    curl -i -H "Content-Type: application/json" -X GET http://127.0.0.1:8002/get_updates?brand=juniper
    curl -i -H "Content-Type: application/json" -X GET http://127.0.0.1:8002/get_updates?brand=huawei
    curl -i -H "Content-Type: application/json" -X GET http://127.0.0.1:8002/get_updates