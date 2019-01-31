import React, { Component } from 'react';
import SelectionField from './SelectionField';
import ValueService from './../ValueService';

class ConditionField extends Component {
    valueService = new ValueService();
    state = { options: [] };

    componentDidMount() {
        this.getData();
    }

    getData() {
        this.valueService.Get_Conditions().then(response => {
            var tmp = [];
            response.map(output => {
                return tmp.push({ id: output.id, value: output.id, label: output.name });
            });
            this.setState({ options: tmp });
        });
    }

    render() {
        return <SelectionField {...this.props} options={this.state.options} />;
    }
}

export default ConditionField;
