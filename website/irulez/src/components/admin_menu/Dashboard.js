import React, { Component } from 'react';
import './Dashboard.css';



import AuthService from '../AuthService';
import withMenuList from '../withMenuList';
import withAuth from '../withAuth';

const Auth = new AuthService();

class Admin extends Component {
    constructor(props) {
        super(props);
        this.handleLogout = this.handleLogout.bind(this);
    }
    componentWillMount(){
        if (this.props.user.role !=="admin"){
         this.props.history.replace('/');
        }
     }
     handleLogout(){
        Auth.logout()
        this.props.history.replace('/login');
     }

  render() {
      return(
        <div className="Admin">
            <div className="App-header">
                <h2>Welcome Admin {this.props.user.username}</h2>
                {/* <Users></Users> */}
            </div>
            <p className="App-intro">
                <button type="button" className="form-submit" onClick={this.handleLogout.bind(this)}>Logout</button>
            </p>
            </div>
    )
    ;
  }
}

 export default withAuth(withMenuList(Admin));
