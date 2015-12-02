###
import pyodbc
import os
#q = r'select * from mscx_table where lang=?' #
#select="english"#
q = r'select * from mscx_table where lang = ?'
conn = pyodbc.connect('DRIVER={SQL Server};SERVER=10.120.30.8;DATABASE=music;UID=sa;PWD=passw0rd')
cur = conn.cursor()
addr = 'E:/musicteam/music' #
#cur.execute(q,select)##
lan = 'english'
rs=cur.execute(q,lan)
musicfilename=[filename.split('.mscx')[0] for filename in os.listdir('E:/musicteam/music')]
try:
    while(rs.next()):
        # row = cur.fetchone() #
        # rows = cur.fetchall()	#
        rows = cur.fetchmany(100)#
        for row in rows:
        #     print row.mname
            i+=1
            if row.mname not in musicfilename:
                content = row.data
                fi = open(addr+'/'+row.mname+'.mscx','wb')
                fi.write(content)
                fi.close()
        print i
        rows=[]
except:
    print 'error'
cur.close()
conn.close()
os.system('python change_pitch_accidental.py')
os.system('python find_mongo_mscx.py')
