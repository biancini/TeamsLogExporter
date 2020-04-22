$("#error-message").hide();

var app = angular.module('teamsLogExporter', []);

app.config(['$interpolateProvider', '$httpProvider', function($interpolateProvider, $httpProvider) {
    $interpolateProvider.startSymbol('{a');
    $interpolateProvider.endSymbol('a}');

    $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    
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

app.service('MicrosoftAPI', ['$http', '$q', function ($http, $q) {
    this.setBearer = function (user, token) {
        var def = $q.defer();

        $http.post("/exporter/bearer", { 'user': user, 'token': token }).then(function successCallback(response) {
            var data = response.data.data;
            def.resolve(data);
        }, function errorCallback(response) {
            def.reject(response.data.message);
        });

        return def.promise;
    };

    this.getUserByGroup = function (selectedGroups) {
        var def = $q.defer();

        $http.post("/exporter/getusers_bygroup", { 'groups': selectedGroups }).then(function successCallback(response) {
            var data = response.data.data;
            def.resolve(data);
        }, function errorCallback(response) {
            def.reject(response.data.message);
        });

        return def.promise;
    };

    this.getUserMeetings = function (selectedUsers) {
        var def = $q.defer();

        $http.post("/exporter/getuser_meetings", { 'users': selectedUsers }).then(function successCallback(response) {
            var options = {'weekday': 'long', 'year': 'numeric', 'month': 'long', 'day': '2-digit', 'hour': '2-digit', 'minute': '2-digit', 'second': '2-digit'};
            
            var data = response.data.data;
            data.forEach(function (item) {
                var durata = Math.floor((new Date(item['end'])) - (new Date(item['start']))) / (1000*60);
                var hours = Math.floor(durata / 60);  
                var minutes = Math.floor(durata % 60);
                
                item['durata'] = hours + " ore e " + minutes + "minuti";
                item['start'] = new Date(item['start']).toLocaleTimeString('it-IT', options);
                item['start'] = item['start'].slice(0, -3);
                item['end'] = new Date(item['end']).toLocaleTimeString('it-IT', options);
                item['end'] = item['end'].slice(0, -3);
            });
            def.resolve(data);
        }, function errorCallback(response) {
            def.reject(response.data.message);
        });

        return def.promise;
    };

    this.getMeetingRecord = function (selectedEvents, eventlist) {
        var def = $q.defer();

        $http.post("/exporter/getmeeting_records", { meetings: selectedEvents }).then(function successCallback(response) {
            var data = response.data.data;
            data.forEach(function (item) {
                var description = item['id'];
                eventlist.forEach(function (ev) {
                    if (ev['id'] == description) {
                        description = "Lezione di " + ev.start + ", durata " + ev.durata + " (" + ev.partecipant + " partecipanti)";
                    }
                });
                item['descr'] = description;
            });
            def.resolve(data);
        }, function errorCallback(response) {
            def.reject(response.data.message);
        });

        return def.promise;
    };
}]);

app.controller('mainController', ['$rootScope', '$scope', '$http', 'MicrosoftAPI', function($rootScope, $scope, $http, MicrosoftAPI) {
    $scope.setupOk = false;
    $scope.errorMessage = '';

    $scope.showError = function (errorMessage) {
        console.log(errorMessage);
        $scope.errorMessage = errorMessage;

        $('#flowDimmer').dimmerHide();
        $('#error-message').modal('show');
    };

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
        MicrosoftAPI.setBearer(user, token).then(function (data) {
            $scope.grouplist = data;
            $('#flowDimmer').dimmerHide();
        },
        function (data) {
            $scope.showError(data);
            $('#flowDimmer').dimmerHide();
        });
    };

    $scope.nextFlow = function() {
        $('#flowDimmer').dimmerShow();

        if ($scope.step1 == 'active') {
            var selectedGroups = [];
            $('#group-selection :checked').each(function() {
                selectedGroups.push($(this).val());
            });

            MicrosoftAPI.getUserByGroup(selectedGroups).then(function (data) {
                $scope.step1 = 'completed';
                $scope.step2 = 'active';

                $scope.userlist = data;
                $('#flowDimmer').dimmerHide();
            },
            function (data) {
                $scope.showError(data);
                $('#flowDimmer').dimmerHide();
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
            MicrosoftAPI.getUserMeetings(selectedUsers).then(function (data) {
                $scope.step1 = 'completed';
                $scope.step2 = 'completed';
                $scope.step3 = 'active';

                $scope.eventlist = data;
                $('#flowDimmer').dimmerHide();
            },
            function (data) {
                $scope.showError(data);
                $('#flowDimmer').dimmerHide();
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
            
            $scope.meetingRecords = []
            MicrosoftAPI.getMeetingRecord(selectedEvents, $scope.eventlist).then(function (data) {
                $scope.step1 = 'completed';
                $scope.step2 = 'completed';
                $scope.step3 = 'completed';
                $scope.step4 = 'active';

                $scope.meetingRecords = data;
                $('#flowDimmer').dimmerHide();
            },
            function (data) {
                $scope.showError(data);
                $('#flowDimmer').dimmerHide();
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