var express = require('express');
var app = express();
var jwt = require('jwt-simple');
const expressJwt = require('express-jwt');
var fs = require('fs');
var bodyParser = require('body-parser');
var mysql = require('mysql');
var md5 = require('md5');
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

var pool = mysql.createPool({
    connectionLimit: 10,
    host: config.database.server,
    user: config.database.user,
    password: config.database.password,
    database: config.database.database
});

app.use(function (req, res, next) {
    res.header('Access-Control-Allow-Origin', '*');
    res.header('Access-Control-Allow-Headers', 'Content-Type, Authorization');
    res.header('Access-Control-Allow-Methods', 'PUT, POST, GET, DELETE, OPTIONS');
    next();
});

app.get('/api/*', checkIfAuthenticated, function (req, res) {
    switch (req.url) {
        case '/api/users':
            get_user(req, res);
            break;
        case '/api/devices':
            get_devices(req, res);
            break;
        case '/api/actions':
            get_actions(req, res);
            break;
        default:
            console.log("response 404");
            res.sendStatus(404);
    }
});

app.delete('/api/*', checkIfAuthenticated, function (req, res) {
    switch (req.url) {
        case '/api/user/delete':
            user_delete(req, res);
            break;
        case '/api/device/delete':
            device_delete(req, res);
            break;
        default:
            console.log('response 404');
            res.sendStatus(404);
    }
});
app.put('/api/*', checkIfAuthenticated, function (req, res) {
    switch (req.url) {
        case "/api/user/edit":
            user_edit(req, res);
            break;
        case "/api/device/edit":
            device_edit(req, res);
            break;
        case "/api/user/changepassword":
            user_changePassword(req, res);
            break;
        default:
            console.log("response 404");
            res.sendStatus(404);
    }
});
app.post('/api/*', checkIfAuthenticated, function (req, res) {
    switch (req.url) {
        case '/api/user/add':
            user_add(req, res);
            break;
        case '/api/device/add':
            device_add(req, res);
            break;
        default:
            console.log('response 404');
            res.sendStatus(404);
    }
});

function get_user(req, res) {
    console.log(req.url);
    try {
        sql = 'SELECT id, email, role FROM tbl_users';
        processRequest(req, res, sql);
    } catch (err) {
        console.log(err); // bar
        res.sendStatus(500);
    }
}

function user_add(req, res) {
    try {
        var sql =
            "INSERT INTO tbl_users (email, role, password) VALUES ('" +
            req.body.email +
            "', '" +
            req.body.role +
            "','" +
            md5(req.body.password) +
            "')";
        processRequest(req, res, sql);
    } catch (err) {
        console.log(err); // bar
        res.sendStatus(500);
    }
}

function user_delete(req, res) {
    try {
        var sql = "DELETE FROM tbl_users WHERE id IN ('" + req.body.id.join("','") + "')";
        processRequest(req, res, sql);
    } catch (err) {
        console.log(err); // bar
        res.sendStatus(500);
    }
}

function user_edit(req, res) {
    try {
        var values = [];
        if (req.body.email) {
            values.push("email='" + req.body.email);
        }
        if (req.body.role) {
            values.push("role='" + req.body.role);
        }
        var sql = 'UPDATE tbl_users SET ' + values.join("', ") + "' WHERE id = " + req.body.id;
        processRequest(req, res, sql);
    } catch (err) {
        console.log(err); // bar
        res.sendStatus(500);
    }
}

function user_changePassword(req, res) {
    try {
        var sql = "UPDATE tbl_users SET password='" + md5(req.body.password) + "' WHERE id = " + req.body.id;
        processRequest(req, res, sql);
    } catch (err) {
        console.log(err); // bar
        res.sendStatus(500);
    }
}

