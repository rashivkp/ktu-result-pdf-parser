import os
import re
import MySQLdb
filename = 'result_KSD.txt'

#os.system("sed '/^$/d' "+filename+" > 1"+filename)
#os.system("sed '1,3 d' 1"+filename+" > 2"+filename)
#os.system("sed 's/\cL//' 2"+filename+" > 3"+filename)
os.system("sed -e '/^$/d' -e '/^*/d' -e '1,2 d' -e 's/\cL//' -e 's/^ *//' -e 's/ \+/ /' "+filename+" > 1"+filename)
fp = open("1"+filename)
subjects = []
next_line = ''
students = []
student_subjects = []
st = None
for line in fp:
    line = line.strip()
    reg = re.compile('^Register No')
    course = re.compile('^Course Code')
    sub = re.compile('^[A-Z]{2}\d{3} .*')
    regV = re.compile('^L?[A-Z]{3}\d{2}[A-Z]{2}\d{3} .*')
    resultValue = re.compile('^[A-Z]{2}\d{3}\(.*')
    if reg.match(line):
        next_line = 'result'
    elif course.match(line):
        next_line = 'sub'
    elif next_line == 'sub' and sub.match(line):
        subject = line.split(' ', 1)
        subjects.append(subject)
    #elif next_line == 'result':
    elif next_line == 'result' and resultValue.match(line):
        l = line.split()
        for s in l:
            m = re.search('([A-Z]{2}\d{3})\((\w+\+?)\),?', s)
            if m is not None:
                st_marks.append(m.group(2))
                sub_order.append(m.group(1))
        students.append(st_marks)
        student_subjects.append(sub_order)
        st = None
        #students.append(l)
    elif next_line == 'result' and regV.match(line):
        l = line.split()
        if st is not None:
            students.append(st_marks)
            student_subjects.append(sub_order)
        st = l[0]
        st_marks = []
        sub_order = []
        st_marks.append(st)
        for s in l[1:]:
            m = re.search('([A-Z]{2}\d{3})\((\w+\+?)\),?', s)
            if m is not None:
                st_marks.append(m.group(2))
                sub_order.append(m.group(1))
    elif sub.match(line):
        subject = line.split(' ', 1)
        subjects.append(subject)
    else:
        next_line = ''

if st is not None:
    students.append(st_marks)

print subjects
#print students
#print student_subjects
print len(subjects)
for s in subjects:
    print s

