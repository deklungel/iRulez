import React, { Component } from 'react';
import AuthService from './AuthService';

export default function withAuth(AuthComponent) {
    const Auth = new AuthService();
    return class AuthWrapped extends Component {
        constructor() {
            super();
            this.state = {
                user: null
            };
        }

        componentWillMount() {
            try {
                if (Auth.tokenExist && !Auth.loggedIn()) {
                    Auth.refreshToken()
                        .then(res => {
                            try {
                                const profile = Auth.getProfile();
                                this.setState({
                                    user: profile
                                });
                            } catch (err) {
                                Auth.logout();
                                this.props.history.replace('/login');
                            }
                        })
                        .catch(error => {
                            Auth.logout();
                            this.props.history.replace('/login');
                        });
                } else {
                    if (!Auth.loggedIn()) {
                        this.props.history.replace('/login');
                    } else {
                        try {
                            const profile = Auth.getProfile();
                            this.setState({
                                user: profile
                            });
                        } catch (err) {
                            Auth.logout();
                            this.props.history.replace('/login');
                        }
                    }
                }
            } catch (err) {
                console.log('Erorr 2');
                Auth.logout();
                this.props.history.replace('/login');
            }
        }
        render() {
            if (this.state.user) {
                return <AuthComponent {...this.props} />;
            } else {
                return null;
            }
        }
    };
}
