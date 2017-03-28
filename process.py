import os
import re
import MySQLdb
filename = 'result_KNR.txt'

#os.system("sed '/^$/d' "+filename+" > 1"+filename)
#os.system("sed '1,3 d' 1"+filename+" > 2"+filename)
#os.system("sed 's/\cL//' 2"+filename+" > 3"+filename)
os.system("sed -e '/^$/d' -e '/^*/d' -e '1,2 d' -e 's/\cL//' -e 's/^ *//' -e 's/ \+/ /' "+filename+" > 1"+filename)
fp = open("1"+filename)
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
for s in subjects:
    print s

