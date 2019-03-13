import React, { Component } from 'react';
import DialogMenu from '../DialogMenu';
import EnhancedTable from '../Table';
import PropTypes from 'prop-types';
import { withSnackbar } from 'notistack';
import AuthService from '../../AuthService';
import UserService from './UserService';
import LoadingOverlay from 'react-loading-overlay';
import CircleLoader from 'react-spinners/CircleLoader';
import PasswordField from '../fields/PasswordField';
import { components } from '../fields/iRulezFields';

class Users extends Component {
    Auth = new AuthService();
    Service = new UserService();
    originalValueRow = [];

    constructor(props) {
        super(props);
        this.props.Collapse('user');
    }

    state = {
        newForm: false,
        editForm: false,
        deleteForm: false,
        changePasswordForm: false,
        data: [],
        selected: [],
        lastSelectedRow: [],
        isActive: true,
        rowsPerPage: 5,
        submitDisabled: false
    };

    componentDidMount() {
        this.getData();
        this.props.checkSidebarState();
        this.resetValues();
    }
    updateRowsPerPage = rows => {
        this.setState({
            rowsPerPage: rows
        });
    };

    resetValues = () => {
        this.fields
            // .filter(field => {
            //     return field.editForm;
            // })
            .map(field => {
                let changed = field.id + '_changed';
                return this.setState({
                    [field.id]: field.array ? [] : field.default ? field.default : '',
                    [changed]: ''
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
                    return field.editForm || field.forLabel;
                })
                .map(field => {
                    if (field.array) {
                        if (this.state.lastSelectedRow[field.id]) {
                            if (!Array.isArray(this.state.lastSelectedRow[field.id])) {
                                var row = this.state.lastSelectedRow;
                                var tmp = this.state.lastSelectedRow[field.id].split(',').map(value => {
                                    return parseInt(value);
                                });
                                row[field.id] = tmp;

                                this.setState({
                                    lastSelectedRow: row
                                });
                            }
                            return this.setState({
                                [field.id]: this.state.lastSelectedRow[field.id]
                            });
                        } else {
                            return this.setState({
                                [field.id]: []
                            });
                        }
                    } else {
                        return this.setState({
                            [field.id]:
                                this.state.lastSelectedRow[field.id] === null
                                    ? ''
                                    : this.state.lastSelectedRow[field.id]
                        });
                    }
                });
        }
    };

    handleFormClose = form => {
        this.setState({
            [form]: false,
            submitDisabled: false
        });
        this.resetValues();
    };
    handleChangePasswordFormClose = form => {
        this.setState({
            changePasswordForm: false,
            submitDisabled: false,
            password: ''
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

    handleChange = (name, value) => {
        let changed = name + '_changed';
        this.setState({
            [name]: value,
            [changed]: true
        });

        if (value.toString() === String(this.state.lastSelectedRow[name])) {
            this.setState({
                [changed]: false
            });
        }
    };

    getData = () => {
        this.setState({ isActive: true });
        this.Service.getData()
            .then(response => {
                this.setState({ data: response });
                this.setState({ selected: [] });
                this.setState({ isActive: false });
            })
            .catch(err => {
                console.log(err);
                this.handleNotification(String(err), 'error');
            });
    };

    add = () => {
        this.setState({ submitDisabled: true });
        this.Service.add(this.state, this.fields)
            .then(() => {
                this.handleFormClose('newForm');
                this.handleNotification('User has been added', 'success');
                this.getData();
            })
            .catch(err => {
                console.log(err);
                this.handleNotification(String(err), 'error');
                this.setState({ submitDisabled: false });
            });
    };

    delete = () => {
        this.setState({ submitDisabled: true });
        this.Service.delete(this.state.selected)
            .then(() => {
                this.handleFormClose('deleteForm');
                this.handleNotification('User has been deleted', 'warning');
                this.getData();
            })
            .catch(err => {
                console.log(err);
                this.handleNotification(String(err), 'error');
                this.setState({ submitDisabled: false });
            });
    };

    edit = () => {
        this.setState({ submitDisabled: true });
        this.Service.edit(this.state, this.fields)
            .then(msg => {
                this.handleFormClose('editForm');
                this.handleNotification(msg, 'info');
                if (msg !== 'No value changed') {
                    this.getData();
                }
            })
            .catch(err => {
                console.log(err);
                this.handleNotification(String(err), 'error');
                this.setState({ submitDisabled: false });
            });
    };
    changePassword = () => {
        this.setState({ submitDisabled: true });
        this.Service.changePassword(this.state, this.fields)
            .then(() => {
                this.handleChangePasswordFormClose();
                this.handleNotification('Password has been changed', 'info');
                this.getData();
            })
            .catch(err => {
                console.log(err);
                this.handleNotification(String(err), 'error');
                this.setState({ submitDisabled: false });
            });
    };

    fields = [
        {
            id: 'email',
            addForm: true,
            editForm: true,
            align: 'left',
            required: true,
            disablePadding: false,
            label: 'Email',
            Component: 'MailField'
        },
        {
            id: 'password',
            addForm: true,
            editForm: false,
            align: 'left',
            required: true,
            disablePadding: false,
            label: 'Password',
            Component: 'PasswordField',
            hideInTable: true
        },
        {
            id: 'group_name',
            label: 'Group'
        },
        {
            id: 'group_id',
            align: 'left',
            disablePadding: true,
            label: 'Group',
            Component: 'GroupField',
            required: true,
            addForm: true,
            editForm: true,
            autoFocus: false,
            hideInTable: true,
            default: '0'
        },
        {
            id: 'role',
            addForm: true,
            editForm: false,
            required: true,
            align: 'left',
            disablePadding: false,
            label: 'Role',
            Component: 'SelectionField',
            default: 'user',
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
                    updateRowsPerPage={this.updateRowsPerPage}
                    title='Users'
                    addIconTooltip='Add user'
                    editIconTooltip='Edit user'
                    deleteIconTooltip='Delete user'
                    rowsPerPage={this.state.rowsPerPage}
                />
                <DialogMenu
                    open={this.state.newForm}
                    submitDisabled={this.state.submitDisabled}
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
                    submitDisabled={this.state.submitDisabled}
                    handleFormAccept={this.edit}
                    handleFormCancel={() => this.handleFormClose('editForm')}
                    title={'Edit ' + this.state.lastSelectedRow.role}
                    acceptLabel='Edit'
                    extraButton='Change Password'
                    extraButtonAction={() => this.handleFormOpen('changePasswordForm')}
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
                    submitDisabled={this.state.submitDisabled}
                    handleFormAccept={this.delete}
                    handleFormCancel={() => this.handleFormClose('deleteForm')}
                    title='Delete User'
                    acceptLabel='Delete'
                >
                    Are you sure you want to delete user {JSON.stringify(this.state.selected)}
                </DialogMenu>
                <DialogMenu
                    open={this.state.changePasswordForm}
                    submitDisabled={this.state.submitDisabled}
                    handleFormAccept={this.changePassword}
                    handleFormCancel={() => this.handleChangePasswordFormClose()}
                    title='Change Password'
                    acceptLabel='Change'
                >
                    <PasswordField
                        key={'password'}
                        classes={classes}
                        field={{
                            id: 'password',
                            addForm: true,
                            editForm: true,
                            align: 'left',
                            required: true,
                            disablePadding: false,
                            label: 'Password',
                            Component: 'PasswordField',
                            hideInTable: true
                        }}
                        handleChange={this.handleChange}
                        value={this.state['password']}
                        autoFocus={false}
                    />
                </DialogMenu>
            </LoadingOverlay>
        );
    }
}
Users.propTypes = {
    enqueueSnackbar: PropTypes.func.isRequired
};

export default withSnackbar(Users);
