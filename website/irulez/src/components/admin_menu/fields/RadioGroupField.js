import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';
import Radio from '@material-ui/core/Radio';
import RadioGroup from '@material-ui/core/RadioGroup';
import FormHelperText from '@material-ui/core/FormHelperText';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import FormControl from '@material-ui/core/FormControl';
import FormLabel from '@material-ui/core/FormLabel';

const styles = theme => ({
    formControl: {
        margin: theme.spacing.unit,
        marginTop: theme.spacing.unit * 2
    },
    group: {
        margin: `${theme.spacing.unit}px 0`
    }
});

class RadioGroupField extends Component {
    onChange = name => event => {
        this.props.handleChange(name, event.target.value);
    };

    render() {
        const { classes, field, autoFocus, value, options, disabled } = this.props;

        return (
            <FormControl fullWidth component='fieldset' required={field.required} className={classes.formControl}>
                <FormLabel component='legend'>{field.label}</FormLabel>
                <RadioGroup
                    aria-label='Gender'
                    name='gender1'
                    row
                    className={classes.group}
                    value={parseInt(value) ? parseInt(value) : 1}
                    onChange={this.onChange(field.id)}
                >
                    {options.map(option => {
                        return <FormControlLabel value={option.value} control={<Radio />} label={option.label} />;
                    })}
                </RadioGroup>
            </FormControl>

            // <TextField
            //     id={field.id}
            //     select
            //     autoFocus={autoFocus}
            //     label={field.label}
            //     className={classNames(classes.margin, classes.textField)}
            //     value={value}
            //     disabled={disabled}
            //     onChange={this.onChange(field.id)}
            //     required={field.required}
            //     SelectProps={{
            //         native: true,
            //         MenuProps: {
            //             className: classes.menu
            //         }
            //     }}
            //     margin='normal'
            //     fullWidth
            // >
            //     {options.map(option => {
            //         return (
            //             <option key={option.id} value={option.value}>
            //                 {option.label}
            //             </option>
            //         );
            //     })}
            // </TextField>
        );
    }
}
RadioGroupField.propTypes = {
    classes: PropTypes.object.isRequired
};

export default withStyles(styles)(RadioGroupField);
