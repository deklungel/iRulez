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

class NameField extends Component {
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
                error={this.state.error}
                required={field.required}
                autoFocus={autoFocus}
                className={classNames(classes.margin, classes.textField)}
                id={field.id}
                name={field.id}
                value={this.props.value}
                onChange={this.onChange(field.id)}
                label={field.label}
                type='string'
                fullWidth
            />
        );
    }
}

export default withStyles(styles)(NameField);
