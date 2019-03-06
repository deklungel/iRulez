import AuthService from '../../AuthService';

export default class ProcessService {
    constructor() {
        this.Auth = new AuthService();
    }

    getData() {
        return new Promise((resolve, reject) => {
            this.Auth.fetch(window.PROCESSES_GET)
                .then(result => {
                    resolve(result.response);
                })
                .catch(err => {
                    reject(String(err).replace(/Error:/g, ''));
                });
        });
    }
    restartProcess(name) {
        return new Promise((resolve, reject) => {
            var options = {
                method: 'POST',
                body: JSON.stringify({ process: name })
            };
            this.Auth.fetch(window.PROCESSES_RESTART, options)
                .then(result => {
                    resolve(result.response);
                })
                .catch(err => {
                    reject(String(err).replace(/Error:/g, ''));
                });
        });
    }
    startProcess(name) {
        return new Promise((resolve, reject) => {
            var options = {
                method: 'POST',
                body: JSON.stringify({ process: name })
            };
            this.Auth.fetch(window.PROCESSES_START, options)
                .then(result => {
                    resolve(result.response);
                })
                .catch(err => {
                    reject(String(err).replace(/Error:/g, ''));
                });
        });
    }
    stopProcess(name) {
        return new Promise((resolve, reject) => {
            var options = {
                method: 'POST',
                body: JSON.stringify({ process: name })
            };
            this.Auth.fetch(window.PROCESSES_STOP, options)
                .then(result => {
                    resolve(result.response);
                })
                .catch(err => {
                    reject(String(err).replace(/Error:/g, ''));
                });
        });
    }
    clearLog(name) {
        return new Promise((resolve, reject) => {
            var options = {
                method: 'POST',
                body: JSON.stringify({ process: name })
            };
            this.Auth.fetch(window.CLEAR_LOG, options)
                .then(result => {
                    resolve(result.response);
                })
                .catch(err => {
                    reject(String(err).replace(/Error:/g, ''));
                });
        });
    }
}
