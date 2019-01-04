import React, {Component} from 'react';


import NewUser from './NewUser';
import EnhancedTable from '../Table'



class Users extends Component {
  state = {
    newUsersFormOpen: false,
  };

  render() {
    return (
      <div>
        <EnhancedTable />
        <NewUser open={this.state.newUsersFormOpen} handleUserFormClose={this.handleUserFormClose} getUsersFromBackend={this.getUsersFromBackend} />
      </div>

    )
  }
}

export default Users;