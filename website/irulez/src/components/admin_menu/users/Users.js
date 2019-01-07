import React, { Component } from 'react';


import NewUser from './NewUser';
import EditUser from './EditUser';

import EnhancedTable from '../Table'

import AuthService from '../../AuthService';
import withAuth from '../../withAuth';
import withMenuList from '../../withMenuList';


const Auth = new AuthService();

class Users extends Component {

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
    Auth.fetch('http://localhost:4002/api/users').then(
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
    Auth.fetch('http://localhost:4002/api/user/delete', options).then(
      function (result) {
        this.getUsersFromBackend();
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


  render() {
    const fields = [
      { id: 'id', numeric: false, disablePadding: true, label: 'ID' },
      { id: 'email', numeric: false, disablePadding: false, label: 'Username' },
      { id: 'role', numeric: false, disablePadding: false, label: 'Role' },
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
        />
        <NewUser
          open={this.state.newForm}
          handleFormClose={this.handleFormClose}
          getUsersFromBackend={this.getUsersFromBackend} />
        <EditUser
          open={this.state.EditForm}
          handleFormClose={this.handleFormClose}
          user = {this.state.selectedUser}
          getUsersFromBackend={this.getUsersFromBackend} />
      </div>

    )
  }
}

export default withMenuList(withAuth(Users));