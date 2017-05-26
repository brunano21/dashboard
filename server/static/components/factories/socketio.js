"use strict";
angular
	.module("empatica")
	.factory("socketio", function(socketFactory, $location) {
		let webSocket = socketFactory({
			prefix: "sio:",
			ioSocket: io.connect($location.path() + "/sio")
		});
		webSocket.forward("error");
		return webSocket;
	});
