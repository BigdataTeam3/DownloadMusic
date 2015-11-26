還沒轉pitch&&accidental的MSCX先執行change_pitch&&accidental.py先轉完
=========================================================================================
執行newcombine.py
main_name = ['melody','melodie','vocal','voice','sing','lead']，有沒有在staff的longName中
1.如果有
=>執行將該staff_id寫入MyData.csv中再執行key.py-->updb.py
2.如果沒有
=>執行ex2.py->Rmainfunc.R(產生MyData.csv)->key.py->updb.py
=========================================================================================
檔案已轉pitch＆keysig的accidental為0
=========================================================================================
以下為dbname&&collectname 
client = MongoClient('mongodb://10.120.30.8:27017')
db = client['music']  
collect = db['mscx_c_key']
=========================================================================================
欄位名稱：欄位內容
_id：檔案名稱
data：檔案
tonality：major(主旋律有大調)否則是minor
main_melody：主旋律的staff_id
