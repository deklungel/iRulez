import React, { Component } from 'react';
import { withStyles } from '@material-ui/core/styles';
import classNames from 'classnames';
import TextField from '@material-ui/core/TextField';

const styles = theme => ({
    textField: {
        marginLeft: theme.spacing.unit,
        marginRight: theme.spacing.unit
    },
    content: {
        overflowY: 'visible'
    }
});

class MailField extends Component {
    state = {
        value: ''
    };

    onChange = name => event => {
        this.props.handleChange(name, event.target.value);
    };

    render() {
        const { classes, field, autoFocus } = this.props;

        return (
            <TextField
                required={field.required}
                autoFocus={autoFocus}
                className={classNames(classes.margin, classes.textField)}
                id={field.id}
                name={field.id}
                value={this.props.value}
                onChange={this.onChange(field.id)}
                label={field.label}
                type='email'
                fullWidth
            />
        );
    }
}

export default withStyles(styles)(MailField);
