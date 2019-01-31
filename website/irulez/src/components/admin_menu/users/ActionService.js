import AuthService from '../../AuthService';

export default class ActionService {
    constructor() {
        this.Auth = new AuthService();
    }

    getData() {
        return new Promise((resolve, reject) => {
            this.Auth.fetch(window.USER_GET)
                .then(result => {
                    resolve(result.response);
                })
                .catch(err => {
                    reject(String(err).replace(/Error:/g, ''));
                });
        });
    }
    getDataWithTimeOut() {
        return new Promise((resolve, reject) => {
            setTimeout(() => {
                this.Auth.fetch(window.USER_GET)
                    .then(result => {
                        resolve(result.response);
                    })
                    .catch(err => {
                        reject(String(err).replace(/Error:/g, ''));
                    });
            }, 2000);
        });
    }
    addUser(email, password, role) {
        return new Promise((resolve, reject) => {
            var options = {
                method: 'POST',
                body: JSON.stringify({ email: email, password: password, role: role })
            };
            this.Auth.fetch(window.USER_ADD, options)
                .then(result => resolve(result.response))
                .catch(err => {
                    reject(String(err).replace(/Error:/g, ''));
                });
        });
    }
    deleteUser(selected) {
        return new Promise((resolve, reject) => {
            var options = {
                method: 'DELETE',
                body: JSON.stringify({ id: selected })
            };
            this.Auth.fetch(window.USER_DELETE, options)
                .then(result => resolve(result.response))
                .catch(err => {
                    reject(String(err).replace(/Error:/g, ''));
                });
        });
    }

    editUser(id, email, email_changed, role, role_changed, password, password_changed) {
        return new Promise((resolve, reject) => {
            if (email_changed || role_changed || password_changed) {
                var json = {};
                json.id = id;
                if (email_changed) {
                    json.email = email;
                }
                if (role_changed) {
                    json.role = role;
                }
                if (password_changed) {
                    json.password = password;
                }
                var options = {
                    method: 'PUT',
                    body: JSON.stringify(json)
                };
                this.Auth.fetch(window.USER_EDIT, options)
                    .then(result => resolve(result.response))
                    .catch(err => {
                        reject(String(err).replace(/Error:/g, ''));
                    });
            } else {
                reject('User not changed');
            }
        });
    }
}
