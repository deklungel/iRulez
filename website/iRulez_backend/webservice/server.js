var express = require('express');
var app = express()
var jwt = require('jwt-simple');
const expressJwt = require('express-jwt');
var fs = require("fs");
var bodyParser = require('body-parser');
var mysql = require('mysql');


app.use( bodyParser.json() );       // to support JSON-encoded bodies
app.use(bodyParser.urlencoded({     // to support URL-encoded bodies
    extended: true
})); 

const RSA_PUBLIC_KEY = fs.readFileSync('./public.key');

const checkIfAuthenticated = expressJwt({
  secret: RSA_PUBLIC_KEY
});

var pool  = mysql.createPool({
  connectionLimit : 10,
  host: "10.0.50.50",
  user: "root",
  password: "irulez4database",
  database: "iRulez"
});

var con = mysql.createConnection({
  host: "10.0.50.50",
  user: "root",
  password: "irulez4database",
  database: "iRulez"
});

// con.connect(function(err) {
//   if (err) throw err;
//   console.log("Connected!");
// });


app.use(function(req, res, next) {
  res.header("Access-Control-Allow-Origin", "*");
  res.header("Access-Control-Allow-Headers", "Content-Type, Authorization");
  res.header('Access-Control-Allow-Methods', 'PUT, POST, GET, DELETE, OPTIONS');
  next();
});

app.get('/api/users',checkIfAuthenticated,
  function(req, res) {
    console.log("api/users");
    var token = fromHeaderOrQuerystring(req);
    try{
      var decoded = jwt.decode(token, RSA_PUBLIC_KEY);
      console.log(decoded.role) // bar
      getUsers(function(returnValue){
        res.json({users: returnValue.result})
        console.log(returnValue);
      });
    }
    catch(err){
      console.log(err) // bar
      res.sendStatus(401); 
    }
  });

  app.post('/api/AddUser',checkIfAuthenticated,
  function(req, res) {
    console.log("api/AddUser");
    var token = fromHeaderOrQuerystring(req);
    try{
      var decoded = jwt.decode(token, RSA_PUBLIC_KEY);
      console.log(decoded.role);
      console.log(req.body);
    }
    catch(err){
      console.log(err) // bar
      res.sendStatus(401); 
    }
  });

  function  getUsers(callback){
    sql = "SELECT id, email, role FROM tbl_users";
    console.log(sql);
    pool.query(sql, function (err, result, fields) {
        if (err) throw err;
            if (result.length == 0) {
                console.log("return false");
                callback(null);
            }
            else{
                callback({result});
            }
    });

}

app.put('/api/status', checkIfAuthenticated, function (req, res) {
  console.log(req.body.message);
  console.log("/api/status");
  res.sendStatus(204); 
});

  function fromHeaderOrQuerystring (req) {
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