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
import InputService from './InputService';
import TextField from '@material-ui/core/TextField';
import Paper from '@material-ui/core/Paper';
import InputBase from '@material-ui/core/InputBase';
import IconButton from '@material-ui/core/IconButton';
import SearchIcon from '@material-ui/icons/Search';

const styles = theme => ({
    textField: {
        marginLeft: theme.spacing.unit,
        marginRight: theme.spacing.unit
    },
    content: {
        overflowY: 'visible'
    },
    search: {
        padding: '2px 4px',
        margin: '5px',
        display: 'flex',
        alignItems: 'center',
        width: 'calc(100% - 10px)'
    },
    input: {
        marginLeft: 8,
        flex: 1
    },
    iconButton: {
        padding: 10
    }
});

class Inputs extends Component {
    Auth = new AuthService();
    Service = new InputService();
    originalValueRow = [];

    constructor(props) {
        super(props);
        this.props.Collapse('inputs');
    }

    state = {
        newForm: false,
        editForm: false,
        deleteForm: false,
        data: [],
        filterArray: [],
        selected: [],
        lastSelectedRow: [],
        isActive: true,
        rowsPerPage: 25,
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
        this.Service.getData()
            .then(response => {
                this.setState({ data: response });
                this.setState({ filterArray: response });
                this.setState({ selected: [] });
                this.setState({ isActive: false });
            })
            .catch(err => {
                console.log(err);
                this.handleNotification(String(err), 'error');
            });
    };

    filter = event => {
        if (event.target.value == '') {
            var filterArray = this.state.data;
        } else {
            var filterArray = this.state.data.filter(row => {
                return row.actions && row.actions.toLowerCase().includes(event.target.value.toLowerCase());
            });
        }
        this.setState({ filterArray: filterArray });
    };

    edit = () => {
        this.setState({ submitDisabled: true });
        this.Service.edit(this.state, this.fields)
            .then(() => {
                this.handleFormClose('editForm');
                this.handleNotification('Device has been changed', 'info');
                this.getData();
            })
            .catch(err => {
                console.log(err);
                this.handleNotification(String(err), 'error');
                this.setState({ submitDisabled: false });
            });
    };

    fields = [
        { id: 'id', align: 'left', disablePadding: true, label: 'ID' },
        {
            id: 'name',
            align: 'left',
            disablePadding: true,
            label: 'Name',
            editForm: true,
            required: false,
            edit_autofocus: true
        },
        {
            id: 'number',
            align: 'left',
            disablePadding: false,
            label: 'Number'
        },
        {
            id: 'time_between_clicks',
            align: 'left',
            disablePadding: false,
            label: 'Time between clicks',
            editForm: true,
            required: false,
            edit_autofocus: false,
            Component: 'DecimalField'
        },
        {
            id: 'actions',
            align: 'left',
            disablePadding: true,
            label: 'Actions',
            type: 'Chip',
            forLabel: true
        },
        {
            id: 'actions_id',
            align: 'left',
            disablePadding: true,
            label: 'Actions',
            Component: 'MultipleActionField',
            labelField: 'actions',
            addForm: true,
            editForm: true,
            array: true,
            hideInTable: true
        },
        {
            id: 'device_name',
            label: 'Device'
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
                <Paper className={classes.search} elevation={1}>
                    <InputBase onChange={this.filter} className={classes.input} placeholder='Search' />
                    <IconButton className={classes.iconButton} aria-label='Search'>
                        <SearchIcon />
                    </IconButton>
                </Paper>
                <EnhancedTable
                    data={this.state.filterArray}
                    fields={fields}
                    selected={this.state.selected}
                    handleFormOpen={this.handleFormOpen}
                    disableNew={true}
                    disableDelete={true}
                    updateRowsPerPage={this.updateRowsPerPage}
                    updatedSelected={this.updatedSelected}
                    title='Action'
                    editIconTooltip='Edit output'
                    rowsPerPage={this.state.rowsPerPage}
                />

                <DialogMenu
                    open={this.state.editForm}
                    submitDisabled={this.state.submitDisabled}
                    handleFormAccept={this.edit}
                    handleFormCancel={() => this.handleFormClose('editForm')}
                    title='Edit Output'
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
            </LoadingOverlay>
        );
    }
}
Inputs.propTypes = {
    enqueueSnackbar: PropTypes.func.isRequired
};

export default withStyles(styles)(withSnackbar(Inputs));
