/**
 * To get started install
 * express bodyparser jsonwebtoken express-jwt
 * via npm
 * command :-
 * npm install express bodyparser jsonwebtoken express-jwt --save
 */

// Bringing all the dependencies in
const express = require('express');
const bodyParser = require('body-parser');
const jwt = require('jsonwebtoken');
const exjwt = require('express-jwt');
var fs = require("fs");
var randtoken = require('rand-token');
var mysql = require('mysql');


var pool  = mysql.createPool({
    connectionLimit : 10,
    host: "10.0.50.50",
    user: "root",
    password: "irulez4database",
    database: "iRulez"
  });
  


const RSA_PRIVATE_KEY = fs.readFileSync('./private.key');

// Instantiating the express app
const app = express();


// See the react auth blog in which cors is required for access
app.use((req, res, next) => {
    res.setHeader('Access-Control-Allow-Origin', 'http://localhost:3000');
    res.setHeader('Access-Control-Allow-Headers', 'Content-type,Authorization');
    next();
});

// Setting up bodyParser to use json and set it to req.body
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

var refreshTokens = {}

// LOGIN ROUTE
app.post('/login', (req, res) => {
    const { username, password } = req.body;
    console.log("before validation")
    validateEmailAndPassword({email:username, password:password},
    function(returnValue){
        console.log(returnValue)
        if (returnValue != null) {
            console.log("Validation passed")
            // 60sec * 60min * 24u * 7d 
            const exp = 604800;
            var refreshToken = randtoken.uid(256) 
            const jwtBearerToken = createToken(returnValue, exp)         
            console.log("token " + jwtBearerToken);
            refreshTokens[refreshToken] = returnValue.email
            res.status(200).json({token: jwtBearerToken, expiresIn: exp, username: returnValue.email, refreshToken: refreshToken});
        }
        else{
            console.log("Validation failed");    
            res.status(401).json({
                    sucess: false,
                    token: null,
                    err: 'Username or password is incorrect'
                });
            }
        console.log('after else');
    }
    )

    
});


function createToken(returnValue, exp){
    return jwtBearerToken = jwt.sign({            
        algorithm: 'RS256',
        expiresIn: exp,
        username: returnValue.email,
        userid: returnValue.email, 
        role: returnValue.role},
        RSA_PRIVATE_KEY, { expiresIn: exp, algorithm: 'RS256'});
}

function  validateEmailAndPassword(credentials, callback){
    sql = "SELECT * FROM tbl_users where LOWER(email)='"+credentials.email.toLowerCase()+"' and password='" +credentials.password+"'";
    console.log(sql);
    pool.query(sql, function (err, result, fields) {
        if (err) throw err;
            if (result.length == 0) {
                console.log("return false");
                callback(null);
            }
            else{
                console.log(result[0].id);
                console.log('return true');
                callback({email:result[0].email, role:result[0].role});
            }
    });

}

// Error handling 
app.use(function (err, req, res, next) {
    if (err.name === 'UnauthorizedError') { // Send the error rather than to show it on the console
        res.status(401).send(err);
    }
    else {
        next(err);
    }
});

// Starting the app on PORT 3000
const PORT = 8080;
app.listen(PORT, () => {
    // eslint-disable-next-line
    console.log(`Magic happens on port ${PORT}`);
});
