# import subprocess
# from flask import Flask, request, render_template
# app = Flask(__name__)

# @app.route('/')
# def hello_world():
#     comando = "VBoxManage modifyvm Ubuntu\\ 1 --memory 512 --vram 32 --boot1 dvd"

#     process = subprocess.Popen(comando, stdout=subprocess.PIPE, shell=True)
#     # espera por 2 minutos
#     out, err = process.communicate(timeout=120) 
#     print(out)
#     return (out)
# if __name__ == '__main__':
#     app.run(host='127.0.0.1', port='5000', debug=True)

# from flask import Flask, render_template, flash, request
# from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField

# # App config.
# DEBUG = True
# app = Flask(__name__)
# app.config.from_object(__name__)
# app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

# class ReusableForm(Form):
#     name = TextField('Name:', validators=[validators.required()])
    
#     @app.route("/", methods=['GET', 'POST'])
#     def hello():
#         form = ReusableForm(request.form)
        
#         print (form.errors)
#         if (request.method == 'POST'):
#             name=request.form['name']
#             print (name)
        
#         if (form.validate()):
#         # Save the comment here.
#             flash('Hello ' + name)
#         else:
#             flash('Error: All the form fields are required. ')
        
#         return render_template('vm.html', form=form)

# if __name__ == "__main__":
#     app.run(port=3000, use_reloader=True)

# from flask import Flask, render_template, flash, request
# from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField

# # App config.
# DEBUG = True
# app = Flask(__name__)
# app.config.from_object(__name__)
# app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

# class ReusableForm(Form):
#     name = TextField('Name:', validators=[validators.required()])
#     email = TextField('Email:', validators=[validators.required(), validators.Length(min=6, max=35)])
#     password = TextField('Password:', validators=[validators.required(), validators.Length(min=3, max=35)])
    
#     @app.route("/", methods=['GET', 'POST'])
#     def hello():
#         form = ReusableForm(request.form)
    
#         print (form.errors)
#         if request.method == 'POST':
#             name=request.form['name']
#             password=request.form['password']
#             email=request.form['email']
#             print (name, " ", email, " ", password)
    
#         if form.validate():
#         # Save the comment here.
#             flash('Thanks for registration ' + name)
#         else:
#             flash('Error: All the form fields are required. ')
    
#         return render_template('vm.html', form=form)

# if __name__ == "__main__":
#     app.run()

# from flask import Flask
# import subprocess
# import os 
# from flask_wtf import FlaskForm
# from wtforms import StringField, IntegerField
# from wtforms.validators import DataRequired

# app = Flask(__name__)

# @app.route("/")

# def hello():
#     myCmd = "VBoxManage modifyvm Ubuntu --memory 4096 --vram 32 --boot1 dvd"
#     os.system (myCmd)
#     return "Ok"

# @app.rout("/form")

# def MyForm(FlaskForm):
#     name = StringField('name', validators=[DataRequired()])
#     age = InterField('age', validators=[DataRequired()])

# if __name__ == "__main__" :
#     app.run()

from flask import Flask, render_template, redirect, jsonify
from flask import request
import subprocess, json
import shlex
import urllib.parse
import shell
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField

app = Flask(__name__)

class ReusableForm(Form):
    so = TextField('Sistema Operacional:', validators=[validators.required()])
    memoria = TextField('Quantidade de memória:', validators=[validators.required(), validators.Length(min=512, max=4096)])
    cpus = TextField('Quantidade de CPUs:', validators=[validators.required(), validators.Length(min=1, max=2)])
    nome_clone = TextField('Nome da VM:', validators=[validators.required(), validators.Length(min=11, max=11)])
    ip = TextField('IP:', validators=[validators.required()])
    num_maq = TextField('Número da Máquina:', validators=[validators.required()])

@app.route("/",methods = ['POST', 'GET'])
def index():
    form = ReusableForm(request.form)
    return render_template("vm.html",form=form)

@app.route("/vm", methods = ['POST'])
def execute():
    if request.method == 'POST':
        #result = request.form.to_dict(flat=True)
        memoria=request.form['memoria']
        so=request.form['so']
        nome_clone=request.form['nome_clone']
        cpus=request.form['cpus']
        ip=request.form['ip']
        num_maq=request.form['num_maq']
        #shell.exec(comando+' list vms').communicate()
        # shell.exec('VBoxManage hostonlyif create && VBoxManage hostonlyif ipconfig vboxnet'+str(num_maq)+' --ip '+str(ip)+' && VBoxManage modifyvm Ubuntu --hostonlyadapter1 vboxnet'+str(num_maq)+' && VBoxManage modifyvm Ubuntu --nic1 hostonly && VBoxManage modifyvm Ubuntu --cpus '+str(cpus)+' --memory '+str(memoria)+' --vram 32 --boot1 dvd && VBoxManage clonevm '+str(so)+' --name '+str(nome_clone)+' --register && VBoxManage modifyvm '+str(nome_clone)+' --nic1 hostonly && VBoxManage startvm '+str(nome_clone))

        shell.exec('VBoxManage hostonlyif remove vboxnet0 && VBoxManage hostonlyif create && VBoxManage hostonlyif ipconfig vboxnet0 --ip 192.168.56.1 && VBoxManage modifyvm Ubuntu --hostonlyadapter1 vboxnet0 && VBoxManage modifyvm Ubuntu --nic1 hostonly && VBoxManage dhcpserver modify --ifname vboxnet0 --ip 192.168.56.1 --netmask 255.255.255.0 --lowerip '+str(ip)+' --upperip '+str(ip)+' && VBoxManage modifyvm Ubuntu --cpus '+str(cpus)+' --memory '+str(memoria)+' --vram 32 --boot1 dvd && VBoxManage clonevm '+str(so)+' --name '+str(nome_clone)+' --register && VBoxManage modifyvm '+str(nome_clone)+' --nic1 hostonly && VBoxManage startvm '+str(nome_clone))
        
        #comando = "VBoxManage"
        return "Operação realizada com sucesso! Aguarde a inicialização da VM!"
    return "Erro! Executar Novamente!"

if __name__ == "__main__":
    app.run(host='127.0.0.1', port='5000', debug=True)