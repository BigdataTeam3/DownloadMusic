本資料夾功能用命令列執行download_sql_mscx.py後完成下載SQL裡的mscx檔並轉調後取出大小調
(多個主旋律有大調判斷這首歌主旋律為大調)與主旋律staff，存入mongodb中。
欄位依序為檔案名、檔案、大小調、主旋律staff。
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
=========================================================================================
download_sql_mscx.py:下載SQL的mscx檔並執行change_pitch_accidental.py與find_mongo_mscx.py

change_pitch_accidental.py:將沒轉pitch&&accidental的MSCX轉為C大調或A小調(accidental為0)。

find_mongo_mscx.py:將mongo中有的歌曲名抓下來到find_mongo_mscx.txt再執行newcombine.py

newcombine.py:執行newcombine.py判斷未上傳到mongodb中的歌曲裡有沒有staff的longName中
    出現main_name = ['melody','melodie','vocal','voice','sing','lead']中的字
    1.如果有=>執行產生MyData.csv(將該歌曲中有出現的staff_id寫入)再執行key.py→updb.py
    2.如果沒有=>執行ex2.py→mainfun.csv→
		Rmainfunc.R(讀入traindata.csv跑logistic regression產生MyData.csv)
                →key.py→updb.py

ex2.py:import mainfun使用mainfun.melody函式產出mainfun.csv

key.py:判斷大小調並產出→檔名|大小調|主旋律staff(有多個主旋律staff以'|'連接)

updb.py:連接mongogdb並將檔案名、檔案、大小調、主旋律staff存入
=========================================================================================
give_accidental.py:讀入filename,accidental值並產出
=========================================================================================

