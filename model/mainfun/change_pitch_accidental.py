from bs4 import BeautifulSoup as bs
import csv
import os
for filename in os.listdir('E:/musicteam/music'):  #音樂來源資料夾
    try:
        addr = 'E:/musicteam/music/'+filename
        fm = open(addr, 'r')
        music = bs(fm.read(),'xml')
        fm.close()
        sub_name = ['drum']
        sub_cand = []
        not_drum_id = []
        bass_name = ['bass']
        cand = music.select('Part')
        n=None
        The_main_melody_Tonality=[]
        #區分是不是鼓。  是鼓>>放入sub_cand，不是>>留在cand        
        for s in [par for par in cand if len(par.select('longName')) != 0]:#PART裡面有longName的放入s
            pname = s.select('longName')[0].text.encode('utf8').lower()
            if len([word for word in sub_name if word in pname]) != 0:
                sub_cand.append(s)
                cand.remove(s)
            for cin in [c for c in list(s.select('Instrument')[0].children) if c != '\n']:# more than one instru. in this staff
                if cin.get('pitch') is not None:
                    if s in cand:
                        sub_cand.append(s)
                        cand.remove(s)
                    break                    
        #取出不是鼓的樂器_id#
        [not_drum_id.append(int(jj.get('id'))) for kk in cand for jj in kk.select('Staff')]
#         for kk in range(0,len(cand)):
#             for jj in  range(0,len(cand[kk].select('Staff'))):
#                 not_drum_id.append(int(cand[kk].select('Staff')[jj].get('id')))
        #尋找不是鼓的staff如果沒有KeySig標籤與其accidental標籤，則補上KeySig標籤與accidental標籤(值為0)
        for j in not_drum_id:
            j=int(j)-1 #j-1代表staff_id=J的樂器
            if ('KeySig' in [a.name for a in music.select('Score > Staff')[j].select('Measure')[0].children if a.name is not None]) is False:
                i=tagTimeSig=music.select('Score > Staff')[j].select('Measure')[0].select('TimeSig')[0]#各樂器的第一小節中的第一個TimeSig標籤
                tag = music.new_tag("KeySig")
                tag.string = "\n"
                tag2=music.new_tag("accidental")
                tag2.string = "0"
                i.insert_before(tag)
                music.select('Score > Staff')[j].KeySig.string.insert_before(tag2)
                music.select('Score > Staff')[j].KeySig.accidental.insert_before(music.new_string("\n"))
                music.select('Score > Staff')[j].KeySig.insert_after(music.new_string("\n"))
        #轉換開始決定根據KeySig與pitch值
        dic_keysig = {0:0,1:7,2:2,3:9,4:4,5:11,6:6,7:1,-1:5,-2:10,-3:3,-4:8,-5:1,-6:6,-7:11}#大調keysig對照
        #dic_minor = {0:9,1:4,2:11,3:6,4:1,5:8,6:3,7:10,-1:2,-2:7,-3:0,-4:5,-5:10,-6:3,-7:8}#小調keysig對照
        #判斷是否同樣KEYSIG不一樣列入例外
        if len(set([int(a.text) for a in [music.select('Score > Staff')[i-1].select('Measure')[0].select('accidental')[0] for i in not_drum_id]]))==1:
            print filename+'>>>KeySig are the same'
            
        #如果沒有鼓的樂器中有BASS以他為主旋律
#           for a in cand:
#               aname = a.select('Instrument longName')[0].text.encode('utf8').lower()#aname is long_name
#               if bass_name[0] in aname:#有BASS以他為主旋律
#                   n=int(a.select('Instrument longName')[0].parent.parent.select('Staff')[0].get('id'))        
        #主旋律有給大調填大調    
#          main_melody_staff=''
#          fi = open('E:/etl/mainfun/MyData.csv','r')
#          for row in csv.reader(fi):  
#              if row[1]=='1':
#                  main_melody_staff=main_melody_staff+','+row[0]
#                  n=int(row[0])
#                  staff = music.select('Score > Staff')[n-1]
#                  keysig = int(staff.select('KeySig')[0].text.strip())
#                  lastnote = (int(staff.select('Note')[-1].pitch.text))%12
#                  if lastnote == dic_keysig[keysig]%12 or lastnote == (dic_keysig[keysig]+4)%12 or lastnote == (dic_keysig[keysig]+7)%12:
#                      The_main_melody_Tonality.append('major')
#         fi.close()            
#         if len(set(The_main_melody_Tonality))==1:
#             print filename.strip()+','+'major'+main_melody_staff
#         else:
#             print filename.strip()+','+'minor'+main_melody_staff
        #如果沒有staff_id:n
            if n is None:
                n=not_drum_id[0] #前面已排除KeySig不同，所以KeySig都一樣在不是鼓的staff中隨便給staff_id:n
            staff = music.select('Score > Staff')[n-1]
            keysig = int(staff.select('KeySig')[0].text.strip())
        #如果accidental值不是0則做轉pitch與轉accidental值(轉調)
            if keysig != 0:
                for nn in not_drum_id:
                    for pitch in music.select('Score > Staff')[nn-1].select('pitch'):
                        if int(pitch.text)<dic_keysig[keysig]:
                            j=int(pitch.text)+dic_keysig[keysig]
                        else:
                            j=int(pitch.text)-dic_keysig[keysig] 
                        pitch.string="{}".format(j)
                for accidental in music.select('Score > Staff accidental'):    
                    l=int(accidental.text)-keysig
                    accidental.string="{}".format(l)
                print filename+'>>>keysig ,pitch are change over'
            else:
                print filename+'>>>keysig is 0,nothing to change'
            addr2 = 'E:/musicteam/newmusic/'+filename  #轉完檔存放位置
            fi = open(addr2,'w')
            fi.write(str(music))
            fi.close()
        else:
            print filename+'>>>KeySig are not the same'
    except:
        print filename+',error'
