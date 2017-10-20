import os
import json
import subprocess

from flask import Flask, request, render_template, jsonify, redirect, url_for
# conda install -c conda-forge flask-httpauth
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
app.debug = True
auth = HTTPBasicAuth()

users = {
    "hayabusa" : "hayabusa"
}

result_file = '/var/tmp/result.log'
search_engine_path = 'path to search_engine.py'

columns = ["syslog"]
collection = [{columns[0] : ''}]


class BaseDataTables:
    def __init__(self, request, columns, collection):
        self.columns = columns
        self.collection = collection

        # values specified by the datatable for filtering, sorting, paging
        self.request_values = request.values
 
        # results from the db
        self.result_data = None
         
        # total in the table after filtering
        self.cardinality_filtered = 0
 
        # total in the table unfiltered
        self.cadinality = 0
 
        self.run_queries()
    
    def output_result(self):
        output = {}

        aaData_rows = []
        
        for row in self.result_data:
            aaData_row = []
            for i in range(len(self.columns)):
                # print row, self.columns, self.columns[i]
                aaData_row.append(str(row[ self.columns[i] ]).replace('"','\\"'))
            aaData_rows.append(aaData_row)
            
        output['aaData'] = aaData_rows
        
        return output
    
    def run_queries(self):
         self.result_data = self.collection
         self.cardinality_filtered = len(self.result_data)
         self.cardinality = len(self.result_data)


def getCollection():
    tmp_file = '%s-%s' % (result_file, auth.username())

    collection = []
    if os.path.exists(tmp_file):
        file = open(tmp_file)
        collection = [{columns[0] : line.strip()} for line in file]
        file.close()
    else:
        collection = [{columns[0] : ''}]

    return collection

@auth.get_password
def get_pw(username):
    if username in users:
        return users.get(username)
    return None

@app.route('/')
@auth.login_required
def index():
    tmp_file = '%s-%s' % (result_file, auth.username())

    cmd = "/usr/bin/rm %s" % (tmp_file) 
    subprocess.call(cmd, shell=True)

    return render_template('index.html', columns=columns, username=auth.username())

@app.route('/dt')
def get_server_data():
    collection = getCollection()

    results = BaseDataTables(request, columns, collection).output_result()
    
    # return the results as a string for the datatable
    return json.dumps(results)

@app.route('/post', methods=['GET', 'POST'])
def post():
    if request.method == 'POST':
        time = request.form['time']
        keyword = request.form['keyword']

        tmp_file = '%s-%s' % (result_file, auth.username())
        cmd = "%s -e --time %s --match %s | /usr/bin/grep -v -e '^\s*#' -e '^\s*$'  > %s" % (search_engine_path, time, keyword, tmp_file) 
        subprocess.call(cmd, shell=True)

        return render_template('index.html', columns=columns, time=time, keyword=keyword, username=auth.username())
    else:
        return render_template('index.html', columns=columns)


if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.run(host="0.0.0.0", debug=True)
