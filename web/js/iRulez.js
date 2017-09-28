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
	this.Validation = new function()
	{
		this.isNullOrEmpty = function(obj)
		{
			return obj == null || obj == 'undefined';
		}
	}
	this.Tool = new function()
	{
		// todo; implement fancy error boxes
		this.showErrorMessage = function(Message)
		{
			alert(Message);
		}
	}
	// Data related functions
	
	this.Data = new function ()
    {
		// This function will request a new state, by putting it on the queue
		this.triggerDeviceState = function(Mac,H,L,callback)
		{
			var x =  { Mac: Mac, H: H, L:L};
			$.ajax({
                type: "POST",
                contentType: "application/json",
				url: iRulez.apiPath("/?action=triggerdevicestate"),
                dataType: "json",
                data: JSON.stringify(x),
                success: function (success) {
                    if (iRulez.Validation.isNullOrEmpty(callback)) return successs;
                    else callback(success);
                },
                error: function (xhr, status, error) {
                    iRulez.Tool.showErrorMessage(xhr.responseJSON.ExceptionMessage, function () {
                        if (iRulez.Validation.isNullOrEmpty(callback)) return false;
                        else callback(false);
                    });
                }
            });
		}
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