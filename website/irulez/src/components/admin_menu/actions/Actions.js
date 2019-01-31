import React, { Component } from 'react';
import DialogMenu from '../DialogMenu';
import EnhancedTable from '../Table';
import PropTypes from 'prop-types';
import { withSnackbar } from 'notistack';
import AuthService from '../../AuthService';
import { withStyles } from '@material-ui/core/styles';
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
        rowsPerPage: 10
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
            this.fields.map(field => {
                if (field.array) {
                    if (this.state.lastSelectedRow[field.mapping]) {
                        var row = this.state.lastSelectedRow;
                        var tmp = this.state.lastSelectedRow[field.mapping].split(',').map(value => {
                            return parseInt(value);
                        });
                        row[field.mapping] = tmp;
                        return this.setState({
                            lastSelectedRow: row,
                            [field.id]: this.state.lastSelectedRow[field.mapping]
                        });
                    }
                } else {
                    return this.setState({
                        [field.id]: this.state.lastSelectedRow[field.mapping]
                    });
                }
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
            .catch(err => console.log(err));
    };

    add = () => {
        this.Action.addAction(
            this.state.name,
            this.state.action_type,
            this.state.trigger,
            this.state.timer,
            this.state.delay,
            this.state.master,
            this.state.condition,
            this.state.click_number,
            this.state.outputs_id,
            this.state.notifications_id
        )
            .then(() => {
                this.handleFormClose('newForm');
                this.handleNotification('Action has been added', 'success');
                this.getData();
            })
            .catch(err => {
                console.log(err);
                this.handleNotification(String(err), 'error');
            });
    };

    delete = () => {
        this.Action.deleteAction(this.state.selected)
            .then(() => {
                this.handleFormClose('deleteForm');
                this.handleNotification('Action has been deleted', 'warning');
                this.getData();
            })
            .catch(err => console.log(err));
    };
    edit = () => {
        this.Action.editAction2(this.state, this.fields);
    };

    edit2 = () => {
        this.Action.editAction(
            this.state.id,
            this.state.name,
            this.state.name_changed,
            this.state.action_type_name,
            this.state.action_type_name_changed,
            this.state.trigger_name,
            this.state.trigger_name_changed,
            this.state.timer,
            this.state.timer_changed,
            this.state.delay,
            this.state.delay_changed,
            this.state.master,
            this.state.master_changed,
            this.state.condition,
            this.state.condition_changed,
            this.state.click_number,
            this.state.click_number_changed,
            this.state.outputs_id,
            this.state.outputs_id_changed,
            this.state.notifications_id,
            this.state.notifications_id_changed
        )
            .then(() => {
                this.handleFormClose('newForm');
                this.handleNotification('Action has been added', 'success');
                this.getData();
            })
            .catch(err => {
                console.log(err);
                this.handleNotification(String(err), 'error');
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
            label: 'Type'
        },
        {
            id: 'action_type',
            mapping: 'action_type',
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
            mapping: 'trigger',
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
            mapping: 'delay',
            align: 'left',
            disablePadding: true,
            label: 'Delay',
            Component: 'SecondsField',
            addForm: true,
            editForm: true
        },
        {
            id: 'timer',
            mapping: 'timer',
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
            mapping: 'master_id',
            align: 'left',
            disablePadding: false,
            label: 'Master',
            Component: 'OutputField',
            addForm: true,
            editForm: true,
            dependency: 'action_type'
        },
        {
            id: 'condition',
            mapping: 'condition_id',
            align: 'left',
            disablePadding: true,
            label: 'Condition',
            Component: 'ConditionField',
            addForm: true,
            editForm: true
        },
        {
            id: 'click_number',
            mapping: 'click_number',
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
            mapping: 'outputs',
            align: 'left',
            disablePadding: true,
            label: 'Outputs',
            type: 'Chip'
        },
        {
            id: 'outputs_id',
            mapping: 'outputs_id',
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
            mapping: 'notifications',
            align: 'left',
            disablePadding: true,
            label: 'Notifications',
            type: 'Chip'
        },
        {
            id: 'notifications_id',
            mapping: 'notifications_id',
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
