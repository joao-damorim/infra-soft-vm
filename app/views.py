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
        memoria=request.form['memoria']
        so=request.form['so']
        nome_clone=request.form['nome_clone']
        cpus=request.form['cpus']
        ip=request.form['ip']
        num_maq=request.form['num_maq']
        
        if so == "Ubuntu" or so == "ubuntu": 
            shell.exec('VBoxManage hostonlyif create && VBoxManage hostonlyif ipconfig vboxnet'+str(num_maq)+' --ip 192.168.'+str(num_maq)+'.1 && VBoxManage modifyvm Ubuntu --hostonlyadapter1 vboxnet'+str(num_maq)+' && VBoxManage modifyvm Ubuntu --nic1 hostonly && VBoxManage dhcpserver add --ifname vboxnet'+str(num_maq)+' --ip 192.168.'+str(num_maq)+'.1 --netmask 255.255.255.0 --lowerip '+str(ip)+' --upperip '+str(ip)+' && VBoxManage dhcpserver modify --ifname vboxnet'+str(num_maq)+' --enable && VBoxManage modifyvm Ubuntu --cpus '+str(cpus)+' --memory '+str(memoria)+' --vram 32 --boot1 dvd && VBoxManage clonevm '+str(so)+' --name '+str(nome_clone)+' --register && VBoxManage modifyvm '+str(nome_clone)+' --nic1 hostonly && VBoxManage startvm '+str(nome_clone))

        if so == "Windows" or so == "windows":
             shell.exec('VBoxManage hostonlyif create && VBoxManage hostonlyif ipconfig vboxnet'+str(num_maq)+' --ip 192.168.'+str(num_maq)+'.1 && VBoxManage modifyvm Windows --hostonlyadapter1 vboxnet'+str(num_maq)+' && VBoxManage modifyvm Windows --nic1 hostonly && VBoxManage dhcpserver add --ifname vboxnet'+str(num_maq)+' --ip 192.168.'+str(num_maq)+'.1 --netmask 255.255.255.0 --lowerip '+str(ip)+' --upperip '+str(ip)+' && VBoxManage dhcpserver modify --ifname vboxnet'+str(num_maq)+' --enable && VBoxManage modifyvm Windows --cpus '+str(cpus)+' --memory '+str(memoria)+' --vram 32 --boot1 dvd && VBoxManage clonevm '+str(so)+' --name '+str(nome_clone)+' --register && VBoxManage modifyvm '+str(nome_clone)+' --nic1 hostonly && VBoxManage startvm '+str(nome_clone))

        return "Operação realizada com sucesso! Aguarde a inicialização da VM!"
    return "Erro! Executar Novamente!"

if __name__ == "__main__":
    app.run(host='127.0.0.1', port='5000', debug=True)