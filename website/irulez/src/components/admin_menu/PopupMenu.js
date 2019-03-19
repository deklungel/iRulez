import React, { Component } from 'react';

import Button from '@material-ui/core/Button';

import Dialog from '@material-ui/core/Dialog';
import DialogActions from '@material-ui/core/DialogActions';
import DialogContent from '@material-ui/core/DialogContent';
import DialogTitle from '@material-ui/core/DialogTitle';

import { withStyles } from '@material-ui/core/styles';

import Chip from '@material-ui/core/Chip';

const styles = theme => ({
    textField: {
        marginLeft: theme.spacing.unit,
        marginRight: theme.spacing.unit
    },
    content: {
        overflowY: 'visible'
    },
    chip: {
        margin: theme.spacing.unit
    }
});

class PopupMenu extends Component {
    closeForm = () => {
        this.props.handleFormClose();
    };

    render() {
        const { classes, data } = this.props;

        return (
            <Dialog open={this.props.open} onClose={this.closeForm} aria-labelledby='form-dialog-title'>
                <DialogTitle id='form-dialog-title'>{this.props.title}</DialogTitle>
                <DialogContent className={classes.content}>
                    {data.map(value => {
                        return <Chip key={value} label={value} className={classes.chip} />;
                    })}
                </DialogContent>
                <DialogActions>
                    <Button onClick={this.closeForm} color='primary'>
                        Close
                    </Button>
                </DialogActions>
            </Dialog>
        );
    }
}

export default withStyles(styles)(PopupMenu);
