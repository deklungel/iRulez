import AuthService from '../AuthService';

export default class LogService {
    constructor() {
        this.Auth = new AuthService();
    }

    getData(name) {
        console.log('getDAta');
        return new Promise((resolve, reject) => {
            var options = {
                method: 'POST',
                body: JSON.stringify({ process: name })
            };
            this.Auth.fetch(window.PROCESSES_GET_LOG, options)
                .then(result => {
                    resolve(result.response);
                })
                .catch(err => {
                    reject(String(err).replace(/Error:/g, ''));
                });
        });
    }
}
