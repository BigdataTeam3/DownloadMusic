from bs4 import BeautifulSoup as bs
import csv
import sys
for filename in sys.stdin:
	print filename
dic_keysig = {0:0,1:7,2:2,3:9,4:4,5:11,6:6,7:1,-1:5,-2:10,-3:3,-4:8,-5:1,-6:6,-7:11}
f = open('E:/musicteam/newmusic/'+filename.strip(),'r')
music = bs(f.read(),'xml')
f.close()
fi = open('E:/etl/mainfun/MyData.csv','r')
The_main_melody_Tonality=[]
main_melody_staff=''
for row in csv.reader(fi):  
    if row[1]=='1':
        main_melody_staff=main_melody_staff+'|'+row[0]
        n=int(row[0])
        staff = music.select('Score > Staff')[n-1]
        keysig = int(staff.select('KeySig')[0].text.strip())
        lastnote = (int(staff.select('Note')[-1].pitch.text))%12
        if lastnote == dic_keysig[keysig]%12 or lastnote == (dic_keysig[keysig]+4)%12 or lastnote == (dic_keysig[keysig]+7)%12:
            The_main_melody_Tonality.append('major')
fi.close()            
if len(set(The_main_melody_Tonality))==1:
    print filename.strip()+'|'+'major'+main_melody_staff
else:
    print filename.strip()+'|'+'minor'+main_melody_staff