function get_devices(req, res) {
    console.log(req.url);
    try {
        sql = 'SELECT id, name, mac, sn, version, ping, mqtt FROM tbl_Arduino';
        processRequest(req, res, sql);
    } catch (err) {
        console.log(err); // bar
        res.sendStatus(500);
    }
}
function device_add(req, res) {
    try {
        console.log(req.body);
        var sql =
            "INSERT INTO tbl_Arduino (name, mac, sn) VALUES ('" +
            req.body.name +
            "', '" +
            req.body.mac +
            "','" +
            req.body.sn +
            "')";
        processRequest(req, res, sql);
    } catch (err) {
        console.log(err); // bar
        res.sendStatus(500);
    }
}
function device_delete(req, res) {
    try {
        var sql = "DELETE FROM tbl_Arduino WHERE id IN ('" + req.body.id.join("','") + "')";
        processRequest(req, res, sql);
    } catch (err) {
        console.log(err); // bar
        res.sendStatus(500);
    }
}
function device_edit(req, res) {
    try {
        var values = [];
        if (req.body.name) {
            values.push("name='" + req.body.name);
        }
        if (req.body.mac) {
            values.push("mac='" + req.body.mac);
        }
        if (req.body.sn || req.body.sn === '') {
            values.push("sn='" + req.body.sn);
        }
        var sql = 'UPDATE tbl_Arduino SET ' + values.join("', ") + "' WHERE id = " + req.body.id;
        processRequest(req, res, sql);
    } catch (err) {
        console.log(err); // bar
        res.sendStatus(500);
    }
}

function get_actions(req, res) {
    console.log(req.url);
    try {
        sql = "SELECT\
    tbl_Action.id,\
    tbl_Action.name,\
    tbl_Action_Type.name as 'type',\
    tbl_Trigger.seconds_down,\
    tbl_Trigger_Type.name as 'tigger_type',\
    tbl_Action.delay,\
    tbl_Action.timer,\
    tbl_Condition.name as 'condition',\
    tbl_OutputPin.name as 'master',\
    tbl_Master_Dimmers.name as 'dimmer',\
    tbl_Action.click_number,\
    tbl_Action.dimmer_speed,\
    tbl_Action.dimmer_light_value,\
    tbl_Action.cancel_on_button_release,\
    (SELECT GROUP_CONCAT(tbl_Action_Notification.Notification_id) from tbl_Action_Notification WHERE tbl_Action_Notification.Action_id = tbl_Action.id) as 'notifications',\
    (SELECT GROUP_CONCAT(tbl_OutputPin.name) from tbl_Action_OutputPin INNER JOIN tbl_OutputPin ON tbl_Action_OutputPin.OutputPin_ID = tbl_OutputPin.id WHERE tbl_Action_OutputPin.Action_id = tbl_Action.id ) as 'outputs'\
    FROM tbl_Action\
    INNER JOIN tbl_Action_Type ON tbl_Action.action_type =tbl_Action_Type.id\
    INNER JOIN tbl_Trigger ON tbl_Action.trigger_id =tbl_Trigger.id\
    INNER JOIN tbl_Trigger_Type ON tbl_Trigger.trigger_type =tbl_Trigger_Type.id\
    LEFT JOIN tbl_Condition ON tbl_Action.condition_id = tbl_Condition.id\
    LEFT JOIN tbl_Master_Dimmers ON tbl_Action.dim_master_id = tbl_Master_Dimmers.id\
    LEFT JOIN tbl_OutputPin ON tbl_Action.master_id = tbl_OutputPin.id";
        processRequest(req, res, sql)
    }
    catch (err) {
        console.log(err) // bar
        res.sendStatus(500);
    }
}

function processRequest(req, res, sql) {
    try {
        console.log(req.url);
        var token = fromHeaderOrQuerystring(req);
        var decoded = jwt.decode(token, RSA_PUBLIC_KEY);
        console.log(sql);
        executeQuery(
            sql,
            function (result) {
                res.json(result);
                console.log('result: ' + result);
            },
            function (errorMessage) {
                console.log('errorMessage ' + errorMessage);
                res.statusMessage = errorMessage;
                res.status(400).send();
            }
        );
    } catch (ex) {
        console.log('error ' + ex);
    }
}
function executeQuery(sql, onSuccess, onFailure) {
    pool.query(sql, function (err, result) {
        if (err) {
            if (err.code === 'ER_DUP_ENTRY') {
                onFailure(new Error('Duplicate User'));
            } else {
                onFailure(new Error('something bad happened'));
            }
        } else {
            onSuccess({ response: result });
        }
    });
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
