#!/usr/bin/env python
#-*- coding = utf-8 -*-


from flask import Flask, render_template, request, redirect, url_for, flash
from flask_script import Manager
from config import *

app = Flask(__name__)
manager = Manager(app=app)
app.config.from_object(__name__)

@app.route('/')
def list():
    db = SQLManager()
    users = db.get_list('select * from user')
    db.close()
    return render_template('list_users.html', users=users)

@app.route('/add', methods=['GET','POST'])
def add():
    if request.method == 'POST':
        name = request.form.get('user_name')
        age = request.form.get('user_age')
        db = SQLManager()
        db.moddify("insert into user(name, age) values ('%s', '%s');" %(name, age))
        db.close()
        return redirect(url_for('list'))
    return render_template('add.html')

@app.route('/dele/<user_id>')
def dele(user_id):
    db = SQLManager()
    user = db.get_list("select * from user where id='%s';" %(user_id))
    #print(user)
    if user:
        try:
            db.moddify("delete from user where id=%s;" %(user_id))
            db.close()
        except Exception as e:
            print(e)
    else:
        print('没有这个用户')
        return redirect(url_for('list'))
    return redirect(url_for('list'))

#@app.route('/upp/<user_id>')
#def upp(user_id):
    #db = SQLManager()
    #user = db.get_list("select * from user where id='%s';" % (user_id))
    #db.moddify("update user set name='%s' age='%s' where id=%s;" %(up_name, up_age, user_id))
    #up_name = request.form.get('up_name')
        #up_age = request.form.get('up_age')
        #db = SQLManager()
        #db.moddify("update user set name='%s' age='%s' where id=%s;" %(up_name, up_age, user_id))

        #return redirect(url_for('list'))
    #return render_template('up.html')
    #return redirect(url_for('add'))
if __name__ == '__main__':
    manager.run()