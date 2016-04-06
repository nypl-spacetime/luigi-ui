import luigi
import pkgutil
import inspect
import importlib
import os
import json
import subprocess

from flask import Flask, jsonify, Response, request
app = Flask(__name__)

config = json.loads(open('./config.json').read())

tasks = []

for package_name in config['packages']:
    package = importlib.import_module(package_name)
    prefix = package.__name__ + '.'
    for importer, modname, ispkg in pkgutil.iter_modules(package.__path__, prefix):
        module_tasks = []
        module = __import__(modname, fromlist="dummy")
        for name, obj in inspect.getmembers(module):
            if inspect.isclass(obj):
                parameters = []
                for name, param in inspect.getmembers(obj):
                    if isinstance(getattr(obj, name), luigi.parameter.Parameter):
                        parameters.append({
                            'name': name,
                            'type': type(param).__name__,
                            'default': getattr(obj, name)._default
                        })

                if isinstance(obj(), luigi.task.Task):
                    module_tasks.append({'class': obj.__name__, 'parameters': parameters})

        tasks.append({'module': modname, 'tasks': module_tasks})

@app.route('/')
def send_js():
    return app.send_static_file('index.html')

@app.route('/tasks', methods=['GET'])
def get_tasks():
    return Response(json.dumps(tasks),  mimetype='application/json')

@app.route('/tasks', methods=['POST'])
def start_task():
    data = request.json
    # TODO: see if data contains module + class, both should exist in tasks

    cmd = 'luigi --module {} {}'.format(
        data['module'], data['class'])
    subprocess.Popen(cmd.split())

    return Response(json.dumps({'success': True}),  mimetype='application/json')

if __name__ == '__main__':
    port = os.environ.get('PORT') or config['port']
    app.run(host='0.0.0.0', port=port)
