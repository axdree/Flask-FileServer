import os 
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
                    return f"Your download link is: <a href='https://filesrv.andreyap.com/storage/{filename}'>https://filesrv.andreyap.com/storage/{filename}</a>"
                else:
                    return redirect(request.url)
        except:
            return redirect(request.url)

    return render_template("upload.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)