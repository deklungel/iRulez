import React, { Component } from 'react';

import Button from '@material-ui/core/Button';

import Dialog from '@material-ui/core/Dialog';
import DialogActions from '@material-ui/core/DialogActions';
import DialogContent from '@material-ui/core/DialogContent';
import DialogTitle from '@material-ui/core/DialogTitle';

import { withStyles } from '@material-ui/core/styles';

const styles = theme => ({
    textField: {
        marginLeft: theme.spacing.unit,
        marginRight: theme.spacing.unit
    },
    content: {
        overflowY: 'visible'
    }
});

class DialogMenu extends Component {
    add = () => {
        this.props.handleFormAccept();
    };
    closeForm = () => {
        this.props.handleFormCancel();
    };

    render() {
        const { classes } = this.props;

        return (
            <Dialog open={this.props.open} onClose={this.closeForm} aria-labelledby='form-dialog-title'>
                <DialogTitle id='form-dialog-title'>{this.props.title}</DialogTitle>
                <DialogContent className={classes.content}>{this.props.children}</DialogContent>
                <DialogActions>
                    <Button onClick={this.closeForm} color='primary'>
                        Cancel
                    </Button>
                    <Button onClick={this.add} color='primary'>
                        {this.props.acceptLabel}
                    </Button>
                </DialogActions>
            </Dialog>
        );
    }
}

export default withStyles(styles)(DialogMenu);
