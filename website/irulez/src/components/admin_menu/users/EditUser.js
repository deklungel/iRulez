import React, { Component } from 'react';
import classNames from 'classnames';

import Button from '@material-ui/core/Button';
import TextField from '@material-ui/core/TextField';
import Dialog from '@material-ui/core/Dialog';
import DialogActions from '@material-ui/core/DialogActions';
import DialogContent from '@material-ui/core/DialogContent';
import DialogTitle from '@material-ui/core/DialogTitle';
import { withStyles } from '@material-ui/core/styles';

import ChangePassword from './ChangePassword';

const styles = theme => ({
    textField: {
        marginLeft: theme.spacing.unit,
        marginRight: theme.spacing.unit,
    }
});

class EditUser extends Component {
    componentWillReceiveProps(newProps) {
        this.setState({ email: newProps.user.email });
        this.setState({ role: newProps.user.role });
        this.setState({ id: newProps.user.id });
    }
    state = {
        id: '',
        email: '',
        role: '',
        changed_email: false,
        changed_role: false,
        changePasswordForm: false,
        emailError: false,
    };


    handleChange = name => event => {
        let changed = "changed_" + name
        let error = name + "Error" 
        this.setState({
            [name]: event.target.value,
            [changed]: true,
            [error]: false,
        });
        if (event.target.value === this.props.user[name]) {
            this.setState({
                [changed]: false,
            })
        }

    };

    EditUser = () => {
        if (this.validateInput()) {
            if (this.state.changed_email || this.state.changed_role) {
                var json = {}
                json.id = this.state.id
                if (this.state.changed_email) {
                    json.email = this.state.email
                }
                if (this.state.changed_role) {
                    json.role = this.state.role
                }
                var options = {
                    'method': 'PUT',
                    'body': JSON.stringify(json)
                }
                this.props.Auth.fetch(window.USER_EDIT, options).then(
                    function (result) {
                        this.closeForm();
                        this.props.getUsersFromBackend();
                        this.props.notification("User has been changed", 'info')
                    }.bind(this)
                )
            } else {
                this.closeForm();
            }

        }
    }

    validateInput() {
        if (this.state.email !== '' && this.validateEmail(this.state.email)) {
            return true
        }
        this.setState({ emailError: true })
        return false

    }
    validateEmail(email) {
        if (/^[a-zA-Z0-9]+@[a-zA-Z0-9]+\.[A-Za-z]+$/.test(email)) {
            return true
        }
        return false
    }

    closeForm = () => {
        this.props.handleFormClose("EditForm");
        this.setState({emailError: false,})
    }

    openChangePasswordForm = () => {
        this.setState({ changePasswordForm: true })
        
    }

    closeChangePasswordForm = () => {
        this.setState({ changePasswordForm: false })
    }


    render() {
        const { classes } = this.props;

        return (
            <Dialog
                open={this.props.open}
                onClose={this.closeForm}
                aria-labelledby="form-dialog-title"
            >
                <DialogTitle id="form-dialog-title">Edit User</DialogTitle>
                <DialogContent>
                    <TextField
                        autoFocus
                        error={this.state.emailError}
                        className={classNames(classes.margin, classes.textField)}
                        id="email"
                        value={this.state.email}
                        onChange={this.handleChange('email')}
                        label="Email Address"
                        type="email"
                        fullWidth
                    />

                    <TextField
                        id="outlined-select-currency-native"
                        select
                        label="Role"
                        className={classes.textField}
                        value={this.state.role}
                        onChange={this.handleChange('role')}
                        SelectProps={{
                            native: true,
                            MenuProps: {
                                className: classes.menu,
                            },
                        }}
                        margin="dense"
                        fullWidth
                    >

                        <option key="user" value="user">
                            User
                        </option>
                        <option key="admin" value="admin">
                            Administrator
                        </option>
                    </TextField>
                </DialogContent>
                <DialogActions>
                    <Button onClick={this.closeForm} color="primary">
                        Cancel
                    </Button>
                    <Button onClick={this.openChangePasswordForm} color="primary">
                        Change Password
                    </Button>
                    <Button onClick={this.EditUser} color="primary">
                        Edit
                    </Button>
                </DialogActions>
                <ChangePassword
                    id={this.state.id}
                    Auth={this.props.Auth}
                    open={this.state.changePasswordForm}
                    handleFormClose={this.closeChangePasswordForm}
                    notification={this.props.notification} />
            </Dialog>
        )
    }

}

export default withStyles(styles)(EditUser);