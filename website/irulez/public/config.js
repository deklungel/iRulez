var BASEURL = 'http://10.0.50.250:3001/api/';
var BASEURL_SUPERVISOR = 'http://10.0.50.250:3003/api/';
var AUTHENTICATION_SERVER = 'http://10.0.50.250:3002/login';

var USER_DELETE = BASEURL + 'user/delete';
var USER_GET = BASEURL + 'users';
var USER_EDIT = BASEURL + 'user/edit';
var USER_CHANGE_PASSWORD = BASEURL + 'user/changepassword';
var USER_ADD = BASEURL + 'user/add';

var GROUP_DELETE = BASEURL + 'group/delete';
var GROUP_GET = BASEURL + 'groups';
var GROUP_EDIT = BASEURL + 'group/edit';
var GROUP_ADD = BASEURL + 'group/add';

var DEVICE_GET = BASEURL + 'devices';
var DEVICE_ADD = BASEURL + 'device/add';
var DEVICE_DELETE = BASEURL + 'device/delete';
var DEVICE_EDIT = BASEURL + 'device/edit';

var OUTPUT_GET = BASEURL + 'outputs';
var OUTPUT_EDIT = BASEURL + 'output/edit';

var INPUT_GET = BASEURL + 'inputs';
var INPUT_EDIT = BASEURL + 'input/edit';

var ACTION_GET = BASEURL + 'actions';
var ACTION_ADD = BASEURL + 'action/add';
var ACTION_DELETE = BASEURL + 'action/delete';
var ACTION_EDIT = BASEURL + 'action/edit';

var DIMMER_ACTIONS_GET = BASEURL + 'dimmeractions';

var GET_FIELD_TRIGGERS = BASEURL + 'field/triggers';
var GET_FIELD_GROUPS = BASEURL + 'field/groups';
var GET_FIELD_ACTION_TYPES = BASEURL + 'field/action_types';
var GET_OUTPUTS = BASEURL + 'field/outputs';
var GET_CONDITIONS = BASEURL + 'field/conditions';
var GET_NOTIFICATIONS = BASEURL + 'field/notifications';
var GET_FIELD_TEMPLATE = BASEURL + 'field/templates';
var GET_FIELD_ACTIONS = BASEURL + 'field/actions';

var PROCESSES_GET = BASEURL_SUPERVISOR + 'getAllProcesses';
var PROCESSES_RESTART = BASEURL_SUPERVISOR + 'restartProcces';
var PROCESSES_START = BASEURL_SUPERVISOR + 'startProcces';
var PROCESSES_STOP = BASEURL_SUPERVISOR + 'stopProcces';
var CLEAR_LOG = BASEURL_SUPERVISOR + 'clearLogs';
