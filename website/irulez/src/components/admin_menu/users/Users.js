import React, { Component } from 'react';


import NewUser from './NewUser';
import EditUser from './EditUser';

import EnhancedTable from '../Table'

import withAuth from '../../withAuth';

import PropTypes from 'prop-types';
import { SnackbarProvider, withSnackbar } from 'notistack';

import SideBar from '../../SideBar';

class Users extends Component {

  Auth = this.props.Auth;

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
        this.setState({ data: result.users })
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
      <SideBar Auth={this.Auth} open="users">
        <EnhancedTable
          data={this.state.data}
          fields={fields}
          selected={this.state.selected}
          handleFormOpen={this.handleFormOpen}
          handleDelete={this.handleDelete}
          updatedSelected={this.updatedSelected}
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
      </SideBar>

    )
  }
}
Users.propTypes = {
  enqueueSnackbar: PropTypes.func.isRequired,
};

const MyApp = withAuth(withSnackbar(Users));

function IntegrationNotistack() {
  return (
    <SnackbarProvider maxSnack={3}>
      <MyApp />
    </SnackbarProvider>
  );
}

export default IntegrationNotistack;