import React, { Component } from 'react';
import NewUser from '../users/NewUser';
import EditUser from '../users/EditUser';
import EnhancedTable from '../Table'
import PropTypes from 'prop-types';
import {withSnackbar } from 'notistack';
import AuthService from '../../AuthService';

class Devices extends Component {
  constructor(props) {
    super(props);
    this.props.Collapse("devices")
}
Auth = new AuthService();

  state = {
    newForm: false,
    EditForm: false,
    data: [],
    selected: [],
    selectedUser: [],
  };

  componentDidMount() {
    this.getUsersFromBackend();
  }

  getUsersFromBackend = () => {
    this.Auth.fetch('http://localhost:4002/api/users').then(
      function (result) {
        this.setState({ data: result.response })
      }.bind(this)
    )
    this.setState({ selected: [] });
  }

  handleDelete = () => {
    var options = {
      'method': 'POST',
      'body': JSON.stringify({ id: this.state.selected })
    }
    this.Auth.fetch('http://localhost:4002/api/user/delete', options).then(
      function (result) {
        this.getUsersFromBackend();
        this.handleNotification("User has been deleted", 'warning')
      }.bind(this)
    )

  }

  handleFormOpen = form => {
    this.setState({
      [form]: true,
    });
  };

  handleFormClose = form => {
    this.setState({
      [form]: false,
    });
  };
  updatedSelected = (value, row) => {
    this.setState({ selected: value });
    if (value.length === 1){
      this.setState({ selectedUser: row[value] });
    }   
  }
  handleNotification = (message, variant) => {
    // variant could be success, error, warning or info
    this.props.enqueueSnackbar(message, { variant });
  };

  render() {
    const fields = [
      { id: 'id', align: 'left', disablePadding: true, label: 'ID' },
      { id: 'email', align: 'left', disablePadding: false, label: 'Username' },
      { id: 'role', align: 'left', disablePadding: false, label: 'Role' },
    ];

    return (
      <div>
        <EnhancedTable
          data={this.state.data}
          fields={fields}
          selected={this.state.selected}
          handleFormOpen={this.handleFormOpen}
          handleDelete={this.handleDelete}
          updatedSelected={this.updatedSelected}
          title="Devices"
          rowsPerPage={10}
        />
        <NewUser
          open={this.state.newForm}
          Auth={this.Auth}
          handleFormClose={this.handleFormClose}
          getUsersFromBackend={this.getUsersFromBackend} 
          notification = {this.handleNotification}
        />
        <EditUser
          open={this.state.EditForm}
          Auth={this.Auth}
          handleFormClose={this.handleFormClose}
          user = {this.state.selectedUser}
          getUsersFromBackend={this.getUsersFromBackend}
          notification = {this.handleNotification} />
      </div>

    )
  }
}
Devices.propTypes = {
  enqueueSnackbar: PropTypes.func.isRequired,
};

export default withSnackbar(Devices);