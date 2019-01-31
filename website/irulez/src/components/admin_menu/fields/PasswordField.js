import React, { Component } from 'react';
import { withStyles } from '@material-ui/core/styles';
import TextField from '@material-ui/core/TextField';
import classNames from 'classnames';
import Visibility from '@material-ui/icons/Visibility';
import VisibilityOff from '@material-ui/icons/VisibilityOff';
import InputAdornment from '@material-ui/core/InputAdornment';
import IconButton from '@material-ui/core/IconButton';

const styles = theme => ({
    textField: {
        marginLeft: theme.spacing.unit,
        marginRight: theme.spacing.unit
    },
    content: {
        overflowY: 'visible'
    }
});

class PasswordField extends Component {
    state = {
        showPassword: false
    };

    onChange = name => event => {
        this.props.handleChange(name, event.target.value);
    };

    handleClickShowPassword = () => {
        this.setState(state => ({ showPassword: !state.showPassword }));
    };

    render() {
        const { classes, field } = this.props;

        return (
            <TextField
                required={field.required}
                error={this.state.passwordError}
                id={field.id}
                className={classNames(classes.margin, classes.textField)}
                type={this.state.showPassword ? 'text' : 'password'}
                label={field.label}
                onChange={this.onChange(field.id)}
                fullWidth
                InputProps={{
                    endAdornment: (
                        <InputAdornment position='end'>
                            <IconButton aria-label='Toggle password visibility' onClick={this.handleClickShowPassword}>
                                {this.state.showPassword ? <VisibilityOff /> : <Visibility />}
                            </IconButton>
                        </InputAdornment>
                    )
                }}
            />
        );
    }
}

export default withStyles(styles)(PasswordField);
