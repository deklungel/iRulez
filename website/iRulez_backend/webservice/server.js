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
    database: config.database.database,
    multipleStatements: true
});

app.use(function(req, res, next) {
    res.header('Access-Control-Allow-Origin', '*');
    res.header('Access-Control-Allow-Headers', 'Content-Type, Authorization');
    res.header('Access-Control-Allow-Methods', 'PUT, POST, GET, DELETE, OPTIONS');
    next();
});

app.get('/api/field/*', checkIfAuthenticated, function(req, res) {
    switch (req.url) {
        case '/api/field/triggers':
            get_field_triggers(req, res);
            break;
        case '/api/field/groups':
            get_field_groups(req, res);
            break;
        case '/api/field/action_types':
            get_field_action_types(req, res);
            break;
        case '/api/field/outputs':
            get_field_outputs(req, res);
            break;
        case '/api/field/actions':
            get_field_actions(req, res);
            break;
        case '/api/field/conditions':
            get_field_conditions(req, res);
            break;
        case '/api/field/templates':
            get_field_templates(req, res);
            break;
        case '/api/field/output_type':
            get_field_output_types(req, res);
            break;
        case '/api/field/menus':
            get_field_menus(req, res);
            break;
        case '/api/field/notifications':
            get_field_notifications(req, res);
            break;

        default:
            console.log('response 404 => unknown url:' + req.url);
            res.sendStatus(404);
    }
});

app.get('/api/*', checkIfAuthenticated, function(req, res) {
    switch (req.url) {
        case '/api/users':
            /*done */
            get_user(req, res);
            break;
        case '/api/groups':
            /*done */
            get_group(req, res);
            break;
        case '/api/devices':
            get_devices(req, res);
            break;
        case '/api/outputs':
            get_outputs(req, res);
            break;
        case '/api/inputs':
            get_inputs(req, res);
            break;
        case '/api/menus':
            get_menus(req, res);
            break;
        case '/api/actions':
            get_actions(req, res);
            break;
        case '/api/dimmeractions':
            get_dimmer_actions(req, res);
            break;

        default:
            console.log('response 404 => unknown url:' + req.url);
            res.sendStatus(404);
    }
});

app.delete('/api/*', checkIfAuthenticated, function(req, res) {
    switch (req.url) {
        case '/api/user/delete':
            /*done */
            user_delete(req, res);
            break;
        case '/api/group/delete':
            /*done */
            group_delete(req, res);
            break;
        case '/api/device/delete':
            device_delete(req, res);
            break;
        case '/api/action/delete':
            action_delete(req, res);
            break;
        case '/api/menu/delete':
            menu_delete(req, res);
            break;
        default:
            console.log('response 404');
            res.sendStatus(404);
    }
});
app.put('/api/*', checkIfAuthenticated, function(req, res) {
    switch (req.url) {
        case '/api/user/edit':
            /*done */
            user_edit(req, res);
            break;
        case '/api/group/edit':
            group_edit(req, res);
            break;
        case '/api/device/edit':
            device_edit(req, res);
            break;
        case '/api/output/edit':
            output_edit(req, res);
            break;
        case '/api/input/edit':
            input_edit(req, res);
            break;
        case '/api/action/edit':
            action_edit(req, res);
            break;
        case '/api/menu/edit':
            menu_edit(req, res);
            break;
        case '/api/user/changepassword':
            /*done */
            user_changePassword(req, res);
            break;
        default:
            console.log('response 404');
            res.sendStatus(404);
    }
});
app.post('/api/*', checkIfAuthenticated, function(req, res) {
    switch (req.url) {
        case '/api/user/add':
            /*done */
            user_add(req, res);
            break;
        case '/api/group/add':
            /*done */
            group_add(req, res);
            break;
        case '/api/menu/add':
            menu_add(req, res);
            break;
        case '/api/device/add':
            device_add(req, res);
            break;
        case '/api/action/add':
            action_add(req, res);
            break;
        default:
            console.log('response 404');
            res.sendStatus(404);
    }
});

