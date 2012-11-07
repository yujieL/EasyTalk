// detect whether current browers support websocket
if (!window.WebSocket) {  
	alert("WebSocket is not supported by current browser!");  
} else{
	var websocket;
	function init() {  
		ws = new WebSocket( 
			"ws://localhost:9000?user='elvis'&&pw='123'");  
		ws.onmessage = function(evt) {  
			//alert msg when recieve it
			alert('server send:'+evt.data)
		};  

		ws.onclose = function() {  
		};  

		ws.onopen = function() {  
			// As a login successful, send a msg to server to tell others you have connected. 
			ws.send(ws+': I am coming');  
		};  
		return ws
	}
	window.onload = function(){
		// Automatically called by browser
		websocket = init();
	}
	
	function sendMSG(){
		// send your input to server
		var value = document.getElementById('input').value;
		websocket.send(value);
	}
}