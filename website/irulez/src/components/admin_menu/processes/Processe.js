import React, { Component } from 'react';
import { withStyles } from '@material-ui/core/styles';
import Card from '@material-ui/core/Card';
import CardActions from '@material-ui/core/CardActions';
import CardContent from '@material-ui/core/CardContent';
import Typography from '@material-ui/core/Typography';
import Grid from '@material-ui/core/Grid';
import IconButton from '@material-ui/core/IconButton';
import classNames from 'classnames';
import RestartIcon from 'mdi-react/RestartIcon';
import PlayIcon from 'mdi-react/PlayIcon';
import StopIcon from 'mdi-react/StopIcon';
import DeleteIcon from 'mdi-react/DeleteIcon';
import AlertCircleOutlineIcon from 'mdi-react/AlertCircleOutlineIcon';
import MagnifyIcon from 'mdi-react/MagnifyIcon';

const styles = {
    card: {
        minWidth: 150,
        margin: 6
    },
    bullet: {
        display: 'inline-block',
        margin: '0 2px',
        transform: 'scale(0.8)'
    },
    title: {
        fontSize: 14
    },
    pos: {
        marginBottom: 12
    },
    running: {
        borderStyle: 'solid',
        borderColor: 'green'
    },
    stopped: {
        borderStyle: 'solid',
        borderColor: 'red'
    },
    actions: {
        display: 'flex',
        justifyContent: 'space-between',
        width: '100%'
    },
    logging: {
        borderStyle: 'solid',
        borderColor: 'grey',
        borderWidth: 'thin',
        borderRadius: '25px'
    }
};

class Processe extends Component {
    calculateUptime(seconds) {
        var days = Math.floor(seconds / (3600 * 24));
        seconds -= days * 3600 * 24;
        var hrs = Math.floor(seconds / 3600);
        seconds -= hrs * 3600;
        var mnts = Math.floor(seconds / 60);
        seconds -= mnts * 60;
        return days + ' days, ' + hrs + ' Hrs, ' + mnts + ' Minutes, ' + seconds + ' Seconds';
    }
    test = () => {
        alert('Hallo');
    };
    restart = name => {
        this.props.restart_process(name);
    };
    start = name => {
        this.props.start_process(name);
    };
    stop = name => {
        this.props.stop_process(name);
    };

    clearLog = name => {
        this.props.clearLog(name);
    };

    render() {
        const { classes } = this.props;

        return (
            <Grid item lg={3} md={4} sm={6} xs={12}>
                <Card
                    className={classNames(
                        classes.card,
                        this.props.state === 'RUNNING' ? classes.running : classes.stopped
                    )}
                >
                    <CardContent>
                        <Typography className={classes.pos} variant='h5' component='h2'>
                            {this.props.name}
                        </Typography>
                        <Typography component='p'>{this.props.state}</Typography>
                        <Typography component='p'>
                            {this.props.state === 'RUNNING'
                                ? this.calculateUptime(this.props.now - this.props.start)
                                : this.calculateUptime(this.props.now - this.props.stop)}
                        </Typography>
                    </CardContent>
                    <CardActions>
                        {this.props.state === 'RUNNING' ? (
                            <div className={classes.actions}>
                                <div>
                                    <IconButton
                                        aria-label='Restart'
                                        onClick={() => {
                                            this.restart(this.props.name);
                                        }}
                                    >
                                        <RestartIcon />
                                    </IconButton>
                                    <IconButton
                                        aria-label='Stop'
                                        onClick={() => {
                                            this.stop(this.props.name);
                                        }}
                                    >
                                        <StopIcon />
                                    </IconButton>
                                </div>
                                <div className={classes.logging}>
                                    <IconButton aria-label='Error Logs' onClick={this.test}>
                                        <AlertCircleOutlineIcon />
                                    </IconButton>
                                    <IconButton aria-label='Logs' onClick={this.test}>
                                        <MagnifyIcon />
                                    </IconButton>
                                    <IconButton
                                        aria-label='Clear Logs'
                                        onClick={() => {
                                            this.clearLog(this.props.name);
                                        }}
                                    >
                                        <DeleteIcon />
                                    </IconButton>
                                </div>
                            </div>
                        ) : (
                            <div className={classes.actions}>
                                <div>
                                    <IconButton
                                        aria-label='Start'
                                        onClick={() => {
                                            this.start(this.props.name);
                                        }}
                                    >
                                        <PlayIcon />
                                    </IconButton>
                                </div>
                                <div className={classes.logging}>
                                    <IconButton aria-label='Error Logs' onClick={this.test}>
                                        <AlertCircleOutlineIcon />
                                    </IconButton>
                                    <IconButton aria-label='Logs' onClick={this.test}>
                                        <MagnifyIcon />
                                    </IconButton>
                                    <IconButton
                                        aria-label='Clear Logs'
                                        onClick={() => {
                                            this.clearLog(this.props.name);
                                        }}
                                    >
                                        <DeleteIcon />
                                    </IconButton>
                                </div>
                            </div>
                        )}
                    </CardActions>
                </Card>
            </Grid>
        );
    }
}

export default withStyles(styles)(Processe);
