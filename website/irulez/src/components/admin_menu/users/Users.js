import React, { Component } from 'react';
import DialogMenu from '../DialogMenu';
import EnhancedTable from '../Table';
import PropTypes from 'prop-types';
import { withSnackbar } from 'notistack';
import AuthService from '../../AuthService';
import ActionService from './ActionService';
import LoadingOverlay from 'react-loading-overlay';
import CircleLoader from 'react-spinners/CircleLoader';

import { components } from '../fields/iRulezFields';

class Users extends Component {
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
        this.Action.addUser(this.state.email, this.state.password, this.state.role)
            .then(() => {
                this.handleFormClose('newForm');
                this.handleNotification('User has been added', 'success');
                this.getData();
            })
            .catch(err => console.log(err));
    };

    delete = () => {
        this.Action.deleteUser(this.state.selected)
            .then(() => {
                this.handleFormClose('deleteForm');
                this.handleNotification('User has been deleted', 'warning');
                this.getData();
            })
            .catch(err => console.log(err));
    };

    edit = () => {
        this.Action.editUser(
            this.state.lastSelectedRow.id,
            this.state.email,
            this.state.email_changed,
            this.state.role,
            this.state.role_changed,
            this.state.password,
            this.state.password_changed
        )
            .then(() => {
                this.handleFormClose('editForm');
                this.handleNotification('User has been changed', 'info');
                this.getData();
            })
            .catch(err => console.log(err));
    };
    fields = [
        {
            id: 'email',
            mapping: 'email',
            addForm: true,
            editForm: true,
            align: 'left',
            disablePadding: false,
            label: 'Username',
            Component: 'MailField'
        },
        {
            id: 'password',
            mapping: 'password',
            addForm: true,
            editForm: true,
            align: 'left',
            disablePadding: false,
            label: 'Password',
            Component: 'PasswordField',
            hideInTable: true
        },
        {
            id: 'role',
            mapping: 'role',
            addForm: true,
            editForm: true,
            align: 'left',
            disablePadding: false,
            label: 'Role',
            Component: 'SelectionField',
            options: [
                {
                    id: 'user',
                    value: 'user',
                    label: 'User'
                },
                {
                    id: 'admin',
                    value: 'admin',
                    label: 'Administrator'
                }
            ]
        }
    ];

    render() {
        const fields = this.fields;
        const { classes } = this.props;

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
                    title='Users'
                    addIconTooltip='Add user'
                    editIconTooltip='Edit user'
                    deleteIconTooltip='Delete user'
                    rowsPerPage={this.state.rowsPerPage}
                />
                <DialogMenu
                    open={this.state.newForm}
                    handleFormAccept={this.add}
                    handleFormCancel={() => this.handleFormClose('newForm')}
                    title='New User'
                    acceptLabel='Add'
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
                                    options={field.options}
                                />
                            );
                        })}
                </DialogMenu>

                <DialogMenu
                    open={this.state.editForm}
                    handleFormAccept={this.edit}
                    handleFormCancel={() => this.handleFormClose('editForm')}
                    title='Edit User'
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
                                    options={field.options}
                                />
                            );
                        })}
                </DialogMenu>
                <DialogMenu
                    open={this.state.deleteForm}
                    handleFormAccept={this.delete}
                    handleFormCancel={() => this.handleFormClose('deleteForm')}
                    title='Delete User'
                    acceptLabel='Delete'
                >
                    Are you sure you want to delete user {JSON.stringify(this.state.selected)}
                </DialogMenu>
            </LoadingOverlay>
        );
    }
}
Users.propTypes = {
    enqueueSnackbar: PropTypes.func.isRequired
};

export default withSnackbar(Users);
