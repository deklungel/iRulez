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
        console.log(action_type);
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
    editAction2(state, fields) {
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
            });
        console.log(json);
    }

    editAction(
        id,
        name,
        name_changed,
        action_type_name,
        action_type_name_changed,
        trigger_name,
        trigger_name_changed,
        timer,
        timer_changed,
        delay,
        delay_changed,
        master,
        master_changed,
        condition,
        condition_changed,
        click_number,
        click_number_changed,
        outputs_id,
        outputs_id_changed,
        notifications_id,
        notifications_id_changed
    ) {
        return new Promise((resolve, reject) => {
            if (
                name_changed ||
                action_type_name_changed ||
                trigger_name_changed ||
                timer_changed ||
                delay_changed ||
                master_changed ||
                condition_changed ||
                click_number_changed ||
                outputs_id_changed ||
                notifications_id_changed
            ) {
                var json = {};
                json.id = id;
                if (name_changed) {
                    json.name = name;
                }
                if (action_type_name_changed) {
                    json.action_type_name = action_type_name;
                }
                if (trigger_name_changed) {
                    json.trigger_name = trigger_name;
                }
                if (timer_changed) {
                    json.timer = timer;
                }
                if (delay_changed) {
                    json.delay = delay;
                }
                if (master_changed) {
                    json.master = master;
                }
                if (condition_changed) {
                    json.condition = condition;
                }
                if (click_number_changed) {
                    json.click_number = click_number;
                }
                if (outputs_id_changed) {
                    json.outputs_id = outputs_id;
                }
                if (notifications_id_changed) {
                    json.notifications_id = notifications_id;
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
