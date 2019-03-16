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
import MenuService from './MenuService';
import App from './Reorder';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import Radio from '@material-ui/core/Radio';

const styles = theme => ({
    textField: {
        marginLeft: theme.spacing.unit,
        marginRight: theme.spacing.unit
    },
    content: {
        overflowY: 'visible'
    }
});

class Menus extends Component {
    Auth = new AuthService();
    Service = new MenuService();
    originalValueRow = [];

    constructor(props) {
        super(props);
        this.props.Collapse('users');
    }

    state = {
        newForm: false,
        editForm: false,
        deleteForm: false,
        changeOrderForm: false,
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

    handleChangeOrderFormClose = form => {
        this.setState({
            changeOrderForm: false,
            submitDisabled: false
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
                this.handleNotification('Menu has been added', 'success');
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
                this.handleNotification('Menu has been deleted', 'warning');
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
            .then(() => {
                this.handleFormClose('editForm');
                this.handleNotification('Menu has been changed', 'info');
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
            id: 'name',
            align: 'left',
            disablePadding: true,
            label: 'Name',
            addForm: true,
            editForm: true,
            required: true,
            add_autoFocus: true,
            edit_autoFocus: true
        },
        {
            id: 'display_name',
            align: 'left',
            disablePadding: false,
            label: 'Display Name'
        },
        {
            id: 'parent_name',
            label: 'parent'
        },
        {
            id: 'parent',
            align: 'left',
            disablePadding: true,
            label: 'Parent Menu',
            Component: 'MenuField',
            addForm: true,
            editForm: true,
            autoFocus: false,
            hideInTable: true
        },
        {
            id: 'order',
            align: 'left',
            disablePadding: true,
            label: 'order'
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
                    updateRowsPerPage={this.updateRowsPerPage}
                    updatedSelected={this.updatedSelected}
                    title='Action'
                    addIconTooltip='Add action'
                    editIconTooltip='Edit action'
                    deleteIconTooltip='Delete action'
                    rowsPerPage={this.state.rowsPerPage}
                />
                <DialogMenu
                    open={this.state.newForm}
                    submitDisabled={this.state.submitDisabled}
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
                    extraButton='Change order'
                    extraButtonAction={() => this.handleFormOpen('changeOrderForm')}
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
                    submitDisabled={this.state.submitDisabled}
                    handleFormAccept={this.delete}
                    handleFormCancel={() => this.handleFormClose('deleteForm')}
                    title='Delete Menu'
                    acceptLabel='Delete'
                >
                    Are you sure you want to delete menu {JSON.stringify(this.state.selected)}
                </DialogMenu>
                <DialogMenu
                    open={this.state.changeOrderForm}
                    submitDisabled={this.state.submitDisabled}
                    handleFormAccept={this.changePassword}
                    handleFormCancel={() => this.handleChangeOrderFormClose()}
                    title='Change order'
                    acceptLabel='Change'
                >
                    <FormControlLabel
                        value='before'
                        control={
                            <Radio
                                checked={this.state.selectedValue === 'a'}
                                onChange={this.handleChange}
                                value='a'
                                name='radio-button-demo'
                                aria-label='A'
                            />
                        }
                        label='Before'
                    />
                    <FormControlLabel
                        value='after'
                        control={
                            <Radio
                                checked={this.state.selectedValue === 'a'}
                                onChange={this.handleChange}
                                name='radio-button-demo'
                                aria-label='A'
                            />
                        }
                        label='After'
                    />
                </DialogMenu>
                <App />
            </LoadingOverlay>
        );
    }
}
Menus.propTypes = {
    enqueueSnackbar: PropTypes.func.isRequired
};

export default withStyles(styles)(withSnackbar(Menus));
