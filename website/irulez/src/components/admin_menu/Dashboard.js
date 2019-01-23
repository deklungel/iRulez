import React, { Component } from 'react';
import './Dashboard.css';

class Admin extends Component {
    constructor(props) {
        super(props);
        this.props.Collapse('dashboard');
    }

    render() {
        return (
            <div className='Admin'>
                <div className='App-header'>
                    <h2>Welcome Admin</h2>
                </div>
            </div>
        );
    }
}

export default Admin;
