# Nama : Miftakhul Anam / 19090127
# Nama : M. salman septianto / 19090080 

import datetime
import os
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, jsonify, request
app = Flask(__name__)

app_dir = os.path.dirname(os.path.abspath(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///{}".format(
    os.path.join(app_dir, "image.db"))
app.config['UPLOAD_FOLDER'] = 'img'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    file = db.Column(db.String(120), unique=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)


# Buat folder 'img' jika tidak ada
if not os.path.exists(os.path.join(app_dir, app.config['UPLOAD_FOLDER'])):
    os.makedirs(os.path.join(app_dir, app.config['UPLOAD_FOLDER']))

# Buat db lokal jika file db tidak ada
if not os.path.exists(os.path.join(app_dir, 'image.db')):
    db.create_all()


@app.route('/file-upload', methods=['POST'])
def upload():

    name = request.form.get('name')
    file = request.files['file_img']

    if 'file_img' not in request.files:
        return jsonify({'msg': 'Upload Failed :('})

    if file.filename != '':
        try:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            data = User(name=name, file=filename)
            db.session.add(data)
            db.session.commit()
            return jsonify({'msge': 'Upload Success'})
        except Exception as error:
            return jsonify({'msge': "Upload Failed :( nama harus unik, nama ini sudah dipakai!"})
    else:
        return jsonify({'msge': 'Upload Failed'})


if __name__ == '__main__':
    app.run(debug=True, port=8080)
