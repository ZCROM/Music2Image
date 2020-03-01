import json
import multiprocessing
import os
import sys
from flask import Flask, request, url_for, send_from_directory, render_template
from werkzeug.utils import secure_filename
music_list=[
"https://img-blog.csdnimg.cn/20200229122438603.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2VoZGhnMTM0NTU=,size_16,color_FFFFFF,t_70",
"https://img-blog.csdnimg.cn/20200229124021799.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2VoZGhnMTM0NTU=,size_16,color_FFFFFF,t_70",
"https://img-blog.csdnimg.cn/20200229124209943.PNG?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2VoZGhnMTM0NTU=,size_16,color_FFFFFF,t_70",
"https://img-blog.csdnimg.cn/20200229124252957.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2VoZGhnMTM0NTU=,size_16,color_FFFFFF,t_70",
"https://img-blog.csdnimg.cn/2020022912432571.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2VoZGhnMTM0NTU=,size_16,color_FFFFFF,t_70",
"https://img-blog.csdnimg.cn/20200229124431643.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2VoZGhnMTM0NTU=,size_16,color_FFFFFF,t_70"
]
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'PUT,GET,POST,DELETE'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
    return response
app = Flask(__name__)
app.after_request(after_request)
app.config['UPLOAD_FOLDER'] = os.getcwd()
ALLOWED_EXTENSIONS = set(['wav'])
testInfo = {}
num=0;
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)
ccnt = 0;
@app.route('/greet123456789', methods=['GET', 'POST'])
def greet_json():
 if (request.method == 'POST'):
     '''receive data'''
     recv_data = request.get_data()
     json_re = json.loads(recv_data)
     if recv_data:
         print: recv_data
         print: json_re['email']
         print: json_re['phone']
     else:
         print("receive data is empty")
     '''send data'''
     f =  open('exchange.txt', 'r')
     line = 0
     for line in f:
         a = 1
     f.close()
     testInfo['name'] = music_list[min(int(line)-1,int(json_re['email'])) ]
     testInfo['age'] = str(min(int(line)-1,int(json_re['email'])))
     return json.dumps(testInfo)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if (request.method == 'POST')  :
         print("debug1")
         file = request.files['file']
         if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            #file.save(os.path.join(app.config['UPLOAD_FOLDER']))
            import  Music2ImageAI
            p = multiprocessing.Process(target=Music2ImageAI.test2)
            print('process start')
            p.start()

    return render_template("localmusic.html")

if __name__ == '__main__':
    f = open('exchange.txt', 'r+')
    f.truncate();
    f.close()
    app.run(debug=True)