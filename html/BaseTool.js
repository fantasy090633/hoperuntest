function BaseTool() {
}
BaseTool.prototype = {
	ajax : function() {
		var id = arguments[0], callback = arguments[1], args = arguments[2] == undefined ? []
				: arguments[2], async = (arguments[3] == undefined ? true
				: arguments[3]), method = arguments[4] == undefined ? "POST"
				: arguments[4];
		new Ajax.Request("controller.jsp", {
			method : method,
			parameters : this.serializes(id, args),
			asynchronous : async,
			onComplete : function(response) {
				callback(eval("(" + response.responseText + ")"))
			}
		})
	},
	serializes : function() {
		var A = arguments[0], B = arguments[1], C = "";
		for ( var D = 0; D < B.length; D++)
			switch (typeof (B[D])) {
			case "string":
				C += "t" + String(D) + "=string&" + String(D) + "="
						+ encodeURIComponent(B[D]) + "&";
				break;
			case "object":
				if (B[D] instanceof Hash)
					C += "t" + String(D) + "=hash&" + String(D) + "="
							+ encodeURIComponent(B[D].toQueryString()) + "&";
				else if (B[D] instanceof Array)
					C += "t" + String(D) + "=array&" + String(D) + "="
							+ encodeURIComponent(this.array2string(B[D])) + "&";
				break;
			default:
				C += "t" + String(D) + "=string&" + String(D) + "="
						+ encodeURIComponent(B[D]) + "&";
				break
			}
		C += ("n=" + String(D) + "&id=" + A);
		return C
	},
	array2string : function() {
		var B = arguments[0], A = "";
		for ( var C = 0; C < B.length; C++)
			A += encodeURIComponent(B[C]) + "&";
		if (A.endsWith("&"))
			A = A.substring(0, A.length - 1);
		return A
	}
}