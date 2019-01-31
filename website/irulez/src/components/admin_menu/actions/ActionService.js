import AuthService from '../../AuthService';

export default class ActionService {
    constructor() {
        this.Auth = new AuthService();
    }

    getData() {
        return new Promise((resolve, reject) => {
            this.Auth.fetch(window.ACTIONS_GET)
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
                this.Auth.fetch(window.ACTIONS_GET)
                    .then(result => {
                        resolve(result.response);
                    })
                    .catch(err => {
                        reject(String(err).replace(/Error:/g, ''));
                    });
            }, 2000);
        });
    }
    addAction(name, action_type, trigger, timer, delay, master, condition, click_number, outputs_id, notifications_id) {
        return new Promise((resolve, reject) => {
            var options = {
                method: 'POST',
                body: JSON.stringify({
                    name: name,
                    action_type: action_type,
                    trigger: trigger,
                    timer: timer,
                    delay: delay,
                    master: master,
                    condition: condition,
                    click_number: click_number,
                    outputs_id: outputs_id,
                    notifications_id: notifications_id
                })
            };
            this.Auth.fetch(window.ACTION_ADD, options)
                .then(result => resolve(result.response))
                .catch(err => {
                    reject(String(err).replace(/Error:/g, ''));
                });
        });
    }
    deleteAction(selected) {
        return new Promise((resolve, reject) => {
            var options = {
                method: 'DELETE',
                body: JSON.stringify({ id: selected })
            };
            this.Auth.fetch(window.ACTION_DELETE, options)
                .then(result => resolve(result.response))
                .catch(err => {
                    reject(String(err).replace(/Error:/g, ''));
                });
        });
    }
    editAction(state, fields) {
        var json = {};
        json.id = state.lastSelectedRow.id;

        fields
            .filter(field => {
                return field.editForm;
            })
            .map(field => {
                let changed = field.id + '_changed';
                if (state[changed]) {
                    json[field.id] = state[field.id];
                }
                return json;
            });
        return new Promise((resolve, reject) => {
            if (Object.keys(json).length > 1) {
                console.log(json);
                var options = {
                    method: 'PUT',
                    body: JSON.stringify(json)
                };
                this.Auth.fetch(window.ACTION_EDIT, options)
                    .then(result => resolve(result.response))
                    .catch(err => {
                        reject(String(err).replace(/Error:/g, ''));
                    });
            } else {
                reject('Action not changed');
            }
        });
    }
}
