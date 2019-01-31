import AuthService from '../AuthService';

export default class ValueService {
    constructor() {
        this.Auth = new AuthService();
    }

    Get_Trigger_Field() {
        return new Promise((resolve, reject) => {
            this.Auth.fetch(window.GET_FIELD_TRIGGERS)
                .then(result => {
                    resolve(result.response);
                })
                .catch(err => {
                    reject(err);
                });
        });
    }

    Get_Action_Type_Field() {
        return new Promise((resolve, reject) => {
            this.Auth.fetch(window.GET_FIELD_ACTION_TYPES)
                .then(result => {
                    resolve(result.response);
                })
                .catch(err => {
                    reject(err);
                });
        });
    }
    Get_Outputs() {
        return new Promise((resolve, reject) => {
            this.Auth.fetch(window.GET_OUTPUTS)
                .then(result => {
                    resolve(result.response);
                })
                .catch(err => {
                    reject(err);
                });
        });
    }
    Get_Conditions() {
        return new Promise((resolve, reject) => {
            this.Auth.fetch(window.GET_CONDITIONS)
                .then(result => {
                    resolve(result.response);
                })
                .catch(err => {
                    reject(err);
                });
        });
    }
    Get_Notifications() {
        return new Promise((resolve, reject) => {
            this.Auth.fetch(window.GET_NOTIFICATIONS)
                .then(result => {
                    resolve(result.response);
                })
                .catch(err => {
                    reject(err);
                });
        });
    }
}
