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



const styles = theme => ({
    textField: {
      marginLeft: theme.spacing.unit,
      marginRight: theme.spacing.unit,
    }
  });

class ChangePassword extends Component {

    state = {
        password: '',
    };

    handleClickShowPassword = () => {
        this.setState(state => ({ showPassword: !state.showPassword }));
    };

    handleChange = name => event => {
        this.setState({
            [name]: event.target.value,
        });
    }

    changePassword = () => {
        if (this.state.password !== ''){
            var options = {
                'method': 'PUT',
                'body': JSON.stringify({id: this.props.id, password: this.state.password})
            }
            this.props.Auth.fetch(window.USER_CHANGE_PASSWORD, options).then(
                function (result) {
                    this.closeForm();
                    this.props.notification("Password has been changed", 'info')
                }.bind(this)
            )
        }else{
            this.props.notification("Password not changed", 'info')
            this.closeForm();
        }
        
    
      }
    closeForm = () => {
        this.props.handleFormClose("changePassword");
    }

    render() {
        const { classes } = this.props;

        return (
            <Dialog
                open={this.props.open}
                onClose={this.closeForm}
                aria-labelledby="form-dialog-title"
            >
                <DialogTitle id="form-dialog-title">Change Password</DialogTitle>
                <DialogContent>
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
                </DialogContent>
                <DialogActions>
                    <Button onClick={this.closeForm} color="primary">
                        Cancel
            </Button>
                    <Button onClick={this.changePassword} color="primary">
                        Change Password
            </Button>
                </DialogActions>
            </Dialog>
        )
    }

}

export default withStyles(styles)(ChangePassword);