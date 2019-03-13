import React, { Component } from 'react';
import ValueService from './../ValueService';
import SelectionField from './SelectionField';

export default class TemplateField extends Component {
    valueService = new ValueService();
    state = { options: [] };

    componentDidMount() {
        this.getData();
    }

    getData() {
        this.valueService.Get_Template_Field().then(response => {
            var tmp = [];
            response.map(trigger => {
                return tmp.push({ id: trigger.id, value: trigger.id, label: trigger.name });
            });
            this.setState({ options: tmp });
        });
    }

    render() {
        return <SelectionField {...this.props} value={parseInt(this.props.value)} options={this.state.options} />;
    }
}
