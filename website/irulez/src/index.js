import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';

import App from './App';
import Login from './components/Login';
import Administrator from './components/admin_menu/Administrator';

import * as serviceWorker from './serviceWorker';

import { BrowserRouter as Router, Route } from 'react-router-dom';

import { MuiThemeProvider, createMuiTheme } from '@material-ui/core/styles';
import grey from '@material-ui/core/colors/grey';

const theme = createMuiTheme({
    palette: {
        primary: grey
    },
    typography: {
        useNextVariants: true
    }
});

ReactDOM.render(
    // <Router history={history}>
    <Router>
        <MuiThemeProvider theme={theme}>
            <Route exact path='/' component={App} />
            <Route exact path='/login' component={Login} />
            <Route path='/administrator' component={Administrator} />
        </MuiThemeProvider>
    </Router>,
    document.getElementById('root')
);

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: http://bit.ly/CRA-PWA
serviceWorker.unregister();
