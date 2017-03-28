from flask import Flask, flash, render_template, request, redirect, url_for
import os, re, MySQLdb
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['pdf'])
app = Flask(__name__)
app.secret_key = 'sdfakjkj'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://pdfparser:password@localhost/pdfdata'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

class Subject(db.Model):
    __tablename__ = 'subject'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    code = db.Column(db.String(128))

class Result(db.Model):
    __tablename__ = 'result'
    id = db.Column(db.Integer, primary_key=True)
    reg = db.Column(db.String(128))
    sub1 = db.Column(db.String(8))
    sub2 = db.Column(db.String(8))
    sub3 = db.Column(db.String(8))
    sub4 = db.Column(db.String(8))
    sub5 = db.Column(db.String(8))
    sub6 = db.Column(db.String(8))
    sub7 = db.Column(db.String(8))
    sub8 = db.Column(db.String(8))

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def process_pdf(pdf_filename):

    os.system("pdftotext -layout uploads/"+pdf_filename)
    filename = pdf_filename.rsplit('.', 1)[0]
    filename += '.txt'
    os.system("sed -e '/^$/d' -e '/^*/d' -e '1,2 d' -e 's/\cL//' -e 's/^ *//' -e 's/ \+/ /' uploads/"+filename+" > stripped/"+filename)
    fp = open("stripped/"+filename)
    subjects = []
    next_line = ''
    students = []
    for line in fp:
        line = line.strip()

        reg = re.compile('^Register Number')
        course = re.compile('^Course Code')
        sub = re.compile('^\d{2}[A-Z]{2}\d{4} .*')
        if reg.match(line):
            next_line = 'result'
        elif course.match(line):
            next_line = 'sub'
        elif next_line == 'sub' and sub.match(line):
            subject = line.split(' ', 1)
            subjects.append(subject)
        elif next_line == 'result':
            l = line.split()
            if len(l[0]) is 11 and len(l) is 8:
                students.append(l)
        elif sub.match(line):
            subject = line.split(' ', 1)
            subjects.append(subject)
        else:
            next_line = ''

    for s in subjects:
        db.session.add(Subject(code=s[0], name=s[1]))
    for st in students:
        if len(st) == 8:
            db.session.add(Result(reg=st[0], sub1=st[1], sub2=st[2], sub3=st[3], sub4=st[4], sub5=st[5], sub6=st[6], sub7=st[7]))
    db.session.commit()

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        if 'pdf' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['pdf']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash( 'No selected file' )
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            process_pdf(filename)
            flash('file uploaded')
            return redirect(request.url)
            #return redirect(url_for('uploaded_file' , filename=filename))
        # check if the post request has
    return render_template('index.html')

if __name__ == '__main__':
    app.debug = True
    manager.run()

