import AuthService from '../../AuthService';

export default class ActionService {
    constructor() {
        this.Auth = new AuthService();
    }

    getData() {
        return new Promise((resolve, reject) => {
            this.Auth.fetch(window.DEVICE_GET)
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
                this.Auth.fetch(window.DEVICE_GET)
                    .then(result => {
                        resolve(result.response);
                    })
                    .catch(err => {
                        reject(String(err).replace(/Error:/g, ''));
                    });
            }, 2000);
        });
    }
    addDevice(name, mac, sn) {
        return new Promise((resolve, reject) => {
            var options = {
                method: 'POST',
                body: JSON.stringify({ name: name, mac: mac, sn: sn })
            };
            this.Auth.fetch(window.DEVICE_ADD, options)
                .then(result => resolve(result.response))
                .catch(err => {
                    reject(String(err).replace(/Error:/g, ''));
                });
        });
    }
    deleteDevice(selected) {
        return new Promise((resolve, reject) => {
            var options = {
                method: 'DELETE',
                body: JSON.stringify({ id: selected })
            };
            this.Auth.fetch(window.DEVICE_DELETE, options)
                .then(result => resolve(result.response))
                .catch(err => {
                    reject(String(err).replace(/Error:/g, ''));
                });
        });
    }

    editDevice(id, mac, mac_changed, sn, sn_changed) {
        return new Promise((resolve, reject) => {
            if (mac_changed || sn_changed) {
                var json = {};
                json.id = id;
                if (mac_changed) {
                    json.mac = mac;
                }
                if (sn_changed) {
                    json.sn = sn;
                }
                var options = {
                    method: 'PUT',
                    body: JSON.stringify(json)
                };
                this.Auth.fetch(window.DEVICE_EDIT, options)
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
