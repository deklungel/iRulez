var iRulez = new function ()
{
	var _HOST_VARIABLE = "";	
	this.apiPath = function (path) {
		if (_HOST_VARIABLE.length <= 0)
		{
			_HOST_VARIABLE == location.protocol + '//' + location.hostname + (location.port ? ':' + location.port : '');
		}
		return _HOST_VARIABLE + "/api" + path;
    }
	// this function is intended to be extended for logging or tracing to another target over Ajax
	this.Log = function(Tag, Message)
	{
		console.log("[" + Tag + "] " + Message); // Write it to the console for now (F12 in your browser)
	}
	
	// Data related functions
	
	this.Data = new function ()
    {
        this.getDevices = function(callback)
        {
            $.ajax({
                type: "GET",
                contentType: "application/json",
                url: iRulez.apiPath("/?action=getdevices"),
                success: function (data) {
                    callback(data);
                },
                error: function (xhr, status, error) {
                    callback("ERROR");
                }
            });
        }
		this.getDevice = function(mac, callback)
		{
            $.ajax({
                type: "GET",
                contentType: "application/json",
                url: iRulez.apiPath("/?action=getdevice&mac="+mac),
                success: function (data) {
                    callback(data);
                },
                error: function (xhr, status, error) {
                    callback("ERROR");
                }
            });
		}
	}
}