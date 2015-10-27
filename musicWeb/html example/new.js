 function doFirst(){
	barSize=604;
	myMovie=document.getElementById('myMovie');
	playButton=document.getElementById('playButton');
	stopButton=document.getElementById('stopButton');
	upButton=document.getElementById('upButton');
	downButton=document.getElementById('downButton');
	mutueButton=document.getElementById('mutueButton');
	defaultBar=document.getElementById('defaultBar');
	progressBar=document.getElementById('progressBar');
	
	playButton.addEventListener('click',playOrPause,false);
	stopButton.addEventListener('click',stop,false);
	upButton.addEventListener('click',upVolume,false);
	downButton.addEventListener('click',downVolume,false);
	mutueButton.addEventListener('click',mutueVolume,false);
	defaultBar.addEventListener('click',clickedBar,false);
	myMovie.addEventListener('click',playOrPause,false);
	
	getSound();
	getTime();
 }

function playOrPause(){		
	if(!myMovie.paused && !myMovie.ended){//影片正在播放中
	myMovie.pause();
	playButton.innerHTML='Play';
	getTime();
	}else{			   					//影片暫停或結束
	myMovie.play();
	playButton.innerHTML='Paused';	
	setInterval(update,400);
	getTime();
	}
}
function stop(){
	myMovie.currentTime=0;
	myMovie.pause();
	playButton.innerHTML='Play';
	getTime();
}
function upVolume(){
	myMovie.volume+=0.1;
	getSound();
}
function downVolume(){
	myMovie.volume-=0.1;
    getSound();
}
function mutueVolume(){
	if(!myMovie.muted){
	myMovie.muted=true;
	}else{
	myMovie.muted=false;	
	}
	getSound();
}
function update(){
	if(!myMovie.ended){
	var size=(barSize/myMovie.duration)*myMovie.currentTime;//(barSize/myMovie.duration)=1秒是多少barSize
	progressBar.style.width= size+'px';
	getTime();
	}else{
	progressBar.style.width='0px';		
	playButton.innerHTML='Play';
	getTime();
	}
}	

function clickedBar(e){
	var mouseX=e.clientX-defaultBar.offsetLeft;
	var newTime=mouseX*myMovie.duration/barSize;
	myMovie.currentTime=newTime;
	progressBar.style.width=mouseX+'px';
	
}
function getSound(){
	var videoVolume = myMovie.volume*100;
	videoVolume = videoVolume.toFixed(0);
	document.getElementById('nowVolume').innerHTML = 'volume: '+videoVolume+'%';
}	
function getTime(){
	var videoTime = myMovie.currentTime.toFixed(0);
	var totalVideoTime = myMovie.duration;
	var secondNow = videoTime % 60;
	var minuteNow = (videoTime -secondNow)/60;
	var secondTotal = totalVideoTime % 60;
	var minuteTotal = (totalVideoTime -secondTotal)/60;
	if(secondNow<10){
		document.getElementById('nowTime').innerHTML = minuteNow + ':0' + secondNow+'/'+ minuteTotal + ':' + secondTotal;
	}else{
		document.getElementById('nowTime').innerHTML = minuteNow + ':' + secondNow+'/'+ minuteTotal + ':' + secondTotal;
	}
}
	
window.addEventListener('load',doFirst,false);