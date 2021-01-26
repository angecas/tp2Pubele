from flask import Flask, render_template, redirect, request, flash, send_file, flash
import requests
import json
import db
import os
from werkzeug.utils import secure_filename


app = Flask(__name__)


#Index
@app.route('/')
def index():
    return render_template('index.html')
#-----------------------------------------------------------------------
#Todos os relatorios
@app.route('/relatorios', methods=['GET'])
def get_relatorios():
    res = requests.get('http://localhost:5000/api/relatorios')
    ps = json.loads(res.content)
    return render_template('relatorios_view.html', relatorios=ps)

@app.route('/api/relatorios', methods=['GET'])
def api_get_relatorios():
    ps = db.find_all()
    return json.dumps(ps)
#-----------------------------------------------------------------------
#Add
@app.route('/relatorios/add', methods=['GET'])
def get_relatorios_add():
    res = requests.get('http://localhost:5000/api/relatorios')
    ps = json.loads(res.content)
    return render_template('relatorio_add.html', relatorios=ps)

@app.route('/relatorios/add', methods=['POST'])
def post_relatorio_add():
    data = dict(request.form)
    print(data)
    requests.post('http://localhost:5000/api/relatorios/add', data=data)
    return redirect('http://localhost:5000/relatorios')

@app.route('/api/relatorios/add', methods=['GET'])
def api_get_relatorios_add():
    ps = db.find_all()
    return json.dumps(ps)

@app.route('/api/relatorios/add', methods=['POST'])
def api_post_relatorios_add():

    data = dict(request.form)
    db.insert(data)

    return json.dumps(db.find_all())
#-----------------------------------------------------------------------
#Remove
@app.route('/relatorios/remove', methods=['GET'])
def get_relatorios_remove():
    res = requests.get('http://localhost:5000/api/relatorios')
    ps = json.loads(res.content)

    return render_template('relatorio_remove.html', relatorios=ps)

@app.route('/relatorios/remove', methods=['POST'])
def post_relatorio_remove():
    data = dict(request.form)
    requests.post('http://localhost:5000/api/relatorios/remove', data=data)

    return redirect('http://localhost:5000/relatorios/remove')

@app.route('/api/relatorios/remove', methods=['GET'])
def api_get_relatorios_remove():
    ps = db.find_all()
    return json.dumps(ps)

@app.route('/api/relatorios/remove', methods=['POST'])
def api_post_relatorios_remove():
    req=request.form
    dic=dict(req)
    db.deletebytitle(dic["relatorio"])
#-----------------------------------------------------------------------
#Relatorio Individual
@app.route('/relatorios/<relatorio>', methods=['GET'])
def get_relatorio(relatorio):
    res = requests.get('http://localhost:5000/api/relatorios/' + relatorio)

    r = json.loads(res.content)

    return render_template('relatorio_view.html', r=r)


@app.route('/api/relatorios/<relatorio>', methods=['GET'])
def api_get_relatorio(relatorio):
    p = db.find_one(relatorio)
    return json.dumps(p)
#-----------------------------------------------------------------------
#AUTORES
@app.route('/autores')
def autores():
    return render_template("autores.html")

@app.route('/angelica')
def angelica():
    return render_template("angelica.html")

@app.route('/bruna')
def bruna():
    return render_template("bruna.html")

@app.route('/bruno')
def bruno():
    return render_template("bruno.html")
#-----------------------------------------------------------------------
#INFORMACAO NO PORTAL
@app.route('/uc')
def uc_info():
    return redirect("https://elearning.uminho.pt/",
                    code=302)


#--------------------------------------------------------------------
@app.route('/utilidades')
def utilidades_view():
    return render_template('util.html')

@app.route('/reset')
def reset():
    db.apagatodos()
    return redirect('/relatorios/add')


@app.route('/ordena')
def ordena():
    L=db.ordenaalfa()
    return render_template("ordena.html", L=L)


@app.route('/gestao')
def gestao():
    return render_template('gestao.html')


#repositorio de documentos


UPLOAD_FOLDER = 'uploads/'

#app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


L=[]
# Upload API
@app.route('/uploadfile', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            print('no file')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            print('no filename')
            return redirect(request.url)
        else:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            Ls=lisof_file(L)
            print("saved file successfully")
      #send file name as parameter to downlad
            return render_template('upload_file.html', filename=filename, Ls=Ls)

    return render_template('upload_file.html')

@app.route('/uploadfile', methods=['GET', 'POST'])
def lisof_file(L):
    if request.method == 'POST':
        file = request.files['file']
        filename = secure_filename(file.filename)
        L.append(str(filename))
        return L
    

@app.route('/return-files/<filename>')
def return_files_tut(filename):
    file_path = UPLOAD_FOLDER + filename
    return send_file(file_path, as_attachment=True, attachment_filename='')

#-----------------------------------------------------------------------
#ERROR HANDLERS
@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html')


if __name__ == '__main__':
    app.run(debug=True)
