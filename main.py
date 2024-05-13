import json
import os
import requests

class Request_index:
    def _read():
        with open('data/request_index.json') as f:
            index = json.load(f)
        return index
    

    def _write(index):
        print(f"writing index: {index}")
        with open('data/request_index.json', 'w') as f:
            json.dump(index, f, indent=6)
        return True
    

    def get_list():
        index = Request_index._read()
        result = []
        for key, value in index.items():
            result.append(key)
        return result


    def get_id(name):
        index = Request_index._read()
        return index[name]
    

    def get_last():
        index = Request_index._read()
        _key = []
        _value = []
        for key, value in index.items():
            _key.append(key)
            _value.append(value)
        return _value[-1]
    

    def generate_id():
        last = Request_index.get_last()
        new = str(int(last) + 1)
        while len(new) != 9:
            new = '0' + new
        return new
    

    def update(name, id):
        print(f'UPDATING INDEX: {name}: {id}')
        index = Request_index._read()
        index.update({name: id})
        response = Request_index._write(index)
        return response


    def new(name):
        id = Request_index.generate_id()
        response = Request_index.update(name, id)
        return response


class Config:
    def get(name):
        data = Config.read()
        for line in data:
            if '=' in line:
                line = line.split('=')
                if line[0].upper() == name.upper():
                    return line[1]
    

    def read():
        data = open('config.cfg', 'r').readlines()
        for i in range(len(data)):
            data[i] = data[i].replace('\n', '')
        return data
    

class Data:
    def write(id, url, method, headers, datajson):
        open(f'{Config.get('RequestsDataFolder')}/{id}/url.data', 'w').writelines(url)
        open(f'{Config.get('RequestsDataFolder')}/{id}/method.data', 'w').writelines(method)
        open(f'{Config.get('RequestsDataFolder')}/{id}/headers.data', 'w').writelines(headers)
        with open(f'{Config.get('RequestsDataFolder')}/{id}/datajson.json', 'w') as f:
            json.dump(datajson, f, indent=6)
        return True
    

    def load(id):
        url = open(f'{Config.get('RequestsDataFolder')}/{id}/url.data', 'r').readline()
        method = open(f'{Config.get('RequestsDataFolder')}/{id}/method.data', 'r').readline()
        headers = open(f'{Config.get('RequestsDataFolder')}/{id}/headers.data', 'r').readline()
        with open(f'{Config.get('RequestsDataFolder')}/{id}/datajson.json') as f:
            datajson = json.load(f)
        return url, method, headers, datajson
    

    def transform_to_dict(var):
        result = {}
        if ',' in var:
            items = var.split(',')
        else:
            items = [var]
        for item in items:
            if '=' in item:
                item = item.split('=')
                key = item[0]
                value = item[1]
                result.update({key: value})
        return result




class Save:
    def new(name, url, method, headers, datajson):
        Request_index.new(name)
        id = Request_index.get_id(name)
        os.makedirs(f'{Config.get('RequestsDataFolder')}/{id}')
        Data.write(id, url, method, headers, datajson)
        return True


    def load(name):
        id = Request_index.get_id(name)
        url, method, headers, datajson = Data.load(id)
        return url, method, headers, datajson
    

    def update(name, url, method, headers, datajson):
        try:
            id = Request_index.get_id(name)
        except Exception:
            Request_index.new(name)
            id = Request_index.get_id(name)
        Data.write(id, url, method, headers, datajson)
        return True
    

    def clear():
        path = (f'{os.getcwd()}/{Config.get('RequestsDataFolder')}').replace('/', '\\')
        if Config.get('debug') == '1':
            print(f'DELETING ALL FILES AND FOLDERS IN {path}')
        os.system(f'rmdir /s /q \"{path}\"')
        os.makedirs(path)
        return True

class Requests:
    def make(name):
        url, method, headers, datajson = Save.load(name)
        if method == 'GET':
            req = requests.get(url, headers=Data.transform_to_dict(headers))
            code = req.status_code
            content = req.content
            return code, content
        elif method == 'POST':
            req = requests.post(url, headers=Data.transform_to_dict(headers), json=datajson)
            code = req.status_code
            content = req.content
            return content
        else:
            return 'UnsupportedRequest'
