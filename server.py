from fileinput import filename
import os, hashlib
from flask import Flask, flash, request, redirect, render_template
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
                return redirect(request.url)
            file = request.files['file']
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file:
                filename = secure_filename(file.filename)
                dirSize = sum(os.path.getsize(f) for f in os.listdir('.') if os.path.isfile(f))
                if dirSize < 50 * 1000 * 1000 * 1000:
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    fileSha1 = hashlib.sha1(filename.encode('utf-8'))
                    fileCode = fileSha1.hexdigest()[:8]
                    return render_template("link.html", content=fileCode)
                else:
                    return redirect(request.url)
        except:
            return redirect(request.url)

    return render_template("upload.html")

@app.route('/receive')
@app.route('/receive/<file>', methods=["GET", "POST"])
def receive_file(file=""):
    if request.method == "POST":
        try:
            fileCode = request.form.get("fileCode")
            fileName = checkFile(fileCode)
            if fileName == "":
                return redirect(request.url)
            return render_template("download.html", content=fileName)
        except:
            return redirect(request.url)
    if file != "":
        fileName = checkFile(file)
        if fileName == "":
            return redirect(request.url)
        return render_template("download.html", content=fileName)
    else:
        return render_template("receive.html")

def checkFile(fileCode):
    if len(fileCode) == 8:
        files = os.listdir(CONTAINER)
        for i in files:
            fileSha1 = hashlib.sha1(i.encode('utf-8'))
            if fileSha1.hexdigest()[:8] == fileCode:
                return i        
        return ""
    return ""

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)