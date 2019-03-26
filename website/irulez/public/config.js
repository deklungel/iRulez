var BASEURL = 'http://10.0.50.250:3001/api/';
var BASEURL_SUPERVISOR = 'http://10.0.50.250:3003/api/';

var PYTHON_SERVER = 'http://10.0.50.250:3004/api/';

var AUTHENTICATION_SERVER = PYTHON_SERVER + 'login';
var AUTHENTICATION_SERVER_REFRESH = PYTHON_SERVER + 'refresh_login';

var USER_DELETE = PYTHON_SERVER + 'users';
var USER_GET = PYTHON_SERVER + 'users';
var USER_EDIT = PYTHON_SERVER + 'users';
var USER_CHANGE_PASSWORD = PYTHON_SERVER + 'users';
var USER_ADD = PYTHON_SERVER + 'users';

var GROUP_DELETE = PYTHON_SERVER + 'groups';
var GROUP_GET = PYTHON_SERVER + 'groups';
var GROUP_EDIT = PYTHON_SERVER + 'groups';
var GROUP_ADD = PYTHON_SERVER + 'groups';

var DEVICE_GET = PYTHON_SERVER + 'devices';
var DEVICE_ADD = PYTHON_SERVER + 'devices';
var DEVICE_DELETE = PYTHON_SERVER + 'devices';
var DEVICE_EDIT = PYTHON_SERVER + 'devices';

var OUTPUT_GET = PYTHON_SERVER + 'outputs';
var OUTPUT_EDIT = PYTHON_SERVER + 'outputs';

var MENU_GET = PYTHON_SERVER + 'menus';
var MENU_ADD = PYTHON_SERVER + 'menus';
var MENU_DELETE = PYTHON_SERVER + 'menus';
var MENU_EDIT = PYTHON_SERVER + 'menus';

var INPUT_GET = PYTHON_SERVER + 'inputs';
var INPUT_EDIT = PYTHON_SERVER + 'inputs';

var ACTION_GET = PYTHON_SERVER + 'actions/relais';
var ACTION_ADD = PYTHON_SERVER + 'actions/relais';
var ACTION_DELETE = PYTHON_SERVER + 'actions/relais';
var ACTION_EDIT = PYTHON_SERVER + 'actions/relais';

var DIMMER_ACTIONS_GET = PYTHON_SERVER + 'actions/dimmers';

var GET_FIELD_TRIGGERS = PYTHON_SERVER + 'field/triggers';
var GET_FIELD_GROUPS = PYTHON_SERVER + 'field/groups';
var GET_FIELD_ACTION_TYPES = PYTHON_SERVER + 'field/action_types_relais';
var GET_OUTPUTS = PYTHON_SERVER + 'field/outputs';
var GET_CONDITIONS = PYTHON_SERVER + 'field/conditions';
var GET_NOTIFICATIONS = PYTHON_SERVER + 'field/notifications';
var GET_FIELD_TEMPLATE = PYTHON_SERVER + 'field/templates';
var GET_FIELD_ACTIONS = PYTHON_SERVER + 'field/actions';
var GET_FIELD_MENUS = PYTHON_SERVER + 'field/menus';
var GET_FIELD_OUTPUTTYPE = PYTHON_SERVER + 'field/output_type';

var PROCESSES_GET = PYTHON_SERVER + 'supervisor';
var PROCESSES_RESTART = PYTHON_SERVER + 'supervisor/restart';
var PROCESSES_START = PYTHON_SERVER + 'supervisor/start';
var PROCESSES_STOP = PYTHON_SERVER + 'supervisor/stop';
var CLEAR_LOG = PYTHON_SERVER + 'clearLogs';
