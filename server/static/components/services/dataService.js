"use strict";
angular.module("empatica")
	.service('dataService', ['$resource', "$location", function($resource, $location) {

		this.getAllDownloads = function () {
			return $resource("/getAllDownloads").get().$promise;
		};

		this.getStatsByCountry = function () {
			return $resource("stats/byCountry").get().$promise;
		};

		this.getStatsByTime = function () {
			return $resource("stats/byTime").get().$promise;
		};

		this.getHistory = function () {
			return $resource("stats/history").get().$promise;
		};
	}]);
