import decode from 'jwt-decode';
import base64 from 'react-native-base64';

export default class AuthService {
    // Initializing important variables
    constructor() {
        this.fetch = this.fetch.bind(this); // React binding stuff
        this.login = this.login.bind(this);
        this.getProfile = this.getProfile.bind(this);
    }

    login(username, password) {
        // Get a token from api server using the fetch api

        return this.fetch(window.AUTHENTICATION_SERVER, {
            method: 'POST',
            headers: { Authorization: 'Basic ' + base64.encode(username + ':' + password) }
        }).then(res => {
            this.setToken(res.token); // Setting the token in localStorage
            return Promise.resolve(res);
        });
    }

    loggedIn() {
        // Checks if there is a saved token and it's still valid
        const token = this.getToken(); // GEtting token from localstorage
        return !!token && !this.isTokenExpired(token); // handwaiving here
    }
    tokenExist() {
        const token = this.getToken(); // GEtting token from localstorage
        return !!token;
    }

    isTokenExpired(token) {
        try {
            const decoded = decode(token);
            if (decoded.exp < Date.now() / 1000) {
                // Checking if token is expired. N
                return true;
            } else {
                return false;
            }
        } catch (err) {
            return false;
        }
    }

    setToken(idToken) {
        // Saves user token to localStorage
        localStorage.setItem('id_token', idToken);
    }

    getToken() {
        // Retrieves the user token from localStorage
        return localStorage.getItem('id_token');
    }

    logout() {
        // Clear user token and profile data from localStorage
        localStorage.removeItem('id_token');
    }

    getProfile() {
        // Using jwt-decode npm package to decode the token
        return decode(this.getToken());
    }

    fetch_old(url, options) {
        // performs api calls sending the required authentication headers
        const headers = {
            Accept: 'application/json',
            'Content-Type': 'application/json'
        };

        // Setting Authorization header
        // Authorization: Bearer xxxxxxx.xxxxxxxx.xxxxxx
        if (this.loggedIn()) {
            headers['Authorization'] = 'Bearer ' + this.getToken();
        }
        return fetch(url, {
            headers,
            ...options
        })
            .then(this._checkStatus)
            .then(response => response.json());
    }

    fetch(url, options) {
        // performs api calls sending the required authentication headers
        const headers = {
            Accept: 'application/json',
            'Content-Type': 'application/json'
        };

        // Setting Authorization header
        // Authorization: Bearer xxxxxxx.xxxxxxxx.xxxxxx
        if (this.tokenExist()) {
            headers['Authorization'] = 'Bearer ' + this.getToken();
        }
        if (this.isTokenExpired(this.getToken())) {
            const decoded = decode(this.getToken());
            return fetch(window.AUTHENTICATION_SERVER_REFRESH, {
                headers,
                method: 'POST',
                body: JSON.stringify({ refreshToken: decoded.refreshToken })
            })
                .then(this._checkStatus)
                .then(response => {
                    return response.json().then(response => {
                        this.setToken(response.token);
                        headers['Authorization'] = 'Bearer ' + response.token;
                        return fetch(url, {
                            headers,
                            ...options
                        })
                            .then(this._checkStatus)
                            .then(response => response.json());
                    });
                });
        } else {
            return fetch(url, {
                headers,
                ...options
            })
                .then(this._checkStatus)
                .then(response => response.json());
        }
    }

    refreshToken() {
        const decoded = decode(this.getToken());
        const headers = {
            Accept: 'application/json',
            'Content-Type': 'application/json',
            Authorization: 'Bearer ' + this.getToken()
        };
        return fetch(window.AUTHENTICATION_SERVER_REFRESH, {
            headers,
            method: 'POST',
            body: JSON.stringify({ refreshToken: decoded.refreshToken })
        })
            .then(this._checkStatus)
            .then(response => {
                return response.json().then(response => {
                    this.setToken(response.token);
                    return Promise.resolve(response);
                });
            });
    }

    _checkStatus(response) {
        console.log(response);
        // raises an error in case response status is not a success
        if (response.status >= 200 && response.status < 300) {
            // Success status lies between 200 to 300
            return response;
        } else {
            var error = new Error(response.statusText);
            error.response = response;
            throw error;
        }
    }
}
