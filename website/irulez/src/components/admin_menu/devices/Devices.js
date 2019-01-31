import React, { Component } from 'react';
import DialogMenu from '../DialogMenu';
import EnhancedTable from '../Table';
import PropTypes from 'prop-types';
import { withSnackbar } from 'notistack';
import AuthService from '../../AuthService';
import { withStyles } from '@material-ui/core/styles';
import { components } from '../fields/iRulezFields';
import LoadingOverlay from 'react-loading-overlay';
import CircleLoader from 'react-spinners/CircleLoader';
import ActionService from './ActionService';

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
    Action = new ActionService();
    originalValueRow = [];

    constructor(props) {
        super(props);
        this.props.Collapse('users');
    }

    state = {
        newForm: false,
        editForm: false,
        deleteForm: false,
        data: [],
        selected: [],
        lastSelectedRow: [],
        isActive: true,
        rowsPerPage: 5
    };

    componentDidMount() {
        this.getData();
        this.resetValues();
    }
    updateRowsPerPage = rows => {
        this.setState({
            rowsPerPage: rows
        });
    };

    resetValues = () => {
        this.fields
            .filter(field => {
                return field.addForm;
            })
            .map(field => {
                let changed = field.id + '_changed';
                let error = field.id + '_error';

                return this.setState({
                    [field.id]: '',
                    [changed]: '',
                    [error]: ''
                });
            });
    };

    handleFormOpen = form => {
        this.setState({
            [form]: true
        });
        if (form === 'editForm') {
            this.fields
                .filter(field => {
                    return field.editForm;
                })
                .map(field => {
                    return this.setState({
                        [field.id]: this.state.lastSelectedRow[field.mapping]
                    });
                });
        }
    };

    handleFormClose = form => {
        this.setState({
            [form]: false
        });
        this.resetValues();
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

    handleChange = (name, value, fieldError) => {
        let changed = name + '_changed';
        let error = name + '_error';

        this.setState({
            [name]: value,
            [changed]: true,
            [error]: fieldError
        });
        if (value === this.state.lastSelectedRow[name]) {
            this.setState({
                [changed]: false
            });
        }
    };

    getData = () => {
        this.setState({ isActive: true });
        this.Action.getDataWithTimeOut()
            .then(response => {
                this.setState({ data: response });
                this.setState({ selected: [] });
                this.setState({ isActive: false });
            })
            .catch(err => console.log(err));
    };

    add = () => {
        this.Action.addDevice(this.state.name, this.state.mac, this.state.sn)
            .then(() => {
                this.handleFormClose('newForm');
                this.handleNotification('Device has been added', 'success');
                this.getData();
            })
            .catch(err => console.log(err));
    };

    delete = () => {
        this.Action.deleteDevice(this.state.selected)
            .then(() => {
                this.handleFormClose('deleteForm');
                this.handleNotification('Device has been deleted', 'warning');
                this.getData();
            })
            .catch(err => console.log(err));
    };

    edit = () => {
        this.Action.editDevice(
            this.state.lastSelectedRow.id,
            this.state.mac,
            this.state.mac_changed,
            this.state.sn,
            this.state.sn_changed
        )
            .then(() => {
                this.handleFormClose('editForm');
                this.handleNotification('Device has been changed', 'info');
                this.getData();
            })
            .catch(err => console.log(err));
    };

    fields = [
        { id: 'id', align: 'left', disablePadding: true, label: 'ID' },
        {
            id: 'name',
            mapping: 'name',
            align: 'left',
            disablePadding: true,
            label: 'Name',
            addForm: true,
            required: true,
            add_autoFocus: true
        },
        {
            id: 'mac',
            mapping: 'mac',
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
            mapping: 'sn',
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

    render() {
        const { classes } = this.props;
        const fields = this.fields;
        return (
            <LoadingOverlay
                active={this.state.isActive}
                spinner={<CircleLoader size={150} color={'yellow'} />}
                text='Loading your content...'
            >
                <EnhancedTable
                    data={this.state.data}
                    fields={fields}
                    selected={this.state.selected}
                    handleFormOpen={this.handleFormOpen}
                    handleDelete={this.handleFormOpen}
                    updatedSelected={this.updatedSelected}
                    title='Action'
                    addIconTooltip='Add action'
                    editIconTooltip='Edit action'
                    deleteIconTooltip='Delete action'
                    rowsPerPage={this.state.rowsPerPage}
                />
                <DialogMenu
                    open={this.state.newForm}
                    handleFormAccept={this.add}
                    handleFormCancel={() => this.handleFormClose('newForm')}
                    title='New Action'
                    acceptLabel='New'
                >
                    {fields
                        .filter(form => {
                            return form.addForm;
                        })
                        .map(field => {
                            const Component = field.Component ? components[field.Component] : components['default'];
                            return (
                                <Component
                                    key={field.id}
                                    classes={classes}
                                    field={field}
                                    handleChange={this.handleChange}
                                    value={this.state[field.id]}
                                    autoFocus={field.autoFocus}
                                    dependency={this.state[field.dependency]}
                                />
                            );
                        })}
                </DialogMenu>

                <DialogMenu
                    open={this.state.editForm}
                    handleFormAccept={this.edit}
                    handleFormCancel={() => this.handleFormClose('editForm')}
                    title='Edit Device'
                    acceptLabel='Edit'
                >
                    {fields
                        .filter(form => {
                            return form.editForm;
                        })
                        .map(field => {
                            const Component = field.Component ? components[field.Component] : components['default'];
                            return (
                                <Component
                                    key={field.id}
                                    classes={classes}
                                    field={field}
                                    handleChange={this.handleChange}
                                    value={this.state[field.id]}
                                    autoFocus={field.autoFocus}
                                    dependency={this.state[field.dependency]}
                                />
                            );
                        })}
                </DialogMenu>
                <DialogMenu
                    open={this.state.deleteForm}
                    handleFormAccept={this.delete}
                    handleFormCancel={() => this.handleFormClose('deleteForm')}
                    title='Delete Device'
                    acceptLabel='Delete'
                >
                    Are you sure you want to delete device {JSON.stringify(this.state.selected)}
                </DialogMenu>
            </LoadingOverlay>
        );
    }
}
Devices.propTypes = {
    enqueueSnackbar: PropTypes.func.isRequired
};

export default withStyles(styles)(withSnackbar(Devices));
