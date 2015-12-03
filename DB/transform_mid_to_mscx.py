# -- coding: UTF-8 --
import pyodbc
import os
import time
q = r'select * from musictable where lang = ?' 
q2 = r'insert into mscx_table values(?,?,?,?)'
#conn = pyodbc.connect('DRIVER={SQL SERVER};SYSTEM=10.120.30.8;\
#UID=sa;PWD=passw0rd;DBQ=jdbc;EXTCOLINFO=1')

conn = pyodbc.connect('DSN=sqlserverdatasource;\
DATABASE=music;UID=sa;PWD=passw0rd')


#conn = pyodbc.connect('DRIVER={SQL Server};SERVER=10.120.30.14;\
#DATABASE=jdbc;UID=sa;PWD=passw0rd')
cur = conn.cursor()
addr = '/home/torrid/Downloads'
select = 'english'
cur.execute(q,select)
rows = cur.fetchall()
# rows = cur.fetchall()	

for row in rows:
  try:
    if len(row.data)==64512:
      continue
    content = row.data
    filename = addr+'/'+row.mname.encode('utf8')+'.mid'
    fi = open(filename,'wb')
    fi.write(content)
    fi.close()
    targetname = addr+'/'+row.mname.encode('utf8')+'.mscx'
    os.system('mscore "'+filename +'" -o "'+ targetname+'"')
    time.sleep(0.2)
    fj = open(targetname,'rb')
    fjcontent = fj.read()
    fj.close()
    insert = (row.mname,pyodbc.Binary(fjcontent),row.lang,row.src)
    cur.execute(q2,insert)
    print row.mname + ' complete'
    os.system('rm "' + filename+'"')
    os.system('rm "' + targetname+'"')
    conn.commit()
    time.sleep(0.4)
  except:
    errfile = addr + '/' + 'errorfile.txt'
    fe = open(errfile,'a')
    fe.write(row.mname+'\t'+ row.lang+'\t'+ row.src+'\n')
    fe.close()
cur.close()
conn.close()

  
#print type(row.mname.encode('utf8')),row.mname.encode('utf8')
#print type(row.mname),row.mname
