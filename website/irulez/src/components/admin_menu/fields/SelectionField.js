import React, { Component } from 'react';
import { withStyles } from '@material-ui/core/styles';
import InputLabel from '@material-ui/core/InputLabel';
import MenuItem from '@material-ui/core/MenuItem';
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
    onChange = name => event => {
        console.log(name + ' ' + event.target.value);
        this.props.handleChange(name, event.target.value);
    };

    render() {
        const { classes, field, value, options, disabled } = this.props;

        return (
            <FormControl fullWidth required={field.required} className={classes.formControl}>
                <InputLabel htmlFor={field.label}>{field.label}</InputLabel>
                <Select
                    value={value}
                    disabled={disabled}
                    onChange={this.onChange(field.id)}
                    inputProps={{
                        name: field.id,
                        id: field.id
                    }}
                >
                    {!field.required ? (
                        <MenuItem value=''>
                            <em>None</em>
                        </MenuItem>
                    ) : null}
                    {options.map(option => {
                        return (
                            <MenuItem key={option.id} value={option.value}>
                                {option.label}
                            </MenuItem>
                        );
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
