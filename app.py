from flask import Flask, flash, render_template, request, redirect, url_for
import os, re, MySQLdb
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['pdf'])
app = Flask(__name__)
app.secret_key = 'sdfakjkj'
app.config['UPLOAD_FOLDER'] = 'uploads'

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

    print subjects
    print students
    print len(subjects)

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

if __name__ == "__main__":
    app.debug = True
    app.run(debug=app.debug, host='0.0.0.0')