// function get_user(req, res) {
//     console.log(req.url);
//     try {
//         sql =
//             'SELECT tbl_Users.id, email, role, group_id, tbl_Groups.name as group_name \
//             FROM tbl_Users INNER JOIN tbl_Groups ON tbl_Groups.id =tbl_Users.group_id ';
//         processRequest(req, res, sql);
//     } catch (err) {
//         console.log(err); // bar
//         res.sendStatus(500);
//     }
// }

// function user_add(req, res) {
//     try {
//         var sql =
//             "INSERT INTO tbl_Users (email, role, group_id, password) VALUES ('" +
//             req.body.email +
//             "', '" +
//             req.body.role +
//             "', '" +
//             req.body.group_id +
//             "','" +
//             md5(req.body.password) +
//             "')";
//         processRequest(req, res, sql);
//     } catch (err) {
//         console.log(err); // bar
//         res.sendStatus(500);
//     }
// }

// function user_delete(req, res) {
//     try {
//         var sql = "DELETE FROM tbl_Users WHERE id IN ('" + req.body.id.join("','") + "')";
//         processRequest(req, res, sql);
//     } catch (err) {
//         console.log(err); // bar
//         res.sendStatus(500);
//     }
// }

// function user_edit(req, res) {
//     try {
//         var values = [];
//         if (req.body.email) {
//             values.push("email='" + req.body.email);
//         }
//         if (req.body.role) {
//             values.push("role='" + req.body.role);
//         }
//         if (req.body.group_id) {
//             values.push("group_id='" + req.body.group_id);
//         }
//         var sql = 'UPDATE tbl_Users SET ' + values.join("', ") + "' WHERE id = " + req.body.id;
//         processRequest(req, res, sql);
//     } catch (err) {
//         console.log(err); // bar
//         res.sendStatus(500);
//     }
// }

// function user_changePassword(req, res) {
//     try {
//         var sql = "UPDATE tbl_Users SET password='" + md5(req.body.password) + "' WHERE id = " + req.body.id;
//         processRequest(req, res, sql);
//     } catch (err) {
//         console.log(err); // bar
//         res.sendStatus(500);
//     }
// }

// function get_group(req, res) {
//     console.log(req.url);
//     try {
//         sql =
//             "SELECT id, name, \
//         (SELECT GROUP_CONCAT(tbl_Users.email) from tbl_Users WHERE tbl_Users.group_id = tbl_Groups.id ) as 'users' \
//         FROM tbl_Groups";
//         processRequest(req, res, sql);
//     } catch (err) {
//         console.log(err); // bar
//         res.sendStatus(500);
//     }
// }
// function group_add(req, res) {
//     try {
//         console.log(req.body);
//         var sql = "INSERT INTO tbl_Groups (name) VALUES ('" + req.body.name + "')";
//         processRequest(req, res, sql);
//     } catch (err) {
//         console.log(err); // bar
//         res.sendStatus(500);
//     }
// }

// function group_delete(req, res) {
//     try {
//         var sql = "DELETE FROM tbl_Groups WHERE id IN ('" + req.body.id.join("','") + "')";
//         processRequest(req, res, sql);
//     } catch (err) {
//         console.log(err); // bar
//         res.sendStatus(500);
//     }
// }
// function group_edit(req, res) {
//     try {
//         var values = [];
//         if (req.body.name) {
//             values.push("name='" + req.body.name);
//         }
//         var sql = 'UPDATE tbl_Groups SET ' + values.join("', ") + "' WHERE id = " + req.body.id;
//         processRequest(req, res, sql);
//     } catch (err) {
//         console.log(err); // bar
//         res.sendStatus(500);
//     }
// }

