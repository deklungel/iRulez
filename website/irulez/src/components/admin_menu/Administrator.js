import React, { Component } from 'react';
import AuthService from '../AuthService';
import SideBar from '../SideBar';
import { Route } from 'react-router-dom';
import PropTypes from 'prop-types';
import classNames from 'classnames';
import { withStyles } from '@material-ui/core/styles';
import withAuth from './../withAuth';
import { SnackbarProvider } from 'notistack';

import Admin from './Dashboard';
import Users from './users/Users';
import Devices from './devices/Devices';
import Actions from './actions/Actions';
import Outputs from './outputs/Outputs';
import Inputs from './inputs/Inputs';
import Menus from './menus/Menus';
import DimmerActions from './actions/DimmerActions';
import Processes from './processes/Processes';
import { BrowserView, MobileView, isBrowser, isMobile } from 'react-device-detect';
import Groups from './users/Groups';

const Auth = new AuthService();

const drawerWidth = 240;

const styles = theme => ({
    drawerHeader: {
        display: 'flex',
        alignItems: 'center',
        padding: '0 8px',
        ...theme.mixins.toolbar,
        justifyContent: 'flex-end'
    },
    content: {
        flexGrow: 1,
        //padding: theme.spacing.unit * 3,
        transition: theme.transitions.create('margin', {
            easing: theme.transitions.easing.sharp,
            duration: theme.transitions.duration.leavingScreen
        }),
        marginLeft: 0
    },
    contentShift: {
        transition: theme.transitions.create('margin', {
            easing: theme.transitions.easing.easeOut,
            duration: theme.transitions.duration.enteringScreen
        }),
        marginLeft: +drawerWidth
    }
});

class Administrator extends Component {
    user = Auth.getProfile();

    state = {
        sidebarOpen: false,
        MenuOpen: ''
    };

    componentWillMount() {
        if (!this.user.admin) {
            this.props.history.replace('/');
        }
    }

    sideBarToggle = value => {
        this.setState({ sidebarOpen: value });
    };
    ToggleCollapse = menu => {
        if (this.state.MenuOpen === menu) {
            this.setState({ MenuOpen: '' });
        } else {
            this.setState({ MenuOpen: menu });
        }
    };
    SetCollapse = menu => {
        this.setState({ MenuOpen: menu });
    };

    checkSidebarState = () => {
        if (isMobile) {
            this.sideBarToggle(false);
        } else {
            this.sideBarToggle(true);
        }
    };

    render() {
        const { classes } = this.props;

        return (
            <div>
                <SideBar
                    Auth={Auth}
                    sidebarToggle={this.sideBarToggle}
                    ToggleCollapse={this.ToggleCollapse}
                    MenuOpen={this.state.MenuOpen}
                    open={this.state.sidebarOpen}
                />
                <SnackbarProvider maxSnack={3}>
                    <main
                        className={classNames(classes.content, {
                            [classes.contentShift]: this.state.sidebarOpen
                        })}
                    >
                        <div className={classes.drawerHeader} />
                        <Route
                            exact
                            path='/administrator'
                            render={props => <Admin {...props} Collapse={this.SetCollapse} />}
                        />
                        <Route
                            path='/administrator/actions/relais'
                            render={props => (
                                <Actions
                                    {...props}
                                    checkSidebarState={this.checkSidebarState}
                                    Collapse={this.SetCollapse}
                                />
                            )}
                        />
                        <Route
                            exact
                            path='/administrator/actions/dimmer'
                            render={props => (
                                <DimmerActions
                                    {...props}
                                    checkSidebarState={this.checkSidebarState}
                                    Collapse={this.SetCollapse}
                                />
                            )}
                        />
                        <Route
                            exact
                            path='/administrator/user/users'
                            render={props => (
                                <Users
                                    {...props}
                                    checkSidebarState={this.checkSidebarState}
                                    Collapse={this.SetCollapse}
                                />
                            )}
                        />
                        <Route
                            exact
                            path='/administrator/user/groups'
                            render={props => (
                                <Groups
                                    {...props}
                                    checkSidebarState={this.checkSidebarState}
                                    Collapse={this.SetCollapse}
                                />
                            )}
                        />
                        <Route
                            exact
                            path='/administrator/menus'
                            render={props => (
                                <Menus
                                    {...props}
                                    checkSidebarState={this.checkSidebarState}
                                    Collapse={this.SetCollapse}
                                />
                            )}
                        />
                        <Route
                            exact
                            path='/administrator/devices'
                            render={props => (
                                <Devices
                                    {...props}
                                    checkSidebarState={this.checkSidebarState}
                                    Collapse={this.SetCollapse}
                                />
                            )}
                        />
                        <Route
                            exact
                            path='/administrator/outputs'
                            render={props => (
                                <Outputs
                                    {...props}
                                    checkSidebarState={this.checkSidebarState}
                                    Collapse={this.SetCollapse}
                                />
                            )}
                        />
                        <Route
                            exact
                            path='/administrator/inputs'
                            render={props => (
                                <Inputs
                                    {...props}
                                    checkSidebarState={this.checkSidebarState}
                                    Collapse={this.SetCollapse}
                                />
                            )}
                        />
                        <Route
                            exact
                            path='/administrator/processes'
                            render={props => (
                                <Processes
                                    {...props}
                                    checkSidebarState={this.checkSidebarState}
                                    Collapse={this.SetCollapse}
                                />
                            )}
                        />
                    </main>
                </SnackbarProvider>
            </div>
        );
    }
}
Administrator.propTypes = {
    classes: PropTypes.object.isRequired,
    theme: PropTypes.object.isRequired
};

export default withStyles(styles, { withTheme: true })(withAuth(Administrator));
