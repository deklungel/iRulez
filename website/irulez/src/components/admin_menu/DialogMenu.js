import React, { Component } from 'react';

import Button from '@material-ui/core/Button';

import Dialog from '@material-ui/core/Dialog';
import DialogActions from '@material-ui/core/DialogActions';
import DialogContent from '@material-ui/core/DialogContent';
import DialogTitle from '@material-ui/core/DialogTitle';

import { ValidatorForm } from 'react-material-ui-form-validator';

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
    handleSubmit = () => {
        this.props.handleFormAccept();
    };
    closeForm = () => {
        this.props.handleFormCancel();
    };

    render() {
        const { classes } = this.props;

        return (
            <Dialog
                fullScreen={this.props.fullScreen}
                open={this.props.open}
                onClose={this.closeForm}
                scroll='body'
                aria-labelledby='form-dialog-title'
            >
                <DialogTitle id='form-dialog-title'>{this.props.title}</DialogTitle>
                <ValidatorForm ref='form' onSubmit={this.handleSubmit} onError={errors => console.log(errors)}>
                    <DialogContent className={classes.content}>{this.props.children}</DialogContent>
                    <DialogActions>
                        {this.props.extraButton ? (
                            <Button onClick={this.props.extraButtonAction} color='secondary'>
                                {this.props.extraButton}
                            </Button>
                        ) : null}
                        <Button onClick={this.closeForm} color='primary'>
                            Cancel
                        </Button>
                        <Button disabled={this.props.submitDisabled} type='submit'>
                            {this.props.acceptLabel}
                        </Button>
                    </DialogActions>
                </ValidatorForm>
            </Dialog>
        );
    }
}

export default withStyles(styles)(DialogMenu);
