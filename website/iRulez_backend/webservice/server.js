var express = require('express');
var app = express()
var jwt = require('jwt-simple');
const expressJwt = require('express-jwt');
var fs = require("fs");
var bodyParser = require('body-parser');
var mysql = require('mysql');


app.use(bodyParser.json());       // to support JSON-encoded bodies
app.use(bodyParser.urlencoded({     // to support URL-encoded bodies
  extended: true
}));

const RSA_PUBLIC_KEY = fs.readFileSync('./public.key');

const checkIfAuthenticated = expressJwt({
  secret: RSA_PUBLIC_KEY
});

var pool = mysql.createPool({
  connectionLimit: 10,
  host: "10.0.50.50",
  user: "root",
  password: "irulez4database",
  database: "iRulez"
});


app.use(function (req, res, next) {
  res.header("Access-Control-Allow-Origin", "*");
  res.header("Access-Control-Allow-Headers", "Content-Type, Authorization");
  res.header('Access-Control-Allow-Methods', 'PUT, POST, GET, DELETE, OPTIONS');
  next();
});

app.get('/api/*', checkIfAuthenticated,
  function (req, res) {
    switch (req.url) {
      case '/api/users':
        get_user(req,res);
        break;
      default:
        console.log("response 501");
        res.sendStatus(501);
    }
  })

app.post('/api/user/*', checkIfAuthenticated,
  function (req, res) {
    switch (req.url) {
      case "/api/user/add":
        user_add(req, res);
        break;
      case "/api/user/delete":
        user_delete(req, res);
        break;
      case "/api/user/edit":
        user_edit(req, res);
        break;
      default:
        console.log("response 501");
        res.sendStatus(501);
    }

  });

  function get_user(req,res){
    console.log(req.url);
    try {
      sql = "SELECT id, email, role FROM tbl_users";
      processRequest(req, res, sql)
    }
    catch (err) {
      console.log(err) // bar
      res.sendStatus(401);
    }
  }

function user_add(req, res) {
  try {
    var sql = "INSERT INTO tbl_users (email, role, password) VALUES ('" + req.body.email + "', '" + req.body.role + "','" + req.body.password + "')";
    processRequest(req, res, sql)
  }
  catch (err) {
    console.log(err) // bar
    res.sendStatus(405);
  }
}

function user_delete(req, res) {
  try {
    var sql = "DELETE FROM tbl_users WHERE id IN ('" + req.body.id.join("','") + "')";
    processRequest(req, res, sql)
  }
  catch (err) {
    console.log(err) // bar
    res.sendStatus(405);
  }
}
function user_edit(req, res) {
  try {
    var values = [];
    if (req.body.email) {
      values.push("email='" + req.body.email)
    }
    if (req.body.role) {
      values.push("role='" + req.body.role)
    }
    var sql = "UPDATE tbl_users SET " + values.join("', ") + "' WHERE id = " + req.body.id;
    processRequest(req, res, sql)
  }
  catch (err) {
    console.log(err) // bar
    res.sendStatus(405);
  }
}

function processRequest(req, res, sql) {
  console.log(req.url);
  var token = fromHeaderOrQuerystring(req);
  var decoded = jwt.decode(token, RSA_PUBLIC_KEY);
  console.log(sql)
  executeQuery(sql,function (result) {
    res.json( result )
    console.log (result)
  })
}
function executeQuery(sql, callback) {
  pool.query(sql, function (err, result) {
    if (err) throw err;
    callback({users: result});
  })
}


function fromHeaderOrQuerystring(req) {
  if (req.headers.authorization && req.headers.authorization.split(' ')[0] === 'Bearer') {
    return req.headers.authorization.split(' ')[1];
  } else if (req.query && req.query.token) {
    return req.query.token;
  }
  return null;
}


port = 4002
app.listen(port);
console.log('Server running... port ' + port);