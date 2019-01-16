import React, { Component } from 'react';
import './Dashboard.css';

import SideBar from '../SideBar';


import AuthService from '../AuthService';
import withAuth from '../withAuth';

const Auth = new AuthService();

class Admin extends Component {
    constructor(props) {
        super(props);
        this.handleLogout = this.handleLogout.bind(this);
    }
    componentWillMount() {
        if (this.props.user.role !== "admin") {
            this.props.history.replace('/');
        }
    }
    handleLogout() {
        Auth.logout()
        this.props.history.replace('/login');
    }

    render() {
        return (
            <SideBar Auth={this.props.Auth} >
                <div className="Admin">
                    <div className="App-header">
                        <h2>Welcome Admin {this.props.user.username}</h2>
                        {/* <Users></Users> */}
                    </div>
                </div>
            </SideBar>
        )
            ;
    }
}

export default withAuth(Admin);
