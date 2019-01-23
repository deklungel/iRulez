import React, { Component } from 'react';
import DialogMenu from '../DialogMenu';
import EnhancedTable from '../Table';
import PropTypes from 'prop-types';
import { withSnackbar } from 'notistack';
import AuthService from '../../AuthService';
import TextField from '@material-ui/core/TextField';
import classNames from 'classnames';
import { withStyles } from '@material-ui/core/styles';

const styles = theme => ({
    textField: {
        marginLeft: theme.spacing.unit,
        marginRight: theme.spacing.unit
    },
    content: {
        overflowY: 'visible'
    }
});

class Devices extends Component {
    Auth = new AuthService();
    originalValueRow = [];

    constructor(props) {
        super(props);
        this.props.Collapse('devices');
    }

    state = {
        newForm: false,
        editForm: false,
        deleteForm: false,
        data: [],
        selected: [],
        lastSelectedRow: [],
        originalValueRow: []
    };

    getDataFromBackend = () => {
        this.Auth.fetch(window.DEVICE_GET).then(
            function (result) {
                this.setState({ data: result.response })
            }.bind(this)
        ).catch(err => {
            alert(err);
        })
        this.setState({ selected: [] });
    }

    getDataFromBackend = () => {
        this.Auth.fetch(window.DEVICE_GET)
            .then(
                function (result) {
                    this.setState({ data: result.response });
                }.bind(this)
            )
            .catch(err => {
                alert(err);
            });
        this.setState({ selected: [] });
    };

    handleFormOpen = form => {
        this.setState({
            [form]: true
        });
        if (form === 'editForm') {
            this.setState({
                name: this.state.lastSelectedRow.name,
                mac: this.state.lastSelectedRow.mac,
                sn: this.state.lastSelectedRow.sn
            });
        }
    };

    handleFormClose = form => {
        this.setState({
            [form]: false
        });
        this.resetValues();
    };

    resetValues = () => {
        this.setState({
            name: '',
            mac: '',
            sn: '',
            name_changed: false,
            sn_changed: false,
            mac_changed: false,
            name_error: false,
            mac_error: false
        });
    };

    updatedSelected = (value, row) => {
        this.setState({ selected: value });
        if (value.length === 1) {
            this.setState({
                lastSelectedRow: row[value]
            });
        }
    };

    handleNotification = (message, variant) => {
        // variant could be success, error, warning or info
        this.props.enqueueSnackbar(message, { variant });
    };

    handleChange = name => event => {
        let changed = name + '_changed';
        let error = name + '_error';
        this.setState({
            [name]: event.target.value,
            [changed]: true,
            [error]: false
        });
        if (event.target.value === this.state.lastSelectedRow[name]) {
            this.setState({
                [changed]: false
            });
        }
    };

    add = () => {
        if (this.validateInput()) {
            var options = {
                method: 'POST',
                body: JSON.stringify({ name: this.state.name, mac: this.state.mac, sn: this.state.sn })
            };
            this.handleFormClose('newForm');
            this.Auth.fetch(window.DEVICE_ADD, options)
                .then(
                    function (result) {
                        this.getDataFromBackend();
                        this.handleNotification('Device has been added', 'success');
                    }.bind(this)
                )
                .catch(err => {
                    var error = String(err).replace(/Error:/g, '');
                    this.handleNotification(String(error), 'error');
                });
        }
    };

    delete = () => {
        var options = {
            method: 'DELETE',
            body: JSON.stringify({ id: this.state.selected })
        };
        this.Auth.fetch(window.DEVICE_DELETE, options)
            .then(
                function (result) {
                    this.getDataFromBackend();
                    this.handleNotification('Device has been deleted', 'warning');
                    this.handleFormClose('deleteForm');
                }.bind(this)
            )
            .catch(err => {
                alert(err);
            });
    };

    edit = () => {
        if (this.validateInput()) {
            if (this.state.name_changed || this.state.mac_changed || this.state.sn_changed) {
                var json = {};
                json.id = this.state.lastSelectedRow.id;
                if (this.state.name_changed) {
                    json.name = this.state.name;
                }
                if (this.state.mac_changed) {
                    json.mac = this.state.mac;
                }
                if (this.state.sn_changed) {
                    json.sn = this.state.sn;
                }
                console.log(json);
                var options = {
                    method: 'PUT',
                    body: JSON.stringify(json)
                };
                this.Auth.fetch(window.DEVICE_EDIT, options).then(
                    function (result) {
                        this.handleFormClose('editForm');
                        this.getDataFromBackend();
                        this.handleNotification('Device has been changed', 'info');
                    }.bind(this)
                );
            } else {
                this.handleFormClose('editForm');
            }
        }
    };

    validateInput() {
        if (this.state.mac !== '' && this.state.name !== '') {
            console.log(this.state.mac);
            console.log(this.state.name);
            return true;
        }
        if (this.state.name === '') {
            this.setState({ name_error: true });
        }
        if (this.state.mac === '') {
            this.setState({ mac_error: true });
        }
    }

    render() {
        const { classes } = this.props;

        const fields = [
            { id: 'id', align: 'left', disablePadding: true, label: 'ID' },
            {
                id: 'name',
                align: 'left',
                disablePadding: true,
                label: 'Name',
                addForm: true,
                required: true,
                add_autoFocus: true
            },
            {
                id: 'mac',
                align: 'left',
                disablePadding: false,
                label: 'MAC',
                addForm: true,
                editForm: true,
                required: true,
                edit_autofocus: true
            },
            {
                id: 'sn',
                align: 'left',
                disablePadding: false,
                label: 'Serial Number',
                addForm: true,
                editForm: true,
                required: false
            },
            { id: 'version', align: 'left', disablePadding: false, label: 'Version' },
            { id: 'ping', align: 'left', disablePadding: false, label: 'PING', type: 'ErrorCheck' },
            { id: 'mqtt', align: 'left', disablePadding: false, label: 'MQTT', type: 'ErrorCheck' }
        ];

        return (
            <div>
                <EnhancedTable
                    data={this.state.data}
                    fields={fields}
                    selected={this.state.selected}
                    handleFormOpen={this.handleFormOpen}
                    handleDelete={this.handleFormOpen}
                    updatedSelected={this.updatedSelected}
                    title='Devices'
                    addIconTooltip='Add device'
                    editIconTooltip='Edit device'
                    deleteIconTooltip='Delete device'
                    rowsPerPage={5}
                />
                <DialogMenu
                    open={this.state.newForm}
                    handleFormAccept={this.add}
                    handleFormCancel={() => this.handleFormClose('newForm')}
                    title='New Device'
                    acceptLabel='New'
                >
                    {fields
                        .filter(form => {
                            return form.addForm;
                        })
                        .map(field => {
                            return (
                                <TextField
                                    key={field.id}
                                    error={this.state[field.id + '_error']}
                                    required={field.required}
                                    autoFocus={field.add_autoFocus}
                                    className={classNames(classes.margin, classes.textField)}
                                    id='name'
                                    value={this.state[field.id]}
                                    onChange={this.handleChange(field.id)}
                                    label={field.label}
                                    type='string'
                                    fullWidth
                                />
                            );
                        })}
                </DialogMenu>
            </div>
        )
    }
}
Devices.propTypes = {
    enqueueSnackbar: PropTypes.func.isRequired
};

export default withStyles(styles)(withSnackbar(Devices));
