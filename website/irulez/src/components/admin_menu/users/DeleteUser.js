import React, { Component } from 'react';

import Button from '@material-ui/core/Button';
import DialogContentText from '@material-ui/core/DialogContentText';
import Dialog from '@material-ui/core/Dialog';
import DialogActions from '@material-ui/core/DialogActions';
import DialogContent from '@material-ui/core/DialogContent';
import DialogTitle from '@material-ui/core/DialogTitle';
import { withStyles } from '@material-ui/core/styles';

const styles = theme => ({
    textField: {
        marginLeft: theme.spacing.unit,
        marginRight: theme.spacing.unit,
    },
    content:{
        overflowY: "visible"
    }
});

class DeleteUser extends Component {

    DeleteUser = () => {
        var options = {
          'method': 'DELETE',
          'body': JSON.stringify({ id: this.props.selected })
        }
        this.prop.Auth.fetch(window.USER_DELETE, options).then(
          function (result) {
            this.props.getUsersFromBackend();
            this.props.notification("User has been deleted", 'warning')
            this.closeForm()
          }.bind(this)
        ).catch(err => {
          alert(err);
        })
    
      }

    closeForm = () => {
        this.props.handleFormClose("DeleteForm");
    }

    render() {
        return (
            <Dialog
            open={this.props.open}
            onClose={this.closeForm}
            aria-labelledby="alert-dialog-title"
            aria-describedby="alert-dialog-description"
          >
            <DialogTitle id="alert-dialog-title">{"Delete this user"}</DialogTitle>
            <DialogContent>
              <DialogContentText id="alert-dialog-description">
                Are you sure you want to delete this user?
              </DialogContentText>
            </DialogContent>
            <DialogActions>
              <Button onClick={this.closeForm} color="primary">
                Cancel
              </Button>
              <Button onClick={this.DeleteUser} color="primary" autoFocus>
                Delete
              </Button>
            </DialogActions>
          </Dialog>
        )
    }

}

export default withStyles(styles)(DeleteUser);