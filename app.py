import random
import shutil
from shutil import copyfile
from dataclasses import dataclass
from flask import Flask, request, render_template, redirect, url_for, session, g, jsonify
from werkzeug.utils import secure_filename
from animal import test_animal as animal
from man import test_man as man
from scenery import test_scenery as scenery
import watermark
import scenery_filter_one as filter1
import scenery_filter_two as filter2
import scenery_filter_three as filter3
import scenery_filter_four as filter4
import scenery_filter_five as filter5
import scenery_filter_six as filter6
import os
import time

app = Flask(__name__)

app.config['SECRET_KEY'] = "sdfklas0lk42j"


@dataclass
class User:
    id: int
    username: str
    password: str


users = [
    User(1, "zl", "0727"),
    User(2, 'gmj', '1002'),
    User(3, '林夕', '0')
]


@app.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        user = [u for u in users if u.id == session['user_id']][0]
        g.user = user


@app.route('/')
def index():
    return redirect(url_for('home_page'))


@app.route('/home_page')
def home_page():
    return render_template("首页.html")


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # 登录操作
        session['animal'] = 0
        session['man'] = 0
        session['scenery'] = 0

        session.pop('user_id', None)
        username = request.form.get("username", None)
        password = request.form.get("password", None)
        user = [u for u in users if u.username == username]
        if len(user) > 0:
            user = user[0]
        if user and user.password == password:
            session['user_id'] = user.id
            return redirect(url_for('do'))

    return render_template("登录.html")


@app.route('/do')
def do():
    return render_template('操作选择.html')


@app.route('/do_man')
def do_man():
    filename='man/colors/color-'+str(session['man'])+'.jpg'

    return render_template('操作-man.html',filename=filename)


@app.route('/do_animal')
def do_animal():
    filename='animal/colors/color-'+str(session['animal'])+'.jpg'

    return render_template('操作-animal.html',filename=filename)


@app.route('/do_scenery')
def do_scenery():
    filename='scenery/colors/color-'+str(session['scenery'])+'.jpg'

    return render_template('操作-scenery.html',filename=filename)


# ---------------人物上色，开始----------------------
@app.route('/upload_man', methods=['POST', 'GET'])
def upload_man():
    if request.method == 'POST':
        filename='man/colors/color-'+str(session['man'])+'.jpg'
        session['man']=1
        f = request.files['file1']
        user_input = request.form.get("name")
        basepath = os.path.dirname(__file__)  # 当前文件所在路径
        upload_path = os.path.join(basepath, 'static/man', 'original.jpg')
        f.save(upload_path)
        copyfile('static/man/original.jpg','static/man/colors/color-'+str(session['man'])+'.jpg')
        return render_template('操作-man.html', userinput=user_input, val1=time.time(),filename=filename)

    return render_template('操作-man.html')


@app.route('/color_man', methods=['POST', 'GET'])
def color_man():
    if request.method == 'POST':
        user_input = request.form.get("color")
        copyfile('static/man/colors/color-'+str(session['man'])+'.jpg','static/man/original/yuantu/original.jpg')
        session['man']+=1
        man.test_man()
        filename = 'man/colors/color-' + str(session['man']) + '.jpg'

        return render_template('操作-man.html', userinput=user_input,filename=filename, val1=time.time())

    return render_template('操作-man.html')


# 水印
@app.route('/watermark_man', methods=['POST', 'GET'])
def watermark_man():
    if request.method == 'POST':
        user_input = request.form.get("color")
        copyfile('static/man/colors/color-' + str(session['man']) + '.jpg',
                 'static/man/original/yuantu/original.jpg')
        session['man'] += 1
        test_path = 'static/man/original/yuantu/original.jpg'
        save_path = 'static/man/colors/color-' + str(session['man']) + '.jpg'
        watermark.addWaterMark(test_path, save_path)
        filename = 'man/colors/color-' + str(session['man']) + '.jpg'

        return render_template('操作-man.html', userinput=user_input, val1=time.time(), filename=filename)

    return render_template('操作-man.html')


@app.route('/withdraw_man',methods=['POST','GET'])
def withdraw_man():
    if request.method=='POST':
        user_input = request.form.get("color")
        if session['man']>1:
            session['man'] -= 1
        filename = 'man/colors/color-' + str(session['man']) + '.jpg'
        return render_template('操作-man.html', userinput=user_input, filename=filename,val1=time.time())

    return render_template('操作-man.html')


@app.route('/download_man',methods=['GET','POST'])
def download_man():
    if request.method=='POST':
        t=random.randint(1,1000)
        filename = 'man/colors/color-' + str(session['man']) + '.jpg'
        copyfile('static/man/colors/color-'+str(session['man'])+'.jpg','static/download_images/'+str(t)+'.jpg')

        return render_template('操作-man.html',filename=filename,val1=time.time())
# ----------------ending------------------------

