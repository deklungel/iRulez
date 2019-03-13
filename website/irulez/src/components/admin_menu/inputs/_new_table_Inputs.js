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
import MUIDataTable from 'mui-datatables';
import CustomToolbarSelect from './CustomToolbarSelect';
import CustomToolbar from './CustomToolbar';
import { createMuiTheme, MuiThemeProvider } from '@material-ui/core/styles';

const styles = theme => ({
    OverlayWrapper: {
        height: 'calc(100vh - 64px)'
    }
});

class Inputs extends Component {
    Auth = new AuthService();
    Service = new InputService();

    constructor(props) {
        super(props);
        this.props.Collapse('inputs');
    }

    state = {
        newForm: false,
        editForm: false,
        deleteForm: false,
        data: [],
        selected: [],
        lastSelectedRow: [],
        isActive: true,
        rowsPerPage: 25,
        submitDisabled: false
    };

    componentDidMount() {
        this.getData();
        this.props.checkSidebarState();
        //this.resetValues();
    }

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

    test() {
        alert('Test');
    }

    getMuiTheme = () =>
        createMuiTheme({
            overrides: { MUIDataTable: { responsiveScroll: { backgroundColor: 'red' } } }
        });

    render() {
        const columns = ['Name', 'Company', 'City', 'State'];

        const data = [
            ['Joe James', 'Test Corp', 'Yonkers', 'NY'],
            ['John Walsh', 'Test Corp', 'Hartford', 'CT'],
            ['Bob Herm', 'Test Corp', 'Tampa', 'FL'],
            ['James Houston', 'Test Corp', 'Dallas', 'TX']
        ];

        const options = {
            filterType: 'dropdown',
            responsive: 'scoll',
            print: false,
            download: false,
            overrides: { MUIDataTable: { responsiveScroll: { backgroundColor: 'red' } } },
            customToolbarSelect: (selectedRows, displayData, setSelectedRows) => (
                <CustomToolbarSelect
                    selectedRows={selectedRows}
                    displayData={displayData}
                    setSelectedRows={setSelectedRows}
                    onRowsDelete={this.test}
                />
            ),
            customToolbar: () => {
                return <CustomToolbar />;
            }
        };
        const { classes } = this.props;

        return (
            <LoadingOverlay
                className={classes.OverlayWrapper}
                active={this.state.isActive}
                spinner={<CircleLoader size={150} color={'yellow'} />}
                text='Loading your content...'
            >
                <MuiThemeProvider theme={this.getMuiTheme()}>
                    <MUIDataTable
                        className={classes.test}
                        title={'Inputs'}
                        data={data}
                        columns={columns}
                        options={options}
                    />
                </MuiThemeProvider>
            </LoadingOverlay>
        );
    }
}

Inputs.propTypes = {
    enqueueSnackbar: PropTypes.func.isRequired
};

export default withStyles(styles)(withSnackbar(Inputs));
