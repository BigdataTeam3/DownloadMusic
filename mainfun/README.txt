����Ƨ��\��ΩR�O�C����download_sql_mscx.py�᧹���U��SQL�̪�mscx�ɨ���ի���X�j�p��
(�h�ӥD�۫ߦ��j�էP�_�o���q�D�۫߬��j��)�P�D�۫�staff�A�s�Jmongodb���C
���̧Ǭ��ɮצW�B�ɮסB�j�p�աB�D�۫�staff�C
=========================================================================================
�H�U��dbname&&collectname 
client = MongoClient('mongodb://10.120.30.8:27017')
db = client['music']  
collect = db['mscx_c_key']
=========================================================================================
���W�١G��줺�e
_id�G�ɮצW��
data�G�ɮ�
tonality�Gmajor(�D�۫ߦ��j��)�_�h�Ominor
main_melody�G�D�۫ߪ�staff_id
=========================================================================================
download_sql_mscx.py:�U��SQL��mscx�ɨð���change_pitch_accidental.py�Pfind_mongo_mscx.py

change_pitch_accidental.py:�N�S��pitch&&accidental��MSCX�ରC�j�թ�A�p��(accidental��0)�C

find_mongo_mscx.py:�Nmongo�������q���W��U�Ө�find_mongo_mscx.txt�A����newcombine.py

newcombine.py:����newcombine.py�P�_���W�Ǩ�mongodb�����q���̦��S��staff��longName��
    �X�{main_name = ['melody','melodie','vocal','voice','sing','lead']�����r
    1.�p�G��=>���沣��MyData.csv(�N�Ӻq�������X�{��staff_id�g�J)�A����key.py��updb.py
    2.�p�G�S��=>����ex2.py��mainfun.csv��
		Rmainfunc.R(Ū�Jtraindata.csv�]logistic regression����MyData.csv)
                ��key.py��updb.py

ex2.py:import mainfun�ϥ�mainfun.melody�禡���Xmainfun.csv

key.py:�P�_�j�p�ըò��X���ɦW|�j�p��|�D�۫�staff(���h�ӥD�۫�staff�H'|'�s��)

updb.py:�s��mongogdb�ñN�ɮצW�B�ɮסB�j�p�աB�D�۫�staff�s�J
=========================================================================================
give_accidental.py:Ū�Jfilename,accidental�Ȩò��X
=========================================================================================

