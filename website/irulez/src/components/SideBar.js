import React from 'react';
import PropTypes from 'prop-types';
import classNames from 'classnames';
import { withStyles } from '@material-ui/core/styles';
import Drawer from '@material-ui/core/Drawer';
import CssBaseline from '@material-ui/core/CssBaseline';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import List from '@material-ui/core/List';
import Typography from '@material-ui/core/Typography';
import Divider from '@material-ui/core/Divider';
import IconButton from '@material-ui/core/IconButton';
import MenuIcon from '@material-ui/icons/Menu';
import ChevronLeftIcon from '@material-ui/icons/ChevronLeft';
import ChevronRightIcon from '@material-ui/icons/ChevronRight';
import ListItem from '@material-ui/core/ListItem';
import ListItemIcon from '@material-ui/core/ListItemIcon';
import ListItemText from '@material-ui/core/ListItemText';
import ExpandLess from '@material-ui/icons/ExpandLess';
import ExpandMore from '@material-ui/icons/ExpandMore';
import Collapse from '@material-ui/core/Collapse';
import { NavLink } from 'react-router-dom';
import { withRouter } from 'react-router-dom';

import SendIcon from '@material-ui/icons/Send';
import PeopleIcon from '@material-ui/icons/People';
import PersonIcon from '@material-ui/icons/Person';
import WallIcon from 'mdi-react/WallIcon';
import LogoutIcon from 'mdi-react/LogoutIcon';
import ChipIcon from 'mdi-react/ChipIcon';
import CogsIcon from "mdi-react/CogsIcon";
import GaugeIcon from "mdi-react/GaugeIcon";
import LightbulbOnOutlineIcon from 'mdi-react/LightbulbOnOutlineIcon'

const drawerWidth = 240;

const styles = theme => ({
    root: {
        display: 'flex'
    },
    appBar: {
        transition: theme.transitions.create(['margin', 'width'], {
            easing: theme.transitions.easing.sharp,
            duration: theme.transitions.duration.leavingScreen
        })
    },
    appBarShift: {
        width: `calc(100% - ${drawerWidth}px)`,
        marginLeft: drawerWidth,
        transition: theme.transitions.create(['margin', 'width'], {
            easing: theme.transitions.easing.easeOut,
            duration: theme.transitions.duration.enteringScreen
        })
    },
    menuButton: {
        marginLeft: 12,
        marginRight: 20
    },
    hide: {
        display: 'none'
    },
    drawer: {
        width: drawerWidth,
        flexShrink: 0
    },
    drawerPaper: {
        width: drawerWidth
    },
    drawerHeader: {
        display: 'flex',
        alignItems: 'center',
        padding: '0 8px',
        ...theme.mixins.toolbar,
        justifyContent: 'flex-end'
    },
    nested: {
        paddingLeft: theme.spacing.unit * 4
    },
    active: {
        backgroundColor: 'rgba(0, 0, 0, 0.14)'
    }
});

function ListItemLink(props) {
    const { primary, to, icon, className, classes } = props;
    return (
        <li>
            <ListItem button className={className} activeClassName={classes.active} component={NavLink} exact to={to}>
                <ListItemIcon>{icon}</ListItemIcon>
                <ListItemText inset primary={primary} />
            </ListItem>
        </li>
    );
}

ListItemLink.propTypes = {
    primary: PropTypes.node.isRequired,
    to: PropTypes.string.isRequired
};

class SideBar extends React.Component {
    constructor(props) {
        super(props);
        this.handleLogout = this.handleLogout.bind(this);
    }

    componentWillReceiveProps = props => {
        this.setState({
            [props.open]: true
        });
    };

    state = {
        open: true,
        subopen: false
    };

    handleClick = menu => {
        this.props.ToggleCollapse(menu);
    };

    handleDrawerOpen = () => {
        this.setState({ open: true });
        this.props.sidebarToggle(true);
    };

    handleDrawerClose = () => {
        this.setState({ open: false });
        this.props.sidebarToggle(false);
    };

    handleLogout() {
        this.props.Auth.logout();
        this.props.history.replace('/login');
        // history.push('/login')
    }

    render() {
        const { classes, theme } = this.props;
        const { open } = this.state;

        return (
            <div className={classes.root}>
                <CssBaseline />
                <AppBar
                    position='fixed'
                    className={classNames(classes.appBar, {
                        [classes.appBarShift]: open
                    })}
                >
                    <Toolbar disableGutters={!open}>
                        <IconButton
                            color='inherit'
                            aria-label='Open drawer'
                            onClick={this.handleDrawerOpen}
                            className={classNames(classes.menuButton, open && classes.hide)}
                        >
                            <MenuIcon />
                        </IconButton>
                        <Typography variant='h6' color='inherit' noWrap>
                            iRulez Administration
                        </Typography>
                    </Toolbar>
                </AppBar>
                <Drawer
                    className={classes.drawer}
                    variant='persistent'
                    anchor='left'
                    open={open}
                    classes={{
                        paper: classes.drawerPaper
                    }}
                >
                    <div className={classes.drawerHeader}>
                        <IconButton onClick={this.handleDrawerClose}>
                            {theme.direction === 'ltr' ? <ChevronLeftIcon /> : <ChevronRightIcon />}
                        </IconButton>
                    </div>

                    <Divider />
                    <List
                        component="nav"

                    >

                        <ListItemLink to="/administrator" classes={classes} button primary="Dashboard" icon={<GaugeIcon />} />
                        <ListItemLink to="/administrator/actions" classes={classes} button primary="Actions" icon={<CogsIcon />} />
                        <ListItemLink to="/administrator/devices" classes={classes} button primary="Devices" icon={<ChipIcon />} />
                        <ListItem button>
                            <ListItemIcon>
                                <LightbulbOnOutlineIcon />
                            </ListItemIcon>
                            <ListItemText inset primary='vButtons' />
                        </ListItem>
                        <ListItem
                            button
                            onClick={() => {
                                this.handleClick('users');
                            }}
                        >
                            <ListItemIcon>
                                <PeopleIcon />
                            </ListItemIcon>
                            <ListItemText inset primary='Users' />
                            {this.state.users ? <ExpandLess /> : <ExpandMore />}
                        </ListItem>
                        <Collapse in={this.props.MenuOpen === 'users'} timeout='auto' unmountOnExit>
                            <List component='div' disablePadding>
                                <ListItemLink
                                    to='/administrator/users'
                                    className={classes.nested}
                                    classes={classes}
                                    primary='Add/edit'
                                    icon={<PersonIcon />}
                                />
                                <ListItem button className={classes.nested}>
                                    <ListItemIcon>
                                        <WallIcon />
                                    </ListItemIcon>
                                    <ListItemText primary='User Rights' />
                                </ListItem>
                            </List>
                        </Collapse>
                        <Divider />
                        <ListItem button onClick={this.handleLogout}>
                            <ListItemIcon>
                                <LogoutIcon />
                            </ListItemIcon>
                            <ListItemText primary='Logout' />
                        </ListItem>
                    </List>
                </Drawer>
            </div>
        );
    }
}

SideBar.propTypes = {
    classes: PropTypes.object.isRequired,
    theme: PropTypes.object.isRequired
};

export default withStyles(styles, { withTheme: true })(withRouter(SideBar));
