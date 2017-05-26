"use strict";
angular.module("empatica")
	.controller('statsCountryController', ["$scope", "$log", "dataService", function($scope, $log, dataService) {
		let vm = this;
		vm.scope = $scope;
		vm.scope.options = {
			chart: {
				type: 'pieChart',
				height: 500,
				donut: true,
				x: function(d) {
					return d.loc_short;
				},
				y: function(d) {
					return d3.format(',f')(d.tot);
				},
				showLabels: true,
				duration: 500,
				showLegend: false,
				tooltip: {
					contentGenerator: function(d) {
						return `<p style="color:${d.color}"><b>${d.data.loc_long}</b></p>
           					<p><em><b>${d.data.tot}</b</em></p>`;
					}
				}
			},
			title: {
				enable: true,
				text: "Where is the empatica app downloaded mostly?",
			}
		};

		dataService.getStatsByCountry().then(function(data) {
			if (data.status === "OK") {
				vm.scope.data = data.results;
				$log.log("data acquired!");
			} else {
				$log.error("Ops, something bad happened.");
			}
		});
	}]);
