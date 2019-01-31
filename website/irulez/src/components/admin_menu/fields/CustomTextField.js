import React, { Component } from 'react';
import { withStyles } from '@material-ui/core/styles';
import TextField from '@material-ui/core/TextField';
import classNames from 'classnames';

const styles = theme => ({
    textField: {
        margin: theme.spacing.unit
    },
    content: {
        overflowY: 'visible'
    }
});

class CustomTextField extends Component {
    state = {
        error: false
    };

    onChange = name => event => {
        this.props.handleChange(name, event.target.value);
    };

    render() {
        const { classes, field, value } = this.props;

        return (
            <TextField
                required={field.required}
                autoFocus={field.edit_autoFocus}
                className={classNames(classes.margin, classes.textField)}
                id='name'
                value={value}
                onChange={this.onChange(field.id)}
                label={field.label}
                type='string'
                fullWidth
            />
        );
    }
}

export default withStyles(styles)(CustomTextField);
