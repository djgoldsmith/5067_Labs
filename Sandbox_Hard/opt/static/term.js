var term = new Terminal({cursorBlink: true,
			 cursorStyle: 'underline'
			});

term.setOption('theme', {"foreground": "#39ff14"})

var thePrompt = ">>> ";

term.open(document.getElementById('terminal'));
//term.write(thePrompt);

var index = 0;
var buffer = "";
var socket = io.connect();

function ab2str(buf) {
  return String.fromCharCode.apply(null, new Uint16Array(buf));
}


socket.on('connect', () => {
    //console.log("CONNECTED");
});

// handle the event sent with socket.send()
socket.on('message', data => {
    if (typeof(data) == "string"){
	var parts = data.split("\n");
	for (i=0; i<parts.length; i++){
	    term.write(parts[i]+"\r\n");
	}
    }
    else{
	term.write(data + "\r\n");
    }
    term.write(thePrompt);
});


term.onData(data => {
    //First the lower contoll chars
    var ord = data.charCodeAt(0);
    //Values lower than 32 are controll.
    //Also 127 is Delete
    if (ord < 32 || ord ==127) {
	//Deal with individual codes
	if (ord == 13){ //Newline
	    socket.send(buffer);
	    index = 0;
	    buffer = "";
	    term.write("\r\n");
	    //term.write(thePrompt);
	}
	else if (ord == 27) { //Ascii Controll Chars
	    //So the next part is the interesting bit
	    var ctlChar = data.substr(1) //Strip of the first part
	    if (ctlChar == "[C") {//Right Arrow
		//Sanity check
		if (index < buffer.length){
		    index += 1;
		    term.write(data);
		}
		else{
		    term.write("\x07");
		}
	    }else if (ctlChar == "[D") { //leftArrow
		if (index > 0){
		    index -= 1;
		    term.write(data);
		}
		else{
		    //Ring that Bell
		    term.write("\x07");
		}
	    }
	}
	else if (ord == 127){ //Deletes
	    //Decrement 
	    index -= 1;
	    
	    //Remove the character from the buffer
	    buffer = buffer.substring(0,index) + buffer.substring(index+1);
	    //And we can move the text backwards with Ascii Control sequences
	    term.write("\b\x1b[P");
	}
	return;
    }
    else{
	//Anything else we stash in the buffer
	if (index == buffer.length){
	    buffer += data;
	}
	else{
	    //Strings are immutable
	    buffer = buffer.substring(0,index) + data + buffer.substring(index+1);
	}
	index += 1;
	term.write(data);
    }

});

/* Linefeeds happen (But based on input linefeeds */
/*
term.onLineFeed(data => {
    console.log("LINEFEED");
    //term.write("\n");
});
 
*/
