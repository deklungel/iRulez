from xmlrpc.client import ServerProxy
from flask import jsonify


class SupervisorClient(object):
    """ Supervisor client to work with remote supervisor
    """

    def __init__(self, host='localhost', port=9001):
        self.server = ServerProxy('http://{}:{}/RPC2'.format(host, port))

    def _generate_correct_process_name(self, process):
        return "{}:1".format(process)

    def start(self, request):
        """ Start process
        """
        data = request.get_json()

        if self.server.supervisor.startProcess(data['process']):
            return jsonify({'response': 'success'})
        else:
            return jsonify({"message": "Process not started"}), 501

    def stop(self, request):
        """ Stop process
        """
        data = request.get_json()

        if self.server.supervisor.stopProcess(data['process']):
            return jsonify({'response': 'success'})
        else:
            return jsonify({"message": "Process not stopped"}), 501

    def restart(self, request):
        """ Stop process
        """
        data = request.get_json()

        if self.server.supervisor.stopProcess(data['process']):
            if self.server.supervisor.startProcess(data['process']):
                return jsonify({'response': 'success'})
            return jsonify({"message": "Process not started"}), 501
        return jsonify({"message": "Process not stopped"}), 501


    def get_all_process(self):
        output = []
        for process in self.server.supervisor.getAllProcessInfo():
            output.append({'name': process['name'],
                        'statename': process['statename'],
                        'start': process['start'],
                        'stop': process['stop'],
                        'now': process['now']})
        return jsonify({'response': output})

