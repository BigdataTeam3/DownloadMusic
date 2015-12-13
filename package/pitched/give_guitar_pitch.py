from decimal import *
import pymongo
from pymongo import MongoClient
def Dong(cp,measure):

    dic_cp = {'C':[0, 4, 7],'C7':[0,4,7,10],'Cmaj7':[0, 4, 7, 11],
        'Dm':[2, 5, 9],'D':[2,6,9],'Dm7':[2, 5, 9, 12],'D7':[2,6,9,12],
        'E':[4,8,11],'E7':[4,8,11,14],'Em':[4, 7, 11],'Em7':[4, 7, 11, 14],
        'F':[5, 9, 12],'Fmaj7':[5, 9, 12, 16],
        'G':[7, 11, 14],'G7':[7, 11, 14, 17],
        'A':[9,13,16],'Am':[9, 12, 16],'Am7':[9, 12, 16, 19],
        'Bb':[10, 14, 17],'Bdim':[11, 14, 17]}
    m1=0
    m2=0
    k=0
    aa_i = measure.copy()
    for key in sorted([aa_ii for aa_ii in aa_i if 'track' in aa_ii]):

        j=k        
        if key=='track0':   
            i=m1           
        elif key!='track0':
            m2-=1 
            i=m2
        m=i
        duration=0
        A=[]
        durationType_pitch=''        
        for pitch in aa_i[key].split(';'):
            if len(pitch.split(','))==2:
                pitch=pitch+',0'
            if duration>=0.5:
                A.append(pitch.split(',')[2])
            if len(A)==1 and (str(A[0])=='1' or str(A[0])=='-1'):
                pitch=pitch.split(',')[0]+','+pitch.split(',')[1]+',0'
            if len(A)==1:
                i=m
            if cp[j]=='0':
                newpitch=0
                durationType_pitch=durationType_pitch+';'+pitch.split(',')[0]+','+str(newpitch)
            else:
                if len(pitch.split(','))==3 and pitch.split(',')[2]=='1':
                    i+=1
                    newpitch=60+12*(i/len(dic_cp[cp[j]]))+dic_cp[cp[j]][i%len(dic_cp[cp[j]])]
                    durationType_pitch=durationType_pitch+';'+pitch.split(',')[0]+','+str(newpitch)
                elif len(pitch.split(','))==3 and pitch.split(',')[2]=='-1':
                    i+=-1
                    newpitch=60+12*(i/len(dic_cp[cp[j]]))+dic_cp[cp[j]][i%len(dic_cp[cp[j]])]
                    durationType_pitch=durationType_pitch+';'+pitch.split(',')[0]+','+str(newpitch)
                else:
                    if pitch.split(',')[1]=='0':
                        newpitch=0
                    else:
                        newpitch=60+12*(i/len(dic_cp[cp[j]]))+dic_cp[cp[j]][i%len(dic_cp[cp[j]])]
                    if durationType_pitch=='':
                        durationType_pitch=durationType_pitch+pitch.split(',')[0]+','+str(newpitch)
                    else:
                        durationType_pitch=durationType_pitch+';'+pitch.split(',')[0]+','+str(newpitch) 
            duration=duration+float(pitch.split(',')[0])
            if duration>=0.5:
                j=k+1
        aa_i[key]=durationType_pitch    
    return aa_i