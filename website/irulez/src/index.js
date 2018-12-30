import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';

import App from './App';
import Login from './components/Login'
import Admin from './components/admin_menu/Dashboard'
import EnhancedTable from './components/admin_menu/users/Users'

import * as serviceWorker from './serviceWorker';

import { BrowserRouter as Router, Route } from 'react-router-dom';

import { MuiThemeProvider, createMuiTheme } from '@material-ui/core/styles';
import grey from '@material-ui/core/colors/grey';

const theme = createMuiTheme({
    palette: {
    primary: grey,
    },
});

ReactDOM.render(
    <Router>
        <MuiThemeProvider theme={theme}>
          <Route exact path='/' component={App} />
          <Route exact path="/login" component={Login} />
          <Route exact path="/admin" component={Admin} />
          <Route exact path="/admin/users" component={EnhancedTable} />
          </MuiThemeProvider>
    </Router>,
    document.getElementById('root'))

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: http://bit.ly/CRA-PWA
serviceWorker.unregister();
