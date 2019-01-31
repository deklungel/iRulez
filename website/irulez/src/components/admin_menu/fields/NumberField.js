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

class NumberField extends Component {
    onChange = name => event => {
        this.props.handleChange(name, event.target.value);
    };

    render() {
        const { classes, field, autoFocus, disabled, InputProps } = this.props;

        return (
            <TextField
                fullWidth
                required={field.required}
                autoFocus={autoFocus}
                type='number'
                inputProps={{ min: '0' }}
                // eslint-disable-next-line
                InputProps={InputProps}
                className={classNames(classes.margin, classes.textField)}
                id={field.id}
                name={field.id}
                value={this.props.value}
                onChange={this.onChange(field.id)}
                label={field.label}
                disabled={disabled}
            />
        );
    }
}

export default withStyles(styles)(NumberField);
