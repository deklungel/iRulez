import React, { Component } from 'react';
import MultipleSelectionField from './MultipleSelectionField';
import ValueService from './../ValueService';

class MultipleOutputField extends Component {
    valueService = new ValueService();
    state = { options: [] };

    componentDidMount() {
        this.getData();
    }

    getData() {
        this.valueService.Get_Outputs().then(response => {
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

export default MultipleOutputField;
