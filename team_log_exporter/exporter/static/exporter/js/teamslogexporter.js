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

    $scope.startFlow = function() {
        $('#flowDimmer').dimmerShow();

        var token = $scope.bearerToken;
        var user = $scope.user;

        $scope.setupOk = true;
        $scope.step1 = 'active';
        $scope.step2 = 'disabled';
        $scope.step3 = 'disabled';
        $scope.step4 = 'disabled';
        
        $scope.grouplist = []
        $http.post("/exporter/bearer", { 'user': user, 'token': token }).then(function successCallback(response) {
            $scope.grouplist = response.data.data;
            $('#flowDimmer').dimmerHide();
        }, function errorCallback(response) {
            var errorMessage = "Errore: " + response.data.message;
            console.log(response);
            $scope.errorMessage = errorMessage;
            $('#flowDimmer').dimmerHide();
            $('#error-message').modal('show');
        });
    };

    $scope.nextFlow = function() {
        $('#flowDimmer').dimmerShow();

        if ($scope.step1 == 'active') {
            var selectedGroups = [];
            $('#group-selection :checked').each(function() {
                selectedGroups.push($(this).val());
            });

            $scope.userlist = []
            $http.post("/exporter/getusers_bygroup", { 'groups': selectedGroups }).then(function successCallback(response) {
                $scope.step1 = 'completed';
                $scope.step2 = 'active';
                
                $scope.userlist = response.data.data;
                $('#flowDimmer').dimmerHide();
            }, function errorCallback(response) {
                var errorMessage = "Errore: " + response.data.message;
                console.log(response);
                $scope.errorMessage = errorMessage;
                $('#flowDimmer').dimmerHide();
                $('#error-message').modal('show');
            });
        }
        else if ($scope.step2 == 'active') {
            var selectedUsers = [];
            $('#user-selection :checked').each(function() {
                selectedUsers.push($(this).val());
            });

            if (selectedUsers.length == 0) {
                $scope.errorMessage = "Devi selezionare almeno un utente.";
                $('#flowDimmer').dimmerHide();
                $('#error-message').modal('show');
                return;
            }
            
            $scope.userlist = []
            $http.post("/exporter/getuser_meetings", { 'users': selectedUsers }).then(function successCallback(response) {
                $scope.step1 = 'completed';
                $scope.step2 = 'completed';
                $scope.step3 = 'active';

                var options = {'weekday': 'long', 'year': 'numeric', 'month': 'long', 'day': '2-digit', 'hour': '2-digit', 'minute': '2-digit', 'second': '2-digit'};
                
                $scope.eventlist = response.data.data;
                $scope.eventlist.forEach(function (item) {
                    var durata = Math.floor((new Date(item['end'])) - (new Date(item['start']))) / (1000*60);
                    var hours = Math.floor(durata / 60);  
                    var minutes = Math.floor(durata % 60);
                    
                    item['durata'] = hours + " ore e " + minutes + "minuti";
                    item['start'] = new Date(item['start']).toLocaleTimeString('it-IT', options);
                    item['start'] = item['start'].slice(0, -3);
                    item['end'] = new Date(item['end']).toLocaleTimeString('it-IT', options);
                    item['end'] = item['end'].slice(0, -3);
                });

                $('#flowDimmer').dimmerHide();
            }, function errorCallback(response) {
                var errorMessage = "Errore: " + response.data.message;
                console.log(response);
                $scope.errorMessage = errorMessage;
                $('#flowDimmer').dimmerHide();
                $('#error-message').modal('show');
            });
        }
        else if ($scope.step3 == 'active') {
            var selectedEvents = [];
            $('#event-selection :checked').each(function() {
                selectedEvents.push($(this).val());
            });

            if (selectedEvents.length == 0) {
                $scope.errorMessage = "Devi selezionare almeno una riunione.";
                $('#flowDimmer').dimmerHide();
                $('#error-message').modal('show');
                return;
            }
            
            $scope.userlist = []
            $http.post("/exporter/getmeeting_records", { meetings: selectedEvents }).then(function successCallback(response) {
                $scope.step1 = 'completed';
                $scope.step2 = 'completed';
                $scope.step3 = 'completed';
                $scope.step4 = 'active';

                $scope.meetingRecords = response.data.data;
                $scope.meetingRecords.forEach(function (item) {
                    var description = item['id'];
                    $scope.eventlist.forEach(function (ev) {
                        if (ev['id'] == description) {
                            description = "Lezione di " + ev.start + ", durata " + ev.durata + " (" + ev.partecipant + " partecipanti)";
                        }
                    });
                    item['descr'] = description;
                });

                $('#flowDimmer').dimmerHide();
            }, function errorCallback(response) {
                var errorMessage = "Errore: " + response.data.message;
                console.log(response);
                $scope.errorMessage = errorMessage;
                $('#flowDimmer').dimmerHide();
                $('#error-message').modal('show');
            });
        }
    };

    $scope.prevFlow = function() {
        if ($scope.step2 == 'active') {
            $scope.step1 = 'active';
            $scope.step2 = 'suspended';
        }
        else if ($scope.step3 == 'active') {
            $scope.step2 = 'active'
            $scope.step3 = 'suspended'
        }
        else if ($scope.step4 == 'active') {
            $scope.step3 = 'active'
            $scope.step4 = 'suspended'
        }
    };

    $scope.showElement = function(mid) {
        if ($scope.showTable == mid) {
            $scope.showTable = "";
        }
        else {
            $scope.showTable = mid;
        }
    };

    $scope.downloadExcel = function(mid) {
        $scope.meetingRecords.forEach(function (item) {
            if (item['id'] == mid) {
                $("#table").val(encodeURIComponent(JSON.stringify(item)));
                var form = angular.element('#excel-form');
                form.submit();
            }
        });
    };

    $scope.selectCheck = function (cid) {
        if ($("#" + cid).prop('checked')) {
            $("#" + cid).removeClass('checked');
            $("#" + cid).prop('checked', false);
        }
        else {
            $("#" + cid).addClass('checked');
            $("#" + cid).prop('checked', true);
        }
    };
}]);