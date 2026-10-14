import subprocess,json
T=[('title','Start'),('01','Unlock 4 (scan QR or type code)'),('02','Home and choosing your grade'),('03','Notes: subjects, units, cards'),('04','Memory tricks, games and unit quiz'),('05','Exercise: practice and Daily Quiz'),('06','Matric and model exams (Grades 11–12)'),('07','Search'),('08','Tutor: ask a question'),('09','Virtual lab (Try it)'),('10','Pictures, 3D models and animations'),('11','Videos, reels and locked PDFs'),('12','Study Coach: check-in and 30-day plan'),('13','Study tips and worksheets'),('14','Your progress'),('15','Settings: name, theme, look'),('16','Monthly update (file)'),('17','Help and contact'),('end','End')]
t=0;out=[]
for n,title in T:
    d=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f'rec/{n}.mp4']))
    if n!='end' and n!='title': out.append((int(t*1000),title))
    if n=='title': out.append((0,'Start'))
    t+=d
json.dump(out,open('chapters.json','w'))
for ms,x in out: print(f'{ms//60000}:{ms//1000%60:02d} {x}')
print('total',round(t,1))