# -----------动物上色，开始---------------
@app.route('/upload_animal', methods=['POST', 'GET'])
def upload_animal():
    if request.method == 'POST':
        filename = 'animal/colors/color-' + str(session['animal']) + '.jpg'
        session['animal']=1
        f = request.files['file2']
        user_input = request.form.get("name")
        basepath = os.path.dirname(__file__)  # 当前文件所在路径
        upload_path = os.path.join(basepath, 'static/animal', 'original.jpg')
        f.save(upload_path)
        copyfile('static/animal/original.jpg', 'static/animal/colors/color-' + str(session['animal']) + '.jpg')

        return render_template('操作-animal.html', userinput=user_input, val1=time.time(),filename=filename)

    return render_template('操作-animal.html')


@app.route('/color_animal', methods=['POST', 'GET'])
def color_animal():
    if request.method == 'POST':
        user_input = request.form.get("color")
        copyfile('static/animal/colors/color-' + str(session['animal']) + '.jpg','static/animal/original/yuantu/original.jpg')
        session['animal'] += 1
        animal.test_animal()
        filename = 'animal/colors/color-' + str(session['animal']) + '.jpg'

        return render_template('操作-animal.html', userinput=user_input, val1=time.time(),filename=filename)

    return render_template('操作-animal.html')


# 水印
@app.route('/watermark_animal',methods=['POST','GET'])
def watermark_animal():
    if request.method=='POST':
        user_input = request.form.get("color")
        copyfile('static/animal/colors/color-' + str(session['animal']) + '.jpg','static/animal/original/yuantu/original.jpg')
        session['animal'] += 1
        test_path = 'static/animal/original/yuantu/original.jpg'
        save_path = 'static/animal/colors/color-' + str(session['animal']) + '.jpg'
        watermark.addWaterMark(test_path, save_path)
        filename = 'animal/colors/color-' + str(session['animal']) + '.jpg'

        return render_template('操作-animal.html', userinput=user_input, val1=time.time(),filename=filename)

    return render_template('操作-animal.html')


@app.route('/withdraw_animal',methods=['POST','GET'])
def withdraw_animal():
    if request.method=='POST':
        user_input = request.form.get("color")
        if session['animal']>1:
            session['animal'] -= 1
        filename = 'animal/colors/color-' + str(session['animal']) + '.jpg'
        return render_template('操作-animal.html', userinput=user_input, filename=filename,val1=time.time())

    return render_template('操作-animal.html')


@app.route('/download_animal',methods=['GET','POST'])
def download_animal():
    if request.method=='POST':
        t=random.randint(1,1000)
        filename = 'animal/colors/color-' + str(session['animal']) + '.jpg'
        copyfile('static/animal/colors/color-'+str(session['animal'])+'.jpg','static/download_images/'+str(t)+'.jpg')

        return render_template('操作-animal.html',filename=filename,val1=time.time())
# ------------ending--------------------


# -----------------景色上色，滤镜，开始-----------------------
@app.route('/upload_scenery', methods=['POST', 'GET'])
def upload_scenery():
    if request.method == 'POST':
        filename = 'scenery/colors/color-' + str(session['scenery']) + '.jpg'
        session['scenery']=1
        f = request.files['file3']
        user_input = request.form.get("name")
        basepath = os.path.dirname(__file__)
        upload_path = os.path.join(basepath, 'static/scenery', 'original.jpg')
        f.save(upload_path)
        copyfile('static/scenery/original.jpg', 'static/scenery/colors/color-' + str(session['scenery']) + '.jpg')

        return render_template('操作-scenery.html', userinput=user_input, val1=time.time(),filename=filename)

    return render_template('操作-scenery.html')

# 上色
@app.route('/color_scenery', methods=['POST', 'GET'])
def color_scenery():
    if request.method == 'POST':
        user_input = request.form.get("color")
        copyfile('static/scenery/colors/color-'+str(session['scenery'])+'.jpg','static/scenery/original/yuantu/original.jpg')
        session['scenery'] += 1
        scenery.test_scenery()
        filename = 'scenery/colors/color-' + str(session['scenery']) + '.jpg'

        return render_template('操作-scenery.html', userinput=user_input, filename=filename,val1=time.time())

    return render_template('操作-scenery.html')


# 水印
@app.route('/watermark_scenery',methods=['POST','GET'])
def watermark_scenery():
    if request.method=='POST':
        user_input = request.form.get("color")
        copyfile('static/scenery/colors/color-'+str(session['scenery'])+'.jpg','static/scenery/original/yuantu/original.jpg')
        session['scenery'] += 1
        test_path='static/scenery/original/yuantu/original.jpg'
        save_path='static/scenery/colors/color-'+str(session['scenery'])+'.jpg'
        watermark.addWaterMark(test_path,save_path)
        filename = 'scenery/colors/color-' + str(session['scenery']) + '.jpg'
        return render_template('操作-scenery.html', userinput=user_input, filename=filename,val1=time.time())

    return render_template('操作-scenery.html')


