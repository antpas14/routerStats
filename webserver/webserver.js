var express = require('express');
var app = express();

// Define static routes
app.use('/assets', express.static('assets'));
app.use('/js', express.static('js'));
app.use('/html', express.static('html'));

app.use(express.static(__dirname + '/html'));

app.get('/', function(req, res) {
    res.sendFile(__dirname + '/html/index2.html');
});

var server = require('http').createServer(app); 


var port = 3001;
console.log("Listening on " + port);
server.listen(port);

// Socket.io server listens to our app
var io = require('socket.io').listen(server);

// Retrieve periodically the JSON and send it to the frontend
setInterval(function() {
	function sendJSON(json) {
		console.log("Trying to send JSON ", json);
		try {
			io.emit('json', JSON.parse(json));
		}   
		catch (e) {
			console.log("Cannot send JSON " + json + ". Exception " + e);
		}   
	}   

	var exec = require('child_process').exec;
	var child;
	var command = "python ../backend/getJsonStats.py";
	child = exec(command,
	   	function (error, stdout, stderr) {
			sendJSON(stdout);
		if (error !== null) {
          		console.log('exec error: ' + error);
        	}
   	});
}, 10000); 
