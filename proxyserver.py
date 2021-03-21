from flask import Flask,request,redirect,Response
import requests
from sql import Check_is_sql

app = Flask(__name__)
SITE_NAME = 'http://localhost:8000'

@app.route('/')
def index():
    return 'Flask is running!'

@app.route('/<path:path>',methods=['GET','POST','DELETE'])
def proxy(path):
    global SITE_NAME
    if request.method=='GET':
        resp = requests.get(f'{SITE_NAME}/{path}')
        print("path - " + path)
        res = Check_is_sql(path)
        print(res)
        if res == 1:
            print ("[SQL-Injection]: %s" % path)
            return "SQL Injection"
        else:
            excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
            headers = [(name, value) for (name, value) in  resp.raw.headers.items() if name.lower() not in excluded_headers]
            response = Response(resp.content, resp.status_code, headers)
            return response
    elif request.method=='POST':
        resp = requests.post(f'{SITE_NAME}/{path}',json=request.get_json())
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        headers = [(name, value) for (name, value) in resp.raw.headers.items() if name.lower() not in excluded_headers]
        response = Response(resp.content, resp.status_code, headers)
        return response
    elif request.method=='DELETE':
        resp = requests.delete(f'{SITE_NAME}/{path}').content
        response = Response(resp.content, resp.status_code, headers)
        return response
        
if __name__ == '__main__':
    app.run(debug = False,port=80)