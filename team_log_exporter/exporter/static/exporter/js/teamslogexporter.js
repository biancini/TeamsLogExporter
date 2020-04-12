var app = angular.module('teamsLogExporter', []);

$("#error-message").hide();

app.config(['$interpolateProvider', function($interpolateProvider) {
    $interpolateProvider.startSymbol('{a');
    $interpolateProvider.endSymbol('a}');
}]);

app.filter('search', function() {
    return function(list, field, partialString) {
        if (!angular.isString(partialString) || partialString.length == 0) return list;

        var results = [];
        angular.forEach(list, function(item) {
            if (angular.isString(item[field])) {
                if (item[field].search(new RegExp(partialString, "i")) > -1) {
                     results.push(item);
                }
            }
        });

        return results;
    }

});

app.controller('mainController', ['$scope', '$http', function($scope, $http) {
    $scope.setupOk = false;
    $scope.errorMessage = '';
    $scope.step1 = '';
    $scope.step2 = '';
    $scope.step3 = '';
    $scope.step4 = '';

    $scope.startFlow = function() {
        var token = $scope.bearerToken;
        
        $scope.grouplist = []
        $http.post("/exporter/bearer", { token: token }).then(function successCallback(response) {
            $scope.setupOk = true;
            $scope.step1 = 'active';
            
            $scope.grouplist = response.data.data;
        }, function errorCallback(response) {
            console.log("Errore: " + JSON.stringify({data: response}));
        });
    };

    $scope.nextFlow = function() {
        if ($scope.step1 == 'active') {
            var selectedGroups = [];
            $('#group-selection :checked').each(function() {
                selectedGroups.push($(this).val());
            });
            
            $scope.userlist = []
            $http.post("/exporter/getusers_bygroup", { groups: selectedGroups }).then(function successCallback(response) {
                $scope.step1 = 'completed'
                $scope.step2 = 'active';
                
                $scope.userlist = response.data.data;
            }, function errorCallback(response) {
                console.log("Errore: " + JSON.stringify({data: response}));
            });

            return;
        }

        if ($scope.step2 == 'active') {
            var selectedUsers = [];
            $('#user-selection :checked').each(function() {
                selectedUsers.push($(this).val());
            });

            if (selectedUsers.length == 0) {
                $scope.errorMessage = "Devi selezionare almeno un utente.";
                $("#error-message").show();
                $("#error-message").delay(4000).slideUp(200, function() {
                    $(this).hide();
                });
                return;
            }
            
            $scope.userlist = []
            $http.post("/exporter/getuser_meetings", { users: selectedUsers }).then(function successCallback(response) {
                $scope.step2 = 'completed'
                $scope.step3 = 'active';

                var options = {'weekday': 'long', 'year': 'numeric', 'month': 'long', 'day': '2-digit'};
                
                $scope.eventlist = response.data.data;
                $scope.eventlist.forEach(function (item) {
                    var durata = Math.floor((new Date(item['end'])) - (new Date(item['start']))) / (1000*60);
                    var hours = Math.floor(durata / 60);  
                    var minutes = Math.floor(durata % 60);
                    
                    item['durata'] = hours + " ore e " + minutes + "minuti";
                    item['start'] = new Date(item['start']).toLocaleTimeString('it-IT', options);
                    item['end'] = new Date(item['end']).toLocaleTimeString('it-IT', options);                    
                });
            }, function errorCallback(response) {
                console.log("Errore: " + JSON.stringify({data: response}));
            });

            return;
        }

        if ($scope.step3 == 'active') {
            var selectedEvents = [];
            $('#event-selection :checked').each(function() {
                selectedEvents.push($(this).val());
            });

            if (selectedEvents.length == 0) {
                $scope.errorMessage = "Devi selezionare almeno una riunione.";
                $("#error-message").show();
                $("#error-message").delay(4000).slideUp(200, function() {
                    $(this).hide();
                });
                return;
            }
            
            $scope.userlist = []
            $http.post("/exporter/getmeeting_records", { meetings: selectedEvents }).then(function successCallback(response) {
                $scope.step3 = 'completed';
                $scope.step4 = 'active';

                $scope.meetingRecords = response.data.data;
                $scope.meetingRecords.forEach(function (item) {
                    var description = item['id'];
                    $scope.eventlist.forEach(function (ev) {
                        if (ev['id'] == description) {
                            description = "Lezione di " + ev.start + ", durata " + ev.durata + " (" + ev.partecipant +" partecipanti)";
                        }
                    });
                    item['descr'] = description;
                });
            }, function errorCallback(response) {
                console.log("Errore: " + JSON.stringify({data: response}));
            });

            return;
        }
    };

    $scope.prevFlow = function() {
        if ($scope.step2 = 'active') {
            $scope.step1 = 'active'
            $scope.step2 = 'suspended'
        }

        if ($scope.step3 = 'active') {
            $scope.step2 = 'active'
            $scope.step3 = 'suspended'
        }

        if ($scope.step4 = 'active') {
            $scope.step3 = 'active'
            $scope.step4 = 'suspended'
        }
    };
}]);