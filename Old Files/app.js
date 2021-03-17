var express = require('express');
var http = require('http');
var bodyParser = require('body-parser');
var fs = require('fs');
var multer = require('multer');
var pyshell = require('python-shell');

var app = express();
var server = http.createServer(app);
app.set('port', process.env.PORT || 3001);
app.use(express.static(__dirname + '/public'));
app.use(bodyParser.json());

app.use(function (request, response, next) {
	response.setHeader("Access-Control-Allow-Methods", "POST, PUT, OPTIONS, DELETE, GET");
	response.header("Access-Control-Allow-Origin", "http://localhost");
	response.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
	next();
});

var storage = multer.diskStorage({
	destination: function (request, file, cb) {
		cb(null, __dirname + '/public/kgml/')
	},
	filename: function (request, file, cb) {
		var datetimestamp = Date.now();
		cb(null, file.fieldname + '-' + datetimestamp + '.' + file.originalname.split('.')[file.originalname.split('.').length - 1])
	}
});

var upload = multer({
	storage: storage
});

app.post('(/*)?/upload', upload.single('file'), function (request, response) {
	response.json(request.file.filename);
});

var options = {
	mode: 'text',
	pythonPath: 'python', //this may change between servers
	pythonOptions: ['-u'],
	scriptPath: 'python/',
	args: []
};

function pathToKMGL(filename) {
	return 'public/kgml/' + filename;
}

app.post('(/*)?/run', function (request, response) {
	options.args = []
	options.args.push(pathToKMGL(request.body.files[0]));
	options.args.push(pathToKMGL(request.body.files[1]));
	pyshell.run('main.py', options, function (err, results) {
		if (err) response.json("Error - revisar formato de los archivos");
		response.json(results);
	});	
});

server.listen(app.get('port'), function () {
	console.log('Express server listening on port ' + app.get('port'));
});