function get_devices(req, res) {
    console.log(req.url);
    try {
        sql =
            'SELECT tbl_Arduino.id, tbl_Arduino.name, tbl_Arduino.mac, tbl_Arduino.sn, version, ping,tbl_Arduino.template_id,\
            tbl_Template.name as "template_name", mqtt FROM tbl_Arduino\
            INNER JOIN tbl_Template ON tbl_Template.id = tbl_Arduino.template_id';
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
            "INSERT INTO tbl_Arduino (name, mac, sn, template_id) VALUES ('" +
            req.body.name +
            "', '" +
            req.body.mac +
            "','" +
            req.body.sn +
            "','" +
            req.body.template_id +
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
function get_outputs(req, res) {
    console.log(req.url);
    try {
        sql =
            'SELECT tbl_OutputPin.id,tbl_OutputPin.type, tbl_OutputPin_Type.name as type_name, tbl_OutputPin.name,tbl_OutputPin.number, tbl_Arduino.name as device_name FROM tbl_OutputPin\
            INNER JOIN tbl_Arduino ON tbl_Arduino.id = tbl_OutputPin.parent_id\
            INNER JOIN tbl_OutputPin_Type ON tbl_OutputPin_Type.id = tbl_OutputPin.type';
        processRequest(req, res, sql);
    } catch (err) {
        console.log(err); // bar
        res.sendStatus(500);
    }
}
function output_edit(req, res) {
    try {
        var values = [];
        if (req.body.name) {
            values.push("name='" + req.body.name);
        }
        if (req.body.type) {
            sqlcheck =
                "SELECT COUNT(tbl_Action_OutputPin.OutputPin_ID) AS 'counter' FROM tbl_Action_OutputPin WHERE tbl_Action_OutputPin.OutputPin_ID=" +
                req.body.id;
            processRequest_withReturn(req, res, sqlcheck, function(result) {
                if (parseInt(result.response[0].counter) == 0) {
                    values.push("type='" + req.body.type);
                    var sql = 'UPDATE tbl_OutputPin SET ' + values.join("', ") + "' WHERE id = " + req.body.id;
                    processRequest(req, res, sql);
                } else {
                    res.statusMessage = 'Output pin exist in action';
                    res.status(400).end();
                }
            });
        } else {
            var sql = 'UPDATE tbl_OutputPin SET ' + values.join("', ") + "' WHERE id = " + req.body.id;
            processRequest(req, res, sql);
        }
    } catch (err) {
        console.log(err); // bar
        res.serverError(err);
    }
}

function get_inputs(req, res) {
    console.log(req.url);
    try {
        sql =
            "SELECT tbl_InputPin.id,tbl_InputPin.name,tbl_InputPin.number,tbl_InputPin.time_between_clicks, tbl_Arduino.name as device_name,\
            (SELECT GROUP_CONCAT(tbl_Action.name) FROM tbl_InputPin_Action INNER JOIN tbl_Action ON tbl_InputPin_Action.Action_ID = tbl_Action.id WHERE tbl_InputPin_Action.InputPin_ID = tbl_InputPin.id ) as 'actions',\
            (SELECT GROUP_CONCAT(tbl_Action.id) FROM tbl_InputPin_Action INNER JOIN tbl_Action ON tbl_InputPin_Action.Action_ID = tbl_Action.id WHERE tbl_InputPin_Action.InputPin_ID = tbl_InputPin.id ) as 'actions_id'\
            FROM tbl_InputPin\
            INNER JOIN tbl_Arduino ON tbl_Arduino.id = tbl_InputPin.parent_id";
        processRequest(req, res, sql);
    } catch (err) {
        console.log(err); // bar
        res.sendStatus(500);
    }
}
function input_edit(req, res) {
    try {
        var values = [];
        if (req.body.name) {
            values.push("name='" + req.body.name);
        }
        if (req.body.time_between_clicks) {
            values.push("time_between_clicks='" + req.body.time_between_clicks);
        }
        if (req.body.time_between_clicks == '') {
            values.push("time_between_clicks=NULL'");
        }
        var sql = 'UPDATE tbl_InputPin SET ' + values.join("', ") + "' WHERE id = " + req.body.id;
        sql = sql.replace("''", '');

        var sql_action = '';
        if (values.length > 0) {
            sql_action = sql + ';';
        }
        if (req.body.actions_id) {
            sql_action = sql_action + 'DELETE FROM `tbl_InputPin_Action` WHERE  InputPin_ID = ' + req.body.id + ';';
            if (req.body.actions_id.length > 0) {
                sql_action = sql_action + 'INSERT INTO tbl_InputPin_Action ( InputPin_ID ,Action_ID) VALUES ';
                req.body.actions_id.map(id => {
                    sql_action = sql_action + '(' + parseInt(req.body.id) + ',' + parseInt(id) + '),';
                });
                sql_action = sql_action.replace(/.$/, ';');
            }
        }

        processRequest(req, res, sql_action);
    } catch (err) {
        console.log(err); // bar
        res.sendStatus(500);
    }
}

function get_actions(req, res) {
    console.log(req.url);
    try {
        sql =
            "SELECT\
    tbl_Action.id,\
    tbl_Action.name,\
    tbl_Action.action_type as 'action_type',\
    tbl_Action_Type.name as 'action_type_name',\
    tbl_Action.trigger_id as 'trigger',\
    tbl_Trigger.seconds_down as 'trigger_seconds_down',\
    tbl_Trigger.name as 'trigger_name',\
    tbl_Action.delay,\
    tbl_Action.timer,\
    tbl_Action.condition_id as 'condition_id',\
    tbl_Condition.name as 'condition',\
    tbl_Action.master_id as 'master_id',\
    tbl_OutputPin.name as 'master',\
    tbl_Action.click_number,\
    (SELECT GROUP_CONCAT(tbl_Notification.name) from tbl_Action_Notification INNER JOIN tbl_Notification on tbl_Action_Notification.Notification_id = tbl_Notification.id WHERE tbl_Action_Notification.Action_id = tbl_Action.id) as 'notifications',\
    (SELECT GROUP_CONCAT(tbl_Notification.id) from tbl_Action_Notification INNER JOIN tbl_Notification on tbl_Action_Notification.Notification_id = tbl_Notification.id WHERE tbl_Action_Notification.Action_id = tbl_Action.id) as 'notifications_id',\
    (SELECT GROUP_CONCAT(tbl_OutputPin.name) from tbl_Action_OutputPin INNER JOIN tbl_OutputPin ON tbl_Action_OutputPin.OutputPin_ID = tbl_OutputPin.id WHERE tbl_Action_OutputPin.Action_id = tbl_Action.id ) as 'outputs',\
    (SELECT GROUP_CONCAT(tbl_OutputPin.id) from tbl_Action_OutputPin INNER JOIN tbl_OutputPin ON tbl_Action_OutputPin.OutputPin_ID = tbl_OutputPin.id WHERE tbl_Action_OutputPin.Action_id = tbl_Action.id ) as 'outputs_id'\
    FROM tbl_Action \
    INNER JOIN tbl_Action_Type ON tbl_Action.action_type =tbl_Action_Type.id\
    INNER JOIN tbl_Trigger ON tbl_Action.trigger_id =tbl_Trigger.id\
    LEFT JOIN tbl_Condition ON tbl_Action.condition_id = tbl_Condition.id\
    LEFT JOIN tbl_OutputPin ON tbl_Action.master_id = tbl_OutputPin.id\
    WHERE tbl_Action.action_type <= 3";
        processRequest(req, res, sql);
    } catch (err) {
        console.log(err); // bar
        res.sendStatus(500);
    }
}
function get_dimmer_actions(req, res) {
    console.log(req.url);
    try {
        sql =
            "SELECT\
    tbl_Action.id,\
    tbl_Action.name,\
    tbl_Action.action_type as 'action_type',\
    tbl_Action_Type.name as 'action_type_name',\
    tbl_Action.trigger_id as 'trigger',\
    tbl_Trigger.seconds_down as 'trigger_seconds_down',\
    tbl_Trigger.name as 'trigger_name',\
    tbl_Action.delay,\
    tbl_Action.timer,\
    tbl_Action.condition_id as 'condition_id',\
    tbl_Condition.name as 'condition',\
    tbl_Action.master_id as 'master_id',\
    tbl_OutputPin.name as 'master',\
    tbl_Action.click_number,\
    (SELECT GROUP_CONCAT(tbl_Notification.name) from tbl_Action_Notification INNER JOIN tbl_Notification on tbl_Action_Notification.Notification_id = tbl_Notification.id WHERE tbl_Action_Notification.Action_id = tbl_Action.id) as 'notifications',\
    (SELECT GROUP_CONCAT(tbl_Notification.id) from tbl_Action_Notification INNER JOIN tbl_Notification on tbl_Action_Notification.Notification_id = tbl_Notification.id WHERE tbl_Action_Notification.Action_id = tbl_Action.id) as 'notifications_id',\
    (SELECT GROUP_CONCAT(tbl_OutputPin.name) from tbl_Action_OutputPin INNER JOIN tbl_OutputPin ON tbl_Action_OutputPin.OutputPin_ID = tbl_OutputPin.id WHERE tbl_Action_OutputPin.Action_id = tbl_Action.id ) as 'outputs',\
    (SELECT GROUP_CONCAT(tbl_OutputPin.id) from tbl_Action_OutputPin INNER JOIN tbl_OutputPin ON tbl_Action_OutputPin.OutputPin_ID = tbl_OutputPin.id WHERE tbl_Action_OutputPin.Action_id = tbl_Action.id ) as 'outputs_id'\
    FROM tbl_Action \
    INNER JOIN tbl_Action_Type ON tbl_Action.action_type =tbl_Action_Type.id\
    INNER JOIN tbl_Trigger ON tbl_Action.trigger_id =tbl_Trigger.id\
    LEFT JOIN tbl_Condition ON tbl_Action.condition_id = tbl_Condition.id\
    LEFT JOIN tbl_OutputPin ON tbl_Action.master_id = tbl_OutputPin.id\
    WHERE tbl_Action.action_type > 4";
        processRequest(req, res, sql);
    } catch (err) {
        console.log(err); // bar
        res.sendStatus(500);
    }
}
function action_add(req, res) {
    try {
        if (req.body.timer === '') {
            req.body.timer = 0;
        }
        if (req.body.delay === '') {
            req.body.delay = 0;
        }
        var sql =
            "INSERT INTO tbl_Action (name, action_type, trigger_id, delay, timer,master_id, condition_id, click_number) VALUES ('" +
            req.body.name +
            "', '" +
            req.body.action_type +
            "','" +
            req.body.trigger +
            "', '" +
            req.body.delay +
            "', '" +
            (req.body.action_type !== '1' ? req.body.timer : null) +
            "', " +
            (req.body.master === '' ? null : req.body.action_type === '1' ? req.body.master : null) +
            ', ' +
            (req.body.condition_id === '' ? null : "'" + req.body.condition_id + "'") +
            ", '" +
            req.body.click_number +
            "')";
        processRequest_withReturn(req, res, sql, function(result) {
            var sql_action =
                'UPDATE tbl_Action SET timer=IF(action_type=1, 0, tbl_Action.timer), master_id=IF(action_type <> 1, null, master_id) WHERE id = ' +
                parseInt(result.response.insertId) +
                ';';
            if (req.body.outputs_id.length > 0) {
                sql_action = sql_action + 'INSERT INTO `tbl_Action_OutputPin` (`Action_ID`, `OutputPin_ID`) VALUES ';
                req.body.outputs_id.map(id => {
                    sql_action = sql_action + '(' + parseInt(result.response.insertId) + ',' + parseInt(id) + '),';
                });
                sql_action = sql_action.replace(/.$/, ';');
            }

            if (req.body.notifications_id.length > 0) {
                sql_action =
                    sql_action + 'INSERT INTO `tbl_Action_Notification` (`Action_ID`, `Notification_id`) VALUES ';
                req.body.notifications_id.map(id => {
                    sql_action = sql_action + '(' + parseInt(result.response.insertId) + ',' + parseInt(id) + '),';
                });
                sql_action = sql_action.replace(/.$/, ';');
            }

            processRequest(req, res, sql_action);
        });
    } catch (err) {
        console.log(err); // bar
        res.sendStatus(500);
    }
}

function action_delete(req, res) {
    try {
        var sql = "DELETE FROM tbl_Action WHERE id IN ('" + req.body.id.join("','") + "')";
        processRequest(req, res, sql);
    } catch (err) {
        console.log(err); // bar
        res.sendStatus(500);
    }
}
function action_edit(req, res) {
    try {
        var values = [];
        if (req.body.name) {
            values.push("name='" + req.body.name);
        }
        if (req.body.action_type) {
            values.push("action_type='" + req.body.action_type);
        }
        if (req.body.trigger_id) {
            values.push("trigger_id='" + req.body.trigger_id);
        }
        if (req.body.delay) {
            values.push("delay='" + req.body.delay);
        }
        if (req.body.timer) {
            values.push("timer='" + req.body.timer);
        }
        if (req.body.master_id) {
            values.push("master_id='" + req.body.master_id);
        }
        if (req.body.condition_id) {
            values.push("condition_id='" + req.body.condition_id);
        }
        if (req.body.click_number) {
            values.push("click_number='" + req.body.click_number);
        }
        if (req.body.click_number) {
            values.push("click_number='" + req.body.click_number);
        }
        var sql_action = '';
        if (values.length > 0) {
            sql_action = 'UPDATE tbl_Action SET ' + values.join("', ") + "' WHERE id = " + req.body.id + ';';
        }
        if (req.body.outputs_id) {
            sql_action = sql_action + 'DELETE FROM `tbl_Action_OutputPin` WHERE  Action_ID = ' + req.body.id + ';';
            if (req.body.outputs_id.length > 0) {
                sql_action = sql_action + 'INSERT INTO `tbl_Action_OutputPin` (`Action_ID`, `OutputPin_ID`) VALUES ';
                req.body.outputs_id.map(id => {
                    sql_action = sql_action + '(' + parseInt(req.body.id) + ',' + parseInt(id) + '),';
                });
                sql_action = sql_action.replace(/.$/, ';');
            }
        }
        if (req.body.notifications_id) {
            sql_action = sql_action + 'DELETE FROM `tbl_Action_Notification` WHERE  Action_ID = ' + req.body.id + ';';
            if (req.body.notifications_id.length > 0) {
                sql_action =
                    sql_action + 'INSERT INTO `tbl_Action_Notification` (`Action_ID`, `Notification_id`) VALUES ';
                req.body.notifications_id.map(id => {
                    sql_action = sql_action + '(' + parseInt(req.body.id) + ',' + parseInt(id) + '),';
                });
                sql_action = sql_action.replace(/.$/, ';');
            }
        }
        sql_action =
            sql_action +
            'UPDATE tbl_Action SET timer=IF(action_type=1, 0, tbl_Action.timer), master_id=IF(action_type <> 1, null, master_id) WHERE id = ' +
            req.body.id +
            ';';
        processRequest(req, res, sql_action);
    } catch (err) {
        console.log(err); // bar
        res.sendStatus(500);
    }
}

async function get_menus(req, res) {
    try {
        sql =
            'SELECT tbl_Menu.id, tbl_Menu.name, tbl_Menu.parent, tbl_Menu.order FROM tbl_Menu where tbl_Menu.parent is null order by tbl_Menu.order';
        to_return = [];
        var result_parent = await processRequest_promise(sql);
        for (var parent of result_parent) {
            to_return.push(parent);
            sql =
                'SELECT tbl_Menu.id, tbl_Menu.name,CONCAT("--"\
                ,name) as display_name, tbl_Menu.parent, tbl_Menu.order,\
                (SELECT tbl_Menu.name FROM tbl_Menu WHERE  tbl_Menu.id = ' +
                parent.id +
                ') as parent_name\
                FROM tbl_Menu where tbl_Menu.parent = ' +
                parent.id +
                ' order by tbl_Menu.order';
            console.log(sql);
            var result_child = await processRequest_promise(sql);
            for (var child of result_child) {
                to_return.push(child);
                sql =
                    'SELECT tbl_Menu.id, tbl_Menu.name,CONCAT("------"\
                    ,name) as display_name, tbl_Menu.parent, tbl_Menu.order,\
                (SELECT tbl_Menu.name FROM tbl_Menu WHERE  tbl_Menu.id = ' +
                    child.id +
                    ') as parent_name\
                FROM tbl_Menu where tbl_Menu.parent = ' +
                    child.id +
                    ' order by tbl_Menu.order';
                var result_grandchild = await processRequest_promise(sql);
                for (var grandchild of result_grandchild) {
                    to_return.push(grandchild);
                }
            }
        }
        res.json({ response: to_return });
        console.log('result: ' + to_return);
    } catch (err) {
        console.log(err); // bar
    }
}

function processRequest_promise(sql) {
    // Return new promise
    return new Promise(function(resolve, reject) {
        // Do async job
        executeQuery(
            sql,
            function(result) {
                resolve(result.response);
            },
            function(err) {
                reject(err);
            }
        );
    });
}

function menu_add(req, res) {
    try {
        if (req.body.parent == '') {
            var sql = "INSERT INTO tbl_Menu (name, parent) VALUES ('" + req.body.name + "',null)";
        } else {
            var sql = "INSERT INTO tbl_Menu (name, parent) VALUES ('" + req.body.name + "','" + req.body.parent + "')";
        }

        processRequest(req, res, sql);
    } catch (err) {
        console.log(err); // bar
        res.sendStatus(500);
    }
}

function menu_delete(req, res) {
    try {
        var sql = "DELETE FROM tbl_Menu WHERE id IN ('" + req.body.id.join("','") + "')";
        processRequest(req, res, sql);
    } catch (err) {
        console.log(err); // bar
        res.sendStatus(500);
    }
}
function menu_edit(req, res) {
    try {
        var values = [];
        if (req.body.name) {
            values.push("name='" + req.body.name);
        }
        if (req.body.parent) {
            values.push("parent='" + req.body.parent);
        }

        var sql = 'UPDATE tbl_Menu SET ' + values.join("', ") + "' WHERE id = " + req.body.id;
        processRequest(req, res, sql);
    } catch (err) {
        console.log(err); // bar
        res.sendStatus(500);
    }
}
function get_field_triggers(req, res) {
    console.log(req.url);
    try {
        sql = 'SELECT tbl_Trigger.id as "id", tbl_Trigger.name as "name" from tbl_Trigger';
        processRequest(req, res, sql);
    } catch (err) {
        console.log(err); // bar
        res.sendStatus(500);
    }
}
function get_field_groups(req, res) {
    console.log(req.url);
    try {
        sql = 'SELECT tbl_Groups.id as "id", tbl_Groups.name as "name" from tbl_Groups';
        processRequest(req, res, sql);
    } catch (err) {
        console.log(err); // bar
        res.sendStatus(500);
    }
}
function get_field_action_types(req, res) {
    console.log(req.url);
    try {
        sql = 'SELECT tbl_Action_Type.id as "id", tbl_Action_Type.name as "name" from tbl_Action_Type WHERE id <= 3';
        processRequest(req, res, sql);
    } catch (err) {
        console.log(err); // bar
        res.sendStatus(500);
    }
}
function get_field_output_types(req, res) {
    console.log(req.url);
    try {
        sql = 'SELECT tbl_OutputPin_Type.id as "id", tbl_OutputPin_Type.name as "name" from tbl_OutputPin_Type';
        processRequest(req, res, sql);
    } catch (err) {
        console.log(err); // bar
        res.sendStatus(500);
    }
}
function get_field_outputs(req, res) {
    console.log(req.url);
    try {
        sql = 'SELECT tbl_OutputPin.id, tbl_OutputPin.name from tbl_OutputPin WHERE type=0';
        processRequest(req, res, sql);
    } catch (err) {
        console.log(err); // bar
        res.sendStatus(500);
    }
}
function get_field_actions(req, res) {
    console.log(req.url);
    try {
        sql = 'SELECT tbl_Action.id, tbl_Action.name from tbl_Action';
        processRequest(req, res, sql);
    } catch (err) {
        console.log(err); // bar
        res.sendStatus(500);
    }
}
async function get_field_menus(req, res) {
    console.log(req.url);
    try {
        sql =
            'SELECT tbl_Menu.id, tbl_Menu.name, tbl_Menu.parent FROM tbl_Menu where tbl_Menu.parent is null order by tbl_Menu.order';
        to_return = [];
        console.log(sql);
        var result_parent = await processRequest_promise(sql);
        for (var parent of result_parent) {
            to_return.push(parent);
            sql =
                'SELECT tbl_Menu.id, tbl_Menu.name,CONCAT((SELECT tbl_Menu.name FROM tbl_Menu WHERE  tbl_Menu.id = ' +
                parent.id +
                ") ,' -- ',name) as name,\
                tbl_Menu.parent, tbl_Menu.order\
                FROM tbl_Menu where tbl_Menu.parent = " +
                parent.id +
                ' order by tbl_Menu.order';
            console.log(sql);
            var result_child = await processRequest_promise(sql);
            for (var child of result_child) {
                to_return.push(child);
            }
        }
        res.json({ response: to_return });
        console.log('result: ' + to_return);
    } catch (err) {
        console.log(err); // bar
        res.sendStatus(500);
    }
}
function get_field_templates(req, res) {
    console.log(req.url);
    try {
        sql = 'SELECT tbl_Template.id, tbl_Template.name from tbl_Template';
        processRequest(req, res, sql);
    } catch (err) {
        console.log(err); // bar
        res.sendStatus(500);
    }
}
function get_field_conditions(req, res) {
    console.log(req.url);
    try {
        sql = 'SELECT tbl_Condition.id, tbl_Condition.name from tbl_Condition';
        processRequest(req, res, sql);
    } catch (err) {
        console.log(err); // bar
        res.sendStatus(500);
    }
}
function get_field_notifications(req, res) {
    console.log(req.url);
    try {
        sql = 'SELECT tbl_Notification.id, tbl_Notification.name from tbl_Notification';
        processRequest(req, res, sql);
    } catch (err) {
        console.log(err); // bar
        res.sendStatus(500);
    }
}
function processRequest_withReturn(req, res, sql, onSuccess) {
    try {
        console.log(req.url);
        var token = fromHeaderOrQuerystring(req);
        var decoded = jwt.decode(token, RSA_PUBLIC_KEY);
        console.log(sql);
        executeQuery(
            sql,
            function(result) {
                console.log('result: ' + result);
                onSuccess(result);
            },
            function(errorMessage) {
                console.log('errorMessage ' + errorMessage);
                res.statusMessage = errorMessage;
                res.status(400).send();
            }
        );
    } catch (ex) {
        console.log('error ' + ex);
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
            function(result) {
                res.json(result);
                console.log('result: ' + result);
            },
            function(errorMessage) {
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
    pool.query(sql, function(err, result) {
        if (err) {
            if (err.code === 'ER_DUP_ENTRY') {
                onFailure(new Error('Duplicate Entry'));
            } else if (err.code === 'ER_ROW_IS_REFERENCED_2') {
                onFailure(new Error('Reference to this ID exists'));
            } else {
                console.log(err.code);
                console.log(err);
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