# one_边界增强,景色
@app.route('/filter_scenery_one',methods=['POST','GET'])
def filter_scenery_one():
    if request.method=='POST':
        user_input = request.form.get("color")
        copyfile('static/scenery/colors/color-'+str(session['scenery'])+'.jpg','static/scenery/original/yuantu/original.jpg')
        session['scenery']+=1
        filter1.filter(str(session['scenery']))

        filename = 'scenery/colors/color-' + str(session['scenery']) + '.jpg'

        return render_template('操作-scenery.html', userinput=user_input, filename=filename,val1=time.time())
    return render_template('操作-scenery.html')


# two_边缘检测,人，动物，景色（最佳）
@app.route('/filter_scenery_two',methods=['POST','GET'])
def filter_scenery_two():
    if request.method=='POST':
        user_input = request.form.get("color")
        copyfile('static/scenery/colors/color-'+str(session['scenery'])+'.jpg','static/scenery/original/yuantu/original.jpg')
        session['scenery'] += 1
        filter2.filter(str(session['scenery']))

        filename = 'scenery/colors/color-' + str(session['scenery']) + '.jpg'

        return render_template('操作-scenery.html', userinput=user_input,filename=filename, val1=time.time())
    return render_template('操作-scenery.html')


# 3._浮雕滤镜,人，动物，景色（最佳）
@app.route('/filter_scenery_three',methods=['POST','GET'])
def filter_scenery_three():
    if request.method=='POST':
        user_input = request.form.get("color")
        copyfile('static/scenery/colors/color-'+str(session['scenery'])+'.jpg','static/scenery/original/yuantu/original.jpg')
        session['scenery'] += 1
        filter3.filter(str(session['scenery']))

        filename = 'scenery/colors/color-' + str(session['scenery']) + '.jpg'

        return render_template('操作-scenery.html', userinput=user_input,filename=filename, val1=time.time())
    return render_template('操作-scenery.html')


# 4.复古风景滤镜
@app.route('/filter_scenery_four',methods=['POST','GET'])
def filter_scenery_four():
    if request.method=='POST':
        user_input = request.form.get("color")
        copyfile('static/scenery/colors/color-'+str(session['scenery'])+'.jpg','static/scenery/original/yuantu/original.jpg')
        session['scenery'] += 1
        filter4.filter(str(session['scenery']))

        filename = 'scenery/colors/color-' + str(session['scenery']) + '.jpg'

        return render_template('操作-scenery.html', userinput=user_input, filename=filename,val1=time.time())
    return render_template('操作-scenery.html')


# 5.模糊滤镜1（风景）
@app.route('/filter_scenery_five',methods=['POST','GET'])
def filter_scenery_five():
    if request.method=='POST':
        user_input = request.form.get("color")
        copyfile('static/scenery/colors/color-'+str(session['scenery'])+'.jpg','static/scenery/original/yuantu/original.jpg')
        session['scenery'] += 1
        filter5.filter(str(session['scenery']))

        filename = 'scenery/colors/color-' + str(session['scenery']) + '.jpg'

        return render_template('操作-scenery.html', userinput=user_input,filename=filename, val1=time.time())
    return render_template('操作-scenery.html')


# 6.铅笔画滤镜（风景）
@app.route('/filter_scenery_six',methods=['POST','GET'])
def filter_scenery_six():
    if request.method=='POST':
        user_input = request.form.get("color")
        copyfile('static/scenery/colors/color-'+str(session['scenery'])+'.jpg','static/scenery/original/yuantu/original.jpg')
        session['scenery'] += 1
        filter6.filter(str(session['scenery']))
        filename = 'scenery/colors/color-' + str(session['scenery']) + '.jpg'

        return render_template('操作-scenery.html', userinput=user_input, filename=filename,val1=time.time())
    return render_template('操作-scenery.html')


@app.route('/scenery_withdraw',methods=['POST','GET'])
def scenery_withdraw():
    if request.method=='POST':
        user_input = request.form.get("color")
        if session['scenery']>1:
            session['scenery'] -= 1
        filename = 'scenery/colors/color-' + str(session['scenery']) + '.jpg'
        return render_template('操作-scenery.html', userinput=user_input, filename=filename,val1=time.time())

    return render_template('操作-scenery.html')

@app.route('/download_scenery',methods=['GET','POST'])
def download_scenery():
    if request.method=='POST':
        t=random.randint(1,1000)
        filename = 'scenery/colors/color-' + str(session['scenery']) + '.jpg'
        copyfile('static/scenery/colors/color-'+str(session['scenery'])+'.jpg','static/download_images/'+str(t)+'.jpg')

        return render_template('操作-scenery.html',filename=filename,val1=time.time())

    return render_template('操作-scenery.html')

# ---------------ending------------------------------

if __name__ == '__main__':
    app.run()
