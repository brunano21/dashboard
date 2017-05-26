angular.module("empatica")
	.controller("mapController", ["$scope", "$log", "NgMap", "socketio", "dataService", function($scope, $log, NgMap, socketio, dataService) {
		let vm = this;
		vm.dynMarkers = [];
		vm.scope = $scope;
		socketio.forward('data', $scope);
		vm.numDonwloads = 0;

		$scope.$on("sio:data", function(ev, data) {
			let latLng = new google.maps.LatLng(data.payload.lat, data.payload.lng);
			let marker = new google.maps.Marker({
				position: latLng
			});
			vm.markerClusterer.addMarkers([marker]);
			vm.map.panTo(latLng);
			vm.numDonwloads++;
			$log.info("Added ", data.payload);
		});

		$scope.$on("sio:error", function(ev, data) {
			$log.log(ev, data);
		});

		NgMap.getMap().then(function(map) {
			vm.map = map;
			dataService.getAllDownloads().then(function(data) {
				if (data.status === "OK") {
					for (let i = 0; i < data.results.length; i++) {
						let latLng = new google.maps.LatLng(data.results[i].lat, data.results[i].lng);
						vm.dynMarkers.push(new google.maps.Marker({
							position: latLng
						}));
					}
					vm.markerClusterer = new MarkerClusterer(map, vm.dynMarkers, {});
					vm.numDonwloads = data.results.length;
					$log.log(data.results.length + " markers loaded!");
				} else {
					$log.error("Ops, something bad happened.");
				}

			});

		});
	}])
