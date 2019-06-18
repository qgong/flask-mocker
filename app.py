#import argparse
import json
import os
import re
import uuid
#from flaskext.xmlrpc import XMLRPCHandler, Fault

from flask import Flask, render_template, request, redirect
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__, static_url_path='')
#handler = XMLRPCHandler('api')
#handler.connect(app, '/api')
api = Api(app)

#@handler.register
def hello(name="world"):
    if not name:
        raise Fault("unknown_recipient", "I need someone to greet!")
    return "Hello, %s!" % name

class Rpl(Resource):
    def get(self, pv, nvr):
        filename = "data_pl_rpm.json"
        if not os.path.exists(filename):
            raise FileNotFoundError("File '{}' not found!".format(filename))
        with open(filename, 'r') as f:
            data = json.load(f)
        new_no = nvr.split(".")[-2]
        s1 = re.sub(r'20.el7_2', new_no + '.el7_2', str(data))
        new_data = s1.replace("\'", "\"")
        new_data= json.loads(new_data)
        return new_data                

class Mpl(Resource):
    def get(self, pv, nvr):
        filename = "data_pl_module.json"
        if not os.path.exists(filename):
            raise FileNotFoundError("File '{}' not found!".format(filename))
        with open(filename, 'r') as f:
            return json.load(f)  

class ModulelMd(Resource):
    def get(self, package, arch_txt):
        
        #import pdb; 
        #pdb.set_trace()
        #import yaml
        #filename = "data_modulemd." + "i686.txt"
        #return redirect("http://download.eng.bos.redhat.com/brewroot/packages/rust-toolset/rhel8/8000120190530030816.4f19bdec/files/module/modulemd." + arch_txt)
        #return app.send_static_file(filename)
        #return app.send_file(filename, )

        #http://download.eng.bos.redhat.com/brewroot/packages/rust-toolset/rhel8/8000120190530030816.4f19bdec/files/module/modulemd.i686.txt
        #return app.send_file(filename)

        #print("filename:",filename)
        #return send_from_directory(app.config['UPLOAD_FOLDER'],
                             #  filename, as_attachment=True)
        #return send_file("data_modulemd.aarch64.txt", attachment_filename='python.jpg)
        #pdb.set_trace()
        #if arch_txt == 'modulemd.i686.txt':
        return app.send_static_file('data_modulemd.' + arch_txt)


api.add_resource(Rpl, '/api/v1.0/product-listings/<string:pv>/<string:nvr>')
api.add_resource(Mpl, '/api/v1.0/module-product-listings/<string:pv>/<string:nvr>')
api.add_resource(ModulelMd, '/brewroot/packages/<string:package>/rhel8/8000120190530030816.4f19bdec/files/module/modulemd.<string:arch_txt>')
                             #/brewroot/packages/rust-toolset/rhel8/8000120190530030816.4f19bdec/files/module/modulemd.i686.txt   
#api.add_resource(ModulelMd, '/brewroot/packages/rust-toolset/rhel8/8000120190530030816.4f19bdec/files/module/modulemd.i686.txt')


if __name__ == '__main__':
    app.run(debug=False, port=5000, host='mock-e2e.usersys.redhat.com')
