from bs4 import BeautifulSoup as bs
import re
head = """
<museScore version="2.06">
<programVersion>2.0.2</programVersion>
<programRevision>f51dc11</programRevision>
<Score>
<Synthesizer>
</Synthesizer>
<Division>480</Division>"""
def insertPitch(staffid,instrumentId):
	return """
<Part>
<Staff id=\""""+staffid+"""\">        
<StaffType group="pitched">          
</StaffType>        
</Staff>      
<Instrument>        
<Channel>          
<program value=\""""+instrumentId+"""\"/>            
<synti>Fluid</synti>          
</Channel>        
</Instrument>      
</Part>
"""
def insertPer(staffid):
	return """
<Part>
      <Staff id=\""""+staffid+"""\">
        <StaffType group="percussion">
          <name>perc5Line</name>
          <keysig>0</keysig>
          </StaffType>
        <defaultClef>PERC</defaultClef>
        </Staff>
      <trackName>Drumset</trackName>
      <Instrument>
        <longName>Drumset</longName>
        <shortName>Drs.</shortName>
        <trackName>Drumset</trackName>
        <instrumentId>drum.group.set</instrumentId>
        <useDrumset>1</useDrumset>
        <Drum pitch="35">
          <head>0</head>
          <line>7</line>
          <voice>1</voice>
          <name>Acoustic Bass Drum</name>
          <stem>2</stem>
          </Drum>
        <Drum pitch="36">
          <head>0</head>
          <line>7</line>
          <voice>1</voice>
          <name>Bass Drum 1</name>
          <stem>2</stem>
          <shortcut>B</shortcut>
          </Drum>
        <Drum pitch="37">
          <head>1</head>
          <line>3</line>
          <voice>0</voice>
          <name>Side Stick</name>
          <stem>1</stem>
          </Drum>
        <Drum pitch="38">
          <head>0</head>
          <line>3</line>
          <voice>0</voice>
          <name>Acoustic Snare</name>
          <stem>1</stem>
          <shortcut>A</shortcut>
          </Drum>
        <Drum pitch="40">
          <head>0</head>
          <line>3</line>
          <voice>0</voice>
          <name>Electric Snare</name>
          <stem>1</stem>
          </Drum>
        <Drum pitch="41">
          <head>0</head>
          <line>5</line>
          <voice>0</voice>
          <name>Low Floor Tom</name>
          <stem>1</stem>
          </Drum>
        <Drum pitch="42">
          <head>1</head>
          <line>-1</line>
          <voice>0</voice>
          <name>Closed Hi-Hat</name>
          <stem>1</stem>
          <shortcut>G</shortcut>
          </Drum>
        <Drum pitch="43">
          <head>0</head>
          <line>5</line>
          <voice>1</voice>
          <name>High Floor Tom</name>
          <stem>2</stem>
          </Drum>
        <Drum pitch="44">
          <head>1</head>
          <line>9</line>
          <voice>1</voice>
          <name>Pedal Hi-Hat</name>
          <stem>2</stem>
          <shortcut>F</shortcut>
          </Drum>
        <Drum pitch="45">
          <head>0</head>
          <line>2</line>
          <voice>0</voice>
          <name>Low Tom</name>
          <stem>1</stem>
          </Drum>
        <Drum pitch="46">
          <head>1</head>
          <line>1</line>
          <voice>0</voice>
          <name>Open Hi-Hat</name>
          <stem>1</stem>
          </Drum>
        <Drum pitch="47">
          <head>0</head>
          <line>1</line>
          <voice>0</voice>
          <name>Low-Mid Tom</name>
          <stem>1</stem>
          </Drum>
        <Drum pitch="48">
          <head>0</head>
          <line>0</line>
          <voice>0</voice>
          <name>Hi-Mid Tom</name>
          <stem>1</stem>
          </Drum>
        <Drum pitch="49">
          <head>1</head>
          <line>-2</line>
          <voice>0</voice>
          <name>Crash Cymbal 1</name>
          <stem>1</stem>
          <shortcut>C</shortcut>
          </Drum>
        <Drum pitch="50">
          <head>0</head>
          <line>0</line>
          <voice>0</voice>
          <name>High Tom</name>
          <stem>1</stem>
          <shortcut>E</shortcut>
          </Drum>
        <Drum pitch="51">
          <head>1</head>
          <line>0</line>
          <voice>0</voice>
          <name>Ride Cymbal 1</name>
          <stem>1</stem>
          <shortcut>D</shortcut>
          </Drum>
        <Drum pitch="52">
          <head>1</head>
          <line>-3</line>
          <voice>0</voice>
          <name>Chinese Cymbal</name>
          <stem>1</stem>
          </Drum>
        <Drum pitch="53">
          <head>2</head>
          <line>0</line>
          <voice>0</voice>
          <name>Ride Bell</name>
          <stem>1</stem>
          </Drum>
        <Drum pitch="54">
          <head>2</head>
          <line>2</line>
          <voice>0</voice>
          <name>Tambourine</name>
          <stem>1</stem>
          </Drum>
        <Drum pitch="55">
          <head>1</head>
          <line>-3</line>
          <voice>0</voice>
          <name>Splash Cymbal</name>
          <stem>1</stem>
          </Drum>
        <Drum pitch="56">
          <head>3</head>
          <line>1</line>
          <voice>0</voice>
          <name>Cowbell</name>
          <stem>1</stem>
          </Drum>
        <Drum pitch="57">
          <head>1</head>
          <line>-3</line>
          <voice>0</voice>
          <name>Crash Cymbal 2</name>
          <stem>1</stem>
          </Drum>
        <Drum pitch="59">
          <head>1</head>
          <line>2</line>
          <voice>0</voice>
          <name>Ride Cymbal 2</name>
          <stem>1</stem>
          </Drum>
        <Drum pitch="63">
          <head>1</head>
          <line>4</line>
          <voice>0</voice>
          <name>Open Hi Conga</name>
          <stem>1</stem>
          </Drum>
        <Drum pitch="64">
          <head>1</head>
          <line>6</line>
          <voice>0</voice>
          <name>Low Conga</name>
          <stem>1</stem>
          </Drum>
        <clef>PERC</clef>
        <Channel>
          <controller ctrl="0" value="1"/>
          <program value="0"/>
          <synti>Fluid</synti>
          </Channel>
        </Instrument>
      </Part>"""
tail = """
</Score>
</museScore>"""

def staffToSheet(staffs):
	staff_dic = dict()
	for staff in staffs:
		staff_dic.update({int(re.match('.*?(\d+)',staff).group(1)):staffs[staff]})
	insertst = ''
	insertst += head + '\n'
	for staffid in sorted(staff_dic):
		if staff_dic[staffid].instrument == 'percussionType':
			print staffid, staff_dic[staffid].instrument
			insertst += insertPer(str(staffid)) + '\n'
		else:
			print staffid, staff_dic[staffid].instrument
			insertst += insertPitch(str(staffid),staff_dic[staffid].instrument) + '\n'
	for staffid in sorted(staff_dic):
		insertst += str(staff_dic[staffid].content) + '\n'
	insertst += tail
	return bs(insertst,'xml')