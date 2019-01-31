import React, { Component } from 'react';
import MultipleSelectionField from './MultipleSelectionField';
import ValueService from './../ValueService';

class MultipleNotificationField extends Component {
    valueService = new ValueService();
    state = { options: [] };

    componentDidMount() {
        this.getData();
    }

    getData() {
        this.valueService.Get_Notifications().then(response => {
            var tmp = [];
            response.map(output => {
                return (tmp[output.id] = { id: output.id, value: output.id, label: output.name });
            });
            this.setState({ options: tmp });
        });
    }

    render() {
        return <MultipleSelectionField {...this.props} options={this.state.options} />;
    }
}

export default MultipleNotificationField;
