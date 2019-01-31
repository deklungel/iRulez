import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';
import Input from '@material-ui/core/Input';
import OutlinedInput from '@material-ui/core/OutlinedInput';
import FilledInput from '@material-ui/core/FilledInput';
import InputLabel from '@material-ui/core/InputLabel';
import MenuItem from '@material-ui/core/MenuItem';
import FormHelperText from '@material-ui/core/FormHelperText';
import FormControl from '@material-ui/core/FormControl';
import Select from '@material-ui/core/Select';

const styles = theme => ({
    formControl: {
        margin: theme.spacing.unit
    },
    content: {
        overflowY: 'visible'
    }
});

class SelectionField extends Component {
    componentDidMount() {
        this.props.handleChange(this.props.id, parseInt(this.props.id));
    }
    onChange = name => event => {
        this.props.handleChange(name, parseInt(event.target.value));
    };

    render() {
        const { classes, field, autoFocus, value, options, disabled } = this.props;

        return (
            <FormControl fullWidth required={field.required} className={classes.formControl}>
                <InputLabel htmlFor={field.label}>{field.label}</InputLabel>
                <Select
                    value={value}
                    disabled={disabled}
                    onChange={this.onChange(field.id)}
                    inputProps={{
                        name: field.label,
                        id: field.label
                    }}
                >
                    {!field.required ? (
                        <MenuItem value=''>
                            <em>None</em>
                        </MenuItem>
                    ) : null}
                    {options.map(option => {
                        return <MenuItem value={option.value}>{option.label}</MenuItem>;
                    })}
                </Select>
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

export default withStyles(styles)(SelectionField);
