import React, { Component } from 'react';
import { withStyles } from '@material-ui/core/styles';
import classNames from 'classnames';
import { TextValidator } from 'react-material-ui-form-validator';

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
            <TextValidator
                required={field.required}
                autoFocus={autoFocus}
                className={classNames(classes.margin, classes.textField)}
                id={field.id}
                name={field.id}
                value={this.props.value}
                onChange={this.onChange(field.id)}
                validators={['isEmail']}
                label={field.label}
                type='string'
                fullWidth
            />
        );
    }
}

export default withStyles(styles)(MailField);
