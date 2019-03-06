import React, { Component } from 'react';
import DialogMenu from '../DialogMenu';
import EnhancedTable from '../Table';
import PropTypes from 'prop-types';
import { withSnackbar } from 'notistack';
import AuthService from '../../AuthService';
import ActionService from './ActionService';
import { components } from '../fields/iRulezFields';

import LoadingOverlay from 'react-loading-overlay';
import CircleLoader from 'react-spinners/CircleLoader';

class Actions extends Component {
    Auth = new AuthService();
    Action = new ActionService();

    constructor(props) {
        super(props);
        this.props.Collapse('actions');
    }

    state = {
        newForm: false,
        editForm: false,
        deleteForm: false,
        data: [],
        selected: [],
        lastSelectedRow: [],
        isActive: true,
        rowsPerPage: 10,
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
            .filter(field => {
                return field.editForm;
            })
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
        this.Action.getDataWithTimeOut()
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
        this.Action.addAction(this.state, this.fields)
            .then(() => {
                this.handleFormClose('newForm');
                this.handleNotification('Action has been added', 'success');
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
        this.Action.deleteAction(this.state.selected)
            .then(() => {
                this.handleFormClose('deleteForm');
                this.handleNotification('Action has been deleted', 'warning');
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
        this.Action.editAction(this.state, this.fields)
            .then(() => {
                this.handleFormClose('editForm');
                this.handleNotification('Action has been changed', 'info');
                this.getData();
            })
            .catch(err => {
                console.log(err);
                this.handleNotification(String(err), 'error');
                this.setState({ submitDisabled: false });
            });
    };

    fields = [
        //{ id: 'id', align: 'left', disablePadding: true, label: 'ID' },
        {
            id: 'name',
            mapping: 'name',
            align: 'left',
            disablePadding: true,
            label: 'Name',
            Component: 'NameField',
            addForm: true,
            editForm: true,
            required: true,
            autoFocus: true
        },
        {
            id: 'action_type_name',
            label: 'Types'
        },
        {
            id: 'action_type',
            align: 'left',
            Component: 'ActionTypeField',
            required: true,
            disablePadding: true,
            label: 'Type',
            addForm: true,
            editForm: true,
            autoFocus: false,
            default: 1,
            hideInTable: true
        },
        {
            id: 'trigger_name',
            label: 'Trigger'
        },
        {
            id: 'trigger',
            align: 'left',
            disablePadding: true,
            label: 'Trigger',
            Component: 'TriggerField',
            required: true,
            addForm: true,
            editForm: true,
            autoFocus: false,
            hideInTable: true,
            default: 1
        },
        {
            id: 'delay',
            align: 'left',
            disablePadding: true,
            label: 'Delay',
            Component: 'SecondsField',
            addForm: true,
            editForm: true
        },
        {
            id: 'timer',
            align: 'left',
            disablePadding: true,
            label: 'Timer',
            Component: 'TimerField',
            addForm: true,
            editForm: true,
            dependency: 'action_type'
        },
        {
            id: 'master',
            align: 'left',
            disablePadding: false,
            label: 'Master'
        },
        {
            id: 'master_id',
            mapping: 'master_id',
            align: 'left',
            disablePadding: false,
            label: 'Master',
            Component: 'MasterField',
            addForm: true,
            editForm: true,
            dependency: 'action_type',
            hideInTable: true
        },
        {
            id: 'condition',
            align: 'left',
            disablePadding: true,
            label: 'Condition'
        },
        {
            id: 'condition_id',
            label: 'Condition',
            Component: 'ConditionField',
            addForm: true,
            editForm: true,
            hideInTable: true
        },
        {
            id: 'click_number',
            align: 'left',
            disablePadding: true,
            label: 'Click Number',
            Component: 'NumberField',
            addForm: true,
            editForm: true,
            required: true,
            default: 1
        },
        {
            id: 'outputs',
            align: 'left',
            disablePadding: true,
            label: 'Outputs',
            type: 'Chip',
            forLabel: true
        },
        {
            id: 'outputs_id',
            align: 'left',
            disablePadding: true,
            label: 'Outputs',
            Component: 'MultipleOutputField',
            labelField: 'outputs',
            addForm: true,
            editForm: true,
            array: true,
            hideInTable: true
        },
        {
            id: 'notifications',
            align: 'left',
            disablePadding: true,
            label: 'Notifications',
            type: 'Chip',
            forLabel: true
        },
        {
            id: 'notifications_id',
            align: 'left',
            disablePadding: true,
            label: 'Notifications',
            Component: 'MultipleNotificationField',
            labelField: 'notifications',
            addForm: true,
            editForm: true,
            array: true,
            hideInTable: true
        }
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
                    updateRowsPerPage={this.updateRowsPerPage}
                    title='Action'
                    addIconTooltip='Add action'
                    editIconTooltip='Edit action'
                    deleteIconTooltip='Delete action'
                    rowsPerPage={this.state.rowsPerPage}
                />
                <DialogMenu
                    open={this.state.newForm}
                    submitDisabled={this.state.submitDisabled}
                    //fullScreen={true}
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
                    submitDisabled={this.state.submitDisabled}
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
                                    labelField={this.state[field.labelField]}
                                />
                            );
                        })}
                </DialogMenu>
                <DialogMenu
                    open={this.state.deleteForm}
                    submitDisabled={this.state.submitDisabled}
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
Actions.propTypes = {
    enqueueSnackbar: PropTypes.func.isRequired
};

export default withSnackbar(Actions);
