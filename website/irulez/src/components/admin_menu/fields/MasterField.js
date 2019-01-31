import React, { Component } from 'react';
import SelectionField from './SelectionField';
import ValueService from '../ValueService';

class MasterField extends Component {
    valueService = new ValueService();
    state = { options: [] };

    componentDidMount() {
        this.getData();
    }

    getData() {
        this.valueService.Get_Outputs().then(response => {
            var tmp = [];
            response.map(output => {
                return tmp.push({ id: output.id, value: output.id, label: output.name });
            });
            this.setState({ options: tmp });
        });
    }

    render() {
        const { dependency } = this.props;

        return (
            <SelectionField
                {...this.props}
                options={this.state.options}
                disabled={dependency && (parseInt(dependency) !== 1 || dependency === '') ? true : false}
            />
        );
    }
}

export default MasterField;
