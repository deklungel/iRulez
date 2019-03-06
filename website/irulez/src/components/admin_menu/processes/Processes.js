import React, { Component } from 'react';
import Processe from './Processe';
import ProcessService from './ProcessService';
import Grid from '@material-ui/core/Grid';

class Processes extends Component {
    ProcessService = new ProcessService();
    state = {
        data: []
    };

    componentDidMount() {
        //this.props.checkSidebarState();
        this.getData();
    }
    getData = () => {
        this.ProcessService.getData().then(response => {
            this.setState({ data: response });
        });
    };

    restartProcess = name => {
        this.ProcessService.restartProcess(name).then(status => {
            this.getData();
        });
    };
    startProcess = name => {
        this.ProcessService.startProcess(name).then(status => {
            this.getData();
        });
    };
    stopProcess = name => {
        this.ProcessService.stopProcess(name).then(status => {
            this.getData();
        });
    };
    clearLog = name => {
        this.ProcessService.clearLog(name).then(status => {
            this.getData();
        });
    };
    render() {
        return (
            <Grid container spacing={16} direction='row' justify='flex-start' alignItems='center'>
                {this.state.data.map(process => {
                    return (
                        <Processe
                            name={process.name}
                            state={process.statename}
                            now={process.now}
                            start={process.start}
                            stop={process.stop}
                            restart_process={this.restartProcess}
                            start_process={this.startProcess}
                            stop_process={this.stopProcess}
                            clearLog={this.clearLog}
                        />
                    );
                })}
            </Grid>
        );
    }
}

export default Processes;
