import os, hashlib
from flask import Flask, flash, request, redirect, render_template, url_for
from werkzeug.utils import secure_filename

CONTAINER = "../storageContainer/"

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = CONTAINER
app.config['MAX_CONTENT_LENGTH'] = 10 * 1000 * 1000 * 1000

@app.route('/', methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        try:
            if 'file' not in request.files:
                flash('No file part')
                return "err"
            file = request.files['file']
            if file.filename == '':
                flash('No selected file')
                return "err"
            if file:
                filename = secure_filename(file.filename)
                dirSize = sum(os.path.getsize(f) for f in os.listdir('.') if os.path.isfile(f))
                if dirSize < 50 * 1000 * 1000 * 1000:
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    fileSha1 = hashlib.sha1(filename.encode('utf-8'))
                    fileCode = fileSha1.hexdigest()[:6]
                    return fileCode# return render_template("link.html", content=fileCode)
                else:
                    return "err"
        except Exception as e:
            return "err"

    return render_template("upload.html")

@app.route('/link', methods=["GET"])
def linkGen():
    code = request.args.get("code")
    try:
        if code.isalnum() and len(code) == 6:
            return render_template("link.html", content=code)
    except:
        return redirect("/")
    return redirect("/")

@app.route('/receive', methods=["GET", "POST"])
@app.route('/receive/<file>', methods=["GET"])
def receive_file(file=""):
    if request.method == "POST":
        try:
            fileCode = request.form.get("fileCode")
            print(fileCode)
            fileName = checkFile(fileCode)
            if fileName == "":
                return redirect(url_for('upload_file'))
            return render_template("download.html", content=fileName)
        except:
            return redirect("/")
    if file != "":
        fileName = checkFile(file)
        if fileName == "":
            return redirect(url_for('upload_file'))
        return render_template("download.html", content=fileName)
    else:
        return render_template("receive.html")

def checkFile(fileCode):
    if len(fileCode) == 8:
        try:
            int(fileCode, 16)
        except:
            return ""
        files = os.listdir(CONTAINER)
        for i in files:
            fileSha1 = hashlib.sha1(i.encode('utf-8'))
            if fileSha1.hexdigest()[:6] == fileCode:
                return i        
        return ""
    return ""

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
