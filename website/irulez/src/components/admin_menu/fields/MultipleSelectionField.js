import React, { Component } from 'react';

import classNames from 'classnames';

import { withStyles } from '@material-ui/core/styles';
import Input from '@material-ui/core/Input';
import InputLabel from '@material-ui/core/InputLabel';
import MenuItem from '@material-ui/core/MenuItem';
import FormControl from '@material-ui/core/FormControl';
import Select from '@material-ui/core/Select';
import Chip from '@material-ui/core/Chip';

const styles = theme => ({
    textField: {
        margin: theme.spacing.unit
    },
    content: {
        overflowY: 'visible'
    },
    chips: {
        display: 'flex',
        flexWrap: 'wrap'
    }
});

const ITEM_HEIGHT = 48;
const ITEM_PADDING_TOP = 8;
const MenuProps = {
    PaperProps: {
        style: {
            maxHeight: ITEM_HEIGHT * 4.5 + ITEM_PADDING_TOP,
            width: 250
        }
    }
};

class MultipleSelectionField extends Component {
    onChange = name => event => {
        this.props.handleChange(name, event.target.value);
    };

    render() {
        const { classes, field, autoFocus, disabled, options, labelField } = this.props;

        return (
            <FormControl fullWidth className={classNames(classes.margin, classes.textField)}>
                <InputLabel htmlFor='select-multiple-chip'>{field.label}</InputLabel>
                <Select
                    required={field.required}
                    autoFocus={autoFocus}
                    fullWidth
                    type='number'
                    id={field.id}
                    name={field.id}
                    value={this.props.value}
                    onChange={this.onChange(field.id)}
                    label={field.label}
                    disabled={disabled}
                    multiple
                    input={<Input id='select-multiple-chip' />}
                    renderValue={selected => (
                        <div className={classes.chips}>
                            {selected.map(value => (
                                <Chip
                                    key={value}
                                    label={options.length === 0 ? labelField[value] : options[value].label}
                                    className={classes.chip}
                                />
                            ))}
                        </div>
                    )}
                    MenuProps={MenuProps}
                >
                    {options.map(option => (
                        <MenuItem key={option.id} value={option.value}>
                            {option.label}
                        </MenuItem>
                    ))}
                </Select>
            </FormControl>
        );
    }
}

export default withStyles(styles)(MultipleSelectionField);
