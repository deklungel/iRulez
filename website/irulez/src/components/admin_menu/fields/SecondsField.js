import React, { Component } from 'react';
import NumberField from './NumberField';
import InputAdornment from '@material-ui/core/InputAdornment';

class SecondsField extends Component {
    onChange = name => event => {
        this.props.handleChange(name, event.target.value);
    };

    render() {
        return (
            <NumberField
                {...this.props}
                InputProps={{
                    endAdornment: (
                        <InputAdornment variant='filled' position='end'>
                            Seconds
                        </InputAdornment>
                    )
                }}
            />
        );
    }
}

export default SecondsField;
