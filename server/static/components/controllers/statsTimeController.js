"use strict";
angular.module("empatica")
	.controller('statsTimeController', ["$scope", "$log", "dataService", function($scope, $log, dataService) {
		let vm = this;
		vm.scope = $scope;
		vm.scope.options = {
			chart: {
				type: 'discreteBarChart',
				height: 450,
				margin: {
					top: 20,
					right: 20,
					bottom: 50,
					left: 55
				},
				x: function(d) {
					return d.AmPmTime;
				},
				y: function(d) {
					return d.tot;
				},
				showValues: true,
				duration: 500,
				xAxis: {
					axisLabel: 'Period of the day'
				},
				yAxis: {
					axisLabel: 'Total downloads',
					axisLabelDistance: -10
				}
			},
			title: {
				enable: true,
				text: "When the empatica app is usually downloaded?",
				className: "h4"
			}
		};


		dataService.getStatsByTime().then(function(data) {
			if (data.status === "OK") {
				vm.scope.data = [{
					key: "data",
					values: data.results
				}];
				$log.log("data acquired!");
			} else {
				$log.error("Ops, something bad happened.");
			}
		});
	}]);
