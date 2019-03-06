import React, { Component } from 'react';

import { withStyles } from '@material-ui/core/styles';
import Checkbox from '@material-ui/core/Checkbox';
import FormControl from '@material-ui/core/FormControl';
import FormControlLabel from '@material-ui/core/FormControlLabel';

const styles = theme => ({
    formControl: {
        margin: theme.spacing.unit,
        marginTop: theme.spacing.unit * 2
    },
    label: {
        color: 'rgba(0, 0, 0, 0.54)',
        fontSize: '1rem'
    }
});

class CheckBoxField extends Component {
    onChange = name => event => {
        this.props.handleChange(name, event.target.checked);
    };

    render() {
        const { classes, field, value } = this.props;

        return (
            <FormControl fullWidth component='fieldset' required={field.required} className={classes.formControl}>
                <FormControlLabel
                    classes={{
                        label: classes.label
                    }}
                    control={<Checkbox checked={value} onChange={this.onChange(field.id)} color='default' value='0' />}
                    label={field.label}
                />
            </FormControl>
        );
    }
}

export default withStyles(styles)(CheckBoxField);
