import React, { Component } from 'react';
import AuthService from '../AuthService';
import withAuth from './../withAuth';
import qs from 'query-string';
import LogService from './LogService';

const Auth = new AuthService();

const divStyle = {
    whiteSpace: 'pre-line'
};

class Logging extends Component {
    user = Auth.getProfile();
    LogService = new LogService();

    state = {
        data: '',
        processName: '',
        tail: 1000
    };

    componentWillMount() {
        if (this.user.role === 'user') {
            this.props.history.replace('/');
        }
    }
    componentDidMount() {
        const obj = qs.parse(this.props.location.search);
        this.setState({ processName: obj.process });
        console.log(obj.process);
        console.log(this.state.processName);
        this.getData(obj.process);
    }

    getData = processName => {
        this.LogService.getData(processName).then(response => {
            this.setState({ data: response });
        });
    };

    render() {
        return <div style={divStyle}>{this.state.data}</div>;
    }
}

export default withAuth(Logging);
