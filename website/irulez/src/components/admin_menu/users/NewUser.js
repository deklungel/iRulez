import React, { Component } from 'react';
import classNames from 'classnames';

import Button from '@material-ui/core/Button';
import TextField from '@material-ui/core/TextField';
import Dialog from '@material-ui/core/Dialog';
import DialogActions from '@material-ui/core/DialogActions';
import DialogContent from '@material-ui/core/DialogContent';
import DialogTitle from '@material-ui/core/DialogTitle';
import Visibility from '@material-ui/icons/Visibility';
import VisibilityOff from '@material-ui/icons/VisibilityOff';
import InputAdornment from '@material-ui/core/InputAdornment';
import IconButton from '@material-ui/core/IconButton';
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

class NewUser extends Component {

    state = {
        email: '',
        password: '',
        role: 'user',
        showPassword: false,
    };

    handleClickShowPassword = () => {
        this.setState(state => ({ showPassword: !state.showPassword }));
    };

    handleChange = name => event => {
        this.setState({
            [name]: event.target.value,
        });
    };

    addUser = () => {
        this.props.handleUserFormClose();
        var options = {
          'method': 'POST',
          'body' : JSON.stringify({email: this.state.email, password: md5(this.state.password), role: this.state.role})
        }
        Auth.fetch('http://localhost:4002/api/AddUser',options).then(
          function(result) {
            this.props.getUsersFromBackend();
          }.bind(this)
        )
    
      }

    render() {
        const { classes } = this.props;

        return (
            <Dialog
                open={this.props.open}
                onClose={this.props.handleUserFormClose}
                aria-labelledby="form-dialog-title"
            >
                <DialogTitle id="form-dialog-title">New User</DialogTitle>
                <DialogContent>
                    <TextField
                        autoFocus
                        className={classNames(classes.margin, classes.textField)}
                        id="email"
                        value={this.state.user}
                        onChange={this.handleChange('email')}
                        label="Email Address"
                        type="email"
                        fullWidth
                    />
                    <TextField
                        id="password"
                        className={classNames(classes.margin, classes.textField)}
                        type={this.state.showPassword ? 'text' : 'password'}
                        label="Password"
                        onChange={this.handleChange('password')}
                        fullWidth
                        InputProps={{
                            endAdornment: (
                                <InputAdornment position="end">
                                    <IconButton
                                        aria-label="Toggle password visibility"
                                        onClick={this.handleClickShowPassword}
                                    >
                                        {this.state.showPassword ? <VisibilityOff /> : <Visibility />}
                                    </IconButton>
                                </InputAdornment>
                            ),
                        }}
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
                    <Button onClick={this.props.handleUserFormClose} color="primary">
                        Cancel
            </Button>
                    <Button onClick={this.addUser} color="primary">
                        Add
            </Button>
                </DialogActions>
            </Dialog>
        )
    }

}

export default withStyles(styles)(NewUser);