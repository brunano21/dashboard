"use strict";
angular.module("empatica")
	.controller('statsHistoryController', ["$scope", "$log", "dataService", function($scope, $log, dataService) {
		let vm = this;
		vm.scope = $scope;
		vm.scope.options = {
			chart: {
				type: 'historicalBarChart',
				height: 450,
				margin: {
					top: 20,
					right: 20,
					bottom: 65,
					left: 50
				},
				x: function(d) {
					return d.downloaded_at;
				},
				y: function(d) {
					return d.num;
				},
				showValues: true,
				valueFormat: function(d) {
					return d3.format(',.1f')(d);
				},
				duration: 100,
				xAxis: {
					axisLabel: 'Days',
					tickFormat: function(d) {
						return d3.time.format('%x')(new Date(d))
					},
					rotateLabels: 30,
					showMaxMin: false
				},
				yAxis: {
					axisLabel: '# downloads',
					axisLabelDistance: -10,
					tickFormat: function(d) {
						return d3.format(',.1f')(d);
					}
				},
				tooltip: {
					keyFormatter: function(d) {
						return d3.time.format('%x')(new Date(d));
					}
				},
				zoom: {
					enabled: true,
					scaleExtent: [1, 10],
					useFixedDomain: false,
					useNiceScale: false,
					horizontalOff: false,
					verticalOff: true,
					unzoomEventType: 'dblclick.zoom'
				}
			}
		};

		dataService.getHistory().then(function(data) {
			if (data.status === "OK") {
				vm.scope.data = [{
					key: "data",
					bar: true,
					values: data.results
				}];
				$log.log("data acquired!");
			} else {
				$log.error("Ops, something bad happened.");
			}
		});
	}]);
