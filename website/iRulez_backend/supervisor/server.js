var supervisord = require('supervisord');
var express = require('express');
var app = express();
var jwt = require('jwt-simple');
const expressJwt = require('express-jwt');
var fs = require('fs');
var bodyParser = require('body-parser');
const config = require('./config.json');
app.use(bodyParser.json()); // to support JSON-encoded bodies
app.use(
    bodyParser.urlencoded({
        // to support URL-encoded bodies
        extended: true
    })
);

const RSA_PUBLIC_KEY = fs.readFileSync(config.key);

const checkIfAuthenticated = expressJwt({
    secret: RSA_PUBLIC_KEY
});

var client = supervisord.connect('http://10.50.240.11:9001');

app.use(function(req, res, next) {
    res.header('Access-Control-Allow-Origin', '*');
    res.header('Access-Control-Allow-Headers', 'Content-Type, Authorization');
    res.header('Access-Control-Allow-Methods', 'PUT, POST, GET, DELETE, OPTIONS');
    next();
});

app.get('/api/*', checkIfAuthenticated, function(req, res) {
    switch (req.url) {
        case '/api/getAllProcesses':
            console.log(req.url);
            getAllProcessInfo(req, res);
            break;

        default:
            console.log('response 404 => unknown url:' + req.url);
            res.sendStatus(404);
    }
});

app.post('/api/*', checkIfAuthenticated, function(req, res) {
    switch (req.url) {
        case '/api/startProcces':
            startProcess(req, res);
            break;
        case '/api/stopProcces':
            stopProcess(req, res);
            break;
        case '/api/restartProcces':
            restartProcess(req, res);
            break;
        case '/api/clearLogs':
            clearLogs(req, res);
            break;
        case '/api/getProcessLog':
            console.log(req.url);
            getProcessLog(req, res);
            break;
        default:
            console.log('response 404 => unknown url:' + req.url);
            res.sendStatus(404);
    }
});

function getAllProcessInfo(req, res) {
    console.log(req.url);
    try {
        client.getAllProcessInfo(function(err, processes) {
            if (err) {
                console.log(err);
                res.sendStatus(500);
            } else {
                var token = fromHeaderOrQuerystring(req);
                var decoded = jwt.decode(token, RSA_PUBLIC_KEY);
                var to_return = [];
                processes.forEach(function(process) {
                    to_return.push({
                        name: process.name,
                        statename: process.statename,
                        start: process.start,
                        stop: process.stop,
                        now: process.now
                    });
                });
                res.json({ response: to_return });
                console.log(to_return);
            }
        });
    } catch (err) {
        console.log(err); // bar
        res.sendStatus(500);
    }
}
function startProcess(req, res) {
    try {
        console.log('restart process');
        console.log(req.body.process);
        client.startProcess(req.body.process, function(err, result) {
            res.json({ result: result });
        });
    } catch (err) {
        console.log(err); // bar
        res.sendStatus(500);
    }
}
function stopProcess(req, res) {
    try {
        console.log('restart process');
        console.log(req.body.process);
        client.stopProcess(req.body.process, function(err, result) {
            res.json({ result: result });
        });
    } catch (err) {
        console.log(err); // bar
        res.sendStatus(500);
    }
}

function restartProcess(req, res) {
    try {
        console.log('restart process');
        console.log(req.body.process);
        client.stopProcess(req.body.process, function(err, result) {
            client.startProcess(req.body.process, function(err, result) {
                res.json({ result: result });
            });
        });
    } catch (err) {
        console.log(err); // bar
        res.sendStatus(500);
    }
}
function clearLogs(req, res) {
    try {
        console.log('restart process');
        console.log(req.body.process);
        client.clearProcessLogs(req.body.process, function(err, result) {
            res.json({ result: result });
        });
    } catch (err) {
        console.log(err); // bar
        res.sendStatus(500);
    }
}
function getProcessLog(req, res) {
    try {
        console.log('log requested');
        console.log(req.body.process);
        client.tailProcessStdoutLog(req.body.process, 0, 10000, function(err, result) {
            console.log(result);
            res.json({ response: result });
        });
    } catch (err) {
        console.log(err); // bar
        res.sendStatus(500);
    }
}
function fromHeaderOrQuerystring(req) {
    if (req.headers.authorization && req.headers.authorization.split(' ')[0] === 'Bearer') {
        return req.headers.authorization.split(' ')[1];
    } else if (req.query && req.query.token) {
        return req.query.token;
    }
    return null;
}

const PORT = config.port;
app.listen(PORT, () => {
    console.log(`Webservice running on port ${PORT}`);
});
