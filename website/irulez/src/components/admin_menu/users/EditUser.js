import React, { Component } from 'react';
import classNames from 'classnames';

import Button from '@material-ui/core/Button';
import TextField from '@material-ui/core/TextField';
import Dialog from '@material-ui/core/Dialog';
import DialogActions from '@material-ui/core/DialogActions';
import DialogContent from '@material-ui/core/DialogContent';
import DialogTitle from '@material-ui/core/DialogTitle';
import { withStyles } from '@material-ui/core/styles';

import md5 from 'md5';

import AuthService from '../../AuthService';

const Auth = new AuthService();

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
    };


    handleChange = name => event => {
        let changed = "changed_" + name

        this.setState({
            [name]: event.target.value,
            [changed]: true,
        });
        if (event.target.value === this.props.user[name]) {
            this.setState({
                [changed]: false,
            })
        }

    };

    EditUser = () => {
        if (this.state.changed_email || this.state.changed_role) {
            var json = {}
            json.id = this.state.id 
            if(this.state.changed_email){
                json.email = this.state.email
            }
            if(this.state.changed_role){
                json.role = this.state.role
            }
            var options = {
                'method': 'POST',
                'body': JSON.stringify(json)
            }
            Auth.fetch('http://localhost:4002/api/user/edit', options).then(
                function (result) {
                    this.closeForm();
                    this.props.getUsersFromBackend();
                }.bind(this)
            )
        }

    }
    closeForm = () => {
        this.props.handleFormClose("EditForm");
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
                    <Button onClick={this.EditUser} color="primary">
                        Edit
            </Button>
                </DialogActions>
            </Dialog>
        )
    }

}

export default withStyles(styles)(EditUser);