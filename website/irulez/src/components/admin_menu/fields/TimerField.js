import React, { Component } from 'react';
import SecondsField from './SecondsField';

class TimerField extends Component {
    render() {
        const { dependency } = this.props;

        return (
            <SecondsField
                {...this.props}
                disabled={parseInt(dependency) === 1 || dependency === '' ? true : false}
                value={parseInt(dependency) === 1 || dependency === '' ? 0 : this.props.value}
            />
        );
    }
}

export default TimerField;
