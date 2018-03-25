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
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:jithu@localhost/pdf1'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

class Subject(db.Model):
    __tablename__ = 'subject'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    code = db.Column(db.String(128))
    course_id = db.Column(db.Integer)

class Course(db.Model):
    __tablename__ = 'course'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    type = db.Column(db.String(128))

class Result(db.Model):
    __tablename__ = 'result'
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer)
    reg = db.Column(db.String(128))
    sub = db.Column(db.String(8))
    score = db.Column(db.String(16))

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
    student_subjects = []
    students = []
    st = None

    reg = re.compile('^Register No')
    subj = re.compile('^Course Code')
    branch = re.compile('^([A-Z| ]*)\[(.*)\]')
    sub = re.compile('^\d{2}[A-Z]{2}\d{4} .*')
    regV = re.compile('^L?[A-Z]{3}\d{2}[A-Z]{2}\d{3} .*')
    resultValue = re.compile('^[A-Z]{2}\d{3}\(.*')

    for line in fp:
        line = line.strip()
        
        if branch.match(line):
            print line
            k = branch.search(line)
            topic = k.group(1)
            type = k.group(2)
            print topic
            c = Course.query.filter_by(name=topic).first()
            if not c:
                c = Course(name=topic, type=type)
                db.session.add(c)
                db.session.commit()
                course_id = c.id
            else:
                course_id = c.id
            next_line = 'subject_heading'

        elif reg.match(line):
            next_line = 'result'
        elif subj.match(line) and next_line == 'subject_heading':
            next_line = 'sub'
        elif next_line == 'sub' and sub.match(line):
            subject = line.split(' ', 1)
            subject.append(course_id)
            subjects.append(subject)
        #elif next_line == 'result':
        elif next_line == 'result' and resultValue.match(line):
            l = line.split()
            for s in l:
                m = re.search('([A-Z]{2}\d{3})\((\w+\+?)\),?', s)
                if m is not None:
                    db.session.add(Result(reg=st, sub=m.group(1), score=m.group(2), course_id=course_id))
            st = None

            #if len(l[0]) is 11 and len(l) is 8:
                #l.append(course_id)
                #students.append(l)
        elif next_line == 'result' and regV.match(line):
            l = line.split()
            st = l[0]
            for s in l[1:]:
                m = re.search('([A-Z]{2}\d{3})\((\w+\+?)\),?', s)
                if m is not None:
                    db.session.add(Result(reg=l[0], sub=m.group(1), score=m.group(2), course_id=course_id))
        elif sub.match(line):
            subject = line.split(' ', 1)
            subject.append(course_id)
            subjects.append(subject)
        else:
            next_line = ''

    for s in subjects:
        if not Subject.query.filter_by(code=s[0]).first():
            db.session.add(Subject(code=s[0], name=s[1], course_id=s[2]))
    #for st in students:
        #db.session.add(Result(reg=st[0], sub1=st[1], sub2=st[2], sub3=st[3], sub4=st[4], sub5=st[5], sub6=st[6], sub7=st[7], course_id=st[8]))
    db.session.commit()

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        if 'pdf' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['pdf']
        if file.filename == '':
            flash( 'No selected file' )
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            if os.path.isfile(os.path.join(app.config['UPLOAD_FOLDER'], filename)):
                flash('file already uploaded')
                return redirect(request.url)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            process_pdf(filename)
            flash('file uploaded')
            return redirect(request.url)
            #return redirect(url_for('uploaded_file' , filename=filename))
        # check if the post request has
    return render_template('admin.html')

@app.route('/', methods=['GET', 'POST'])
def result():
    result = ''
    subjects = []
    if request.method == 'POST' and request.form['reg'] != '':
        reg = request.form['reg']
        result = Result.query.filter_by(reg=reg)
        if not result.first():
            flash('result not found')
            return redirect(request.url)

        subjects = Subject.query.filter_by(course_id=result.first().course_id)

    return render_template('index.html', result=result, subjects=subjects)

if __name__ == '__main__':
    app.debug = True
    manager.run()

