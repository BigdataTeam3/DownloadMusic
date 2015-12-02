from bs4 import BeautifulSoup as bs
import csv
import os
def give_accidental(filename,accidental1):
    try:
        addr = 'E:/musicteam/give_accidental/'+filename
        fm = open(addr, 'r')
        music = bs(fm.read(),'xml')
        fm.close()
        sub_name = ['drum']
        sub_cand = []
        not_drum_id = []
        bass_name = ['bass']
        cand = music.select('Part')
        #    
        for s in [par for par in cand if len(par.select('longName')) != 0]:#
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
        [not_drum_id.append(int(jj.get('id'))) for kk in cand for jj in kk.select('Staff')]
        dic_keysig = {0:0,1:7,2:2,3:9,4:4,5:11,6:6,7:1,-1:5,-2:10,-3:3,-4:8,-5:1,-6:6,-7:11}#
        for nn in not_drum_id:
            for pitch in music.select('Score > Staff')[nn-1].select('pitch'):
                j=int(pitch.text)+dic_keysig[accidental1] 
                pitch.string="{}".format(j)
        for accidental in music.select('Score > Staff accidental'):    
            l=int(accidental.text)+accidental1
            accidental.string="{}".format(l)
        print filename+'>>>keysig ,pitch are change over'

        addr2 = 'E:/musicteam/give_accidental/new/'+filename  #
        fi = open(addr2,'w')
        fi.write(str(music))
        fi.close()
    except:
        print filename+',error'