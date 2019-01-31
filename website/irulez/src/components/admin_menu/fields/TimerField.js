import React, { Component } from 'react';
import SecondsField from './SecondsField';

class TimerField extends Component {
    onChange = name => event => {
        this.props.handleChange(name, event.target.value);
    };

    render() {
        const { dependency } = this.props;

        return (
            <SecondsField {...this.props} disabled={parseInt(dependency) === 1 || dependency === '' ? true : false} />
        );
    }
}

export default TimerField;
