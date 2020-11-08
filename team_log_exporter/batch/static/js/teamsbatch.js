$("#error-message").hide();

var app = angular.module('teamsBatch', []);

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

app.service('DjangoAPI', ['$http', '$q', function ($http, $q) {
    this.humanFileSize = function(bytes) {
        const thresh = 1000;

        if (Math.abs(bytes) < thresh) {
            return bytes + ' B';
        }

        const units = ['kB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'];
        let u = -1;
        const r = 10;

        do {
            bytes /= thresh;
            ++u;
        } while (Math.round(Math.abs(bytes) * r) / r >= thresh && u < units.length - 1);

        return bytes.toFixed(1) + ' ' + units[u];
    };
    
    this.loadCSVFile = function (dataFile) {
        var def = $q.defer();

        $('#uploadChangeStateTarget').removeClass('success');
        $('#uploadChangeStateTarget').addClass('loading');
        $('#simTitle').text(dataFile.name);
        $('#simText').text('Caricamento in corso...');

        var fileExt = dataFile.name.split('.').pop().toUpperCase();
        var fileSz = this.humanFileSize(dataFile.size);
        $('#filetype').text(fileExt + " (" + fileSz + ")");

        formData = new FormData();
        formData.append("uploadcsv", dataFile);

        $http({
            url: $('#uploadChangeStateTarget').attr('action'),
            method: 'POST',
            data: formData,
            headers: { 'Content-Type': undefined },
            reportProgress: true,
            uploadEventHandlers: {
                progress: function (event) {
                    var loaded = event.loaded;
                    var total = event.total;
                    var percent_complete = (loaded / total) * 100;

                    $("#divProgress1").circularloader({
                        progressPercent: Math.floor(percent_complete)
                    });
                }
            }
        }).then(function (event) {
            $('#divProgress1').remove();
            $('#uploadChangeStateTarget').removeClass('loading');
            $('#uploadChangeStateTarget').addClass('success');
            $('#simText').text('Caricamento completato. Indicate ' + event.data.message.length + ' lezioni da scaricare.');

            def.resolve(event.data.message);
        }).catch(function (err) {
            def.reject(err.message);
        });

        return def.promise;
    };

    this.downloadTeamsJson = function (callId) {
        var def = $q.defer();

        $http.post("/batch/download_jsonapi", { 'callId': callId }).then(function successCallback(response) {
            var jsonData = response.data.calldata;
            def.resolve(jsonData);
        }, function errorCallback(err) {
            console.log("Error while downloading file: " + err.message);
            def.reject(err.message);
        });

        return def.promise;
    };

    this.downloadTeamsExcel = function (jsonFile) {
        var def = $q.defer();

        $http.post("/batch/generate_excel", { 'jsonFile': jsonFile }).then(function successCallback(response) {
            var filename = response.data.filename;
            var jsonData = response.data.calldata;
            def.resolve([filename, jsonData]);
        }, function errorCallback(err) {
            console.log("Error while downloading file: " + err.message);
            def.reject(err.message);
        });

        return def.promise;
    };
}]);

app.controller('mainController', ['$scope', '$q', 'DjangoAPI', function($scope, $q, DjangoAPI) {
    $scope.step1 = 'active';
    $scope.step2 = 'inactive';
    $scope.step3 = 'inactive';

    $scope.stopProceed = true;
    $scope.showDownloadZip = false;
    $scope.showDownloadExcel = false;
    $scope.errorMessage = '';

    $scope.downloadedJsons = {};
    $scope.downloadedExcels = {};

    $scope.showError = function (errorMessage) {
        console.log(errorMessage);
        $scope.errorMessage = errorMessage;

        $('#flowDimmer').dimmerHide();
        $('#error-message').modal('show');
    };

    $scope.dropCSV = function(event) {
        DjangoAPI.loadCSVFile(event.originalEvent.dataTransfer.files[0]).then(function (data) {
            $scope.stopProceed = false;
            $scope.lessonIds = data;
        },
        function (data) {
            console.log("errore");
            $scope.showError(data);
        });
    };

    $scope.uploadCSV = function(event) {
        DjangoAPI.loadCSVFile(event.originalEvent.srcElement.files[0]).then(function (data) {
            $scope.stopProceed = false;
            $scope.lessonIds = data;
        },
        function (data) {
            $scope.showError(data);
        });
    };

    $scope.downloadJsonAPI = function() {
        $scope.stopProceed = true;
        var eventIds = [];

        $('#event-selection :checked').each(function() {
            eventIds.push($(this).val());
        });

        eventIds = [...new Set(eventIds)];

        var total = eventIds.length;
        var count = 0;

        var promises = [];
        for (let callId of eventIds) {
            var prom = DjangoAPI.downloadTeamsJson(callId).then(function (data) {
                $("#downloaded-" + callId).removeClass('d-none');
                $scope.downloadedJsons[callId] = data;
                count++;

                var percent = (count / total) * 100;
                $("#progress-json").attr("style", "width: " + percent + "%");
                $("#progress-json").attr("aria-valuenow", percent);
            },
            function (data) {
                console.log("errore");
                $scope.showError(data);
            });

            promises.push(prom);
        }

        return $q.all(promises);
    };

    $scope.generateExcel = function() {
        var total = Object.keys($scope.downloadedJsons).length;
        var count = 0;

        $scope.lessonExcels = [];
        var promises = [];
        
        for (let callId in $scope.downloadedJsons) {
            var jsonFile = $scope.downloadedJsons[callId];

            var prom = DjangoAPI.downloadTeamsExcel(jsonFile).then(function (data) {
                if (data[1] != null && typeof(data[1]) != "undefined") {
                    filename = data[0];
                    duplicatenum = 0;
                    while ($scope.lessonExcels.includes(filename)) {
                        duplicatenum += 1;
                        filename = data[0].replace('.xlsx', ' - ' + duplicatenum + '.xlsx');
                    }

                    $scope.lessonExcels.push(filename);
                    $scope.lessonExcels.sort();
                    $scope.downloadedExcels[filename] = data[1];
                }
                count++;

                var percent = (count / total) * 100;
                $("#progress-excel").attr("style", "width: " + percent + "%");
                $("#progress-excel").attr("aria-valuenow", percent);
            },
            function (data) {
                console.log("errore");
                $scope.showError(data);
            });

            promises.push(prom);
        }

        return $q.all(promises);
    };

    $scope.goNextStep = function() {
        if ($scope.step1 == 'active') {
            $scope.step1 = 'inactive';
            $scope.step2 = 'active';
            $scope.step3 = 'inactive';
        }
        else if ($scope.step2 == 'active' && $scope.showDownloadZip == false) {
            $scope.stopProceed = true;
            $scope.downloadJsonAPI().then(function (r) {
                $scope.stopProceed = false;
                $scope.showDownloadZip = true;
            });
        }
        else if ($scope.step2 == 'active' && $scope.showDownloadZip == true) {
            $scope.step1 = 'inactive';
            $scope.step2 = 'inactive';
            $scope.step3 = 'active';

            $scope.showDownloadZip = false;
            $scope.stopProceed = true;
            
            $scope.generateExcel().then(function (r) {
                $scope.showDownloadExcel = true;
            });
        }
    }

    $scope.b64toBlob = function (b64Data, contentType, sliceSize) {
        contentType = contentType || '';
        sliceSize = sliceSize || 512;
      
        var byteCharacters = atob(b64Data);
        var byteArrays = [];
      
        for (var offset = 0; offset < byteCharacters.length; offset += sliceSize) {
          var slice = byteCharacters.slice(offset, offset + sliceSize);
      
          var byteNumbers = new Array(slice.length);
          for (var i = 0; i < slice.length; i++) {
            byteNumbers[i] = slice.charCodeAt(i);
          }
      
          var byteArray = new Uint8Array(byteNumbers);
      
          byteArrays.push(byteArray);
        }
          
        var blob = new Blob(byteArrays, {type: contentType});
        return blob;
    };

    $scope.downloadExcelZip = function() {
        const zip = JSZip();
        for (let callId in $scope.downloadedExcels) {
            var excelFile = encodeURI($scope.downloadedExcels[callId]);
            excelFile = $scope.b64toBlob(excelFile, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet');
            zip.file(callId, excelFile);
        }

        zip.generateAsync({type: 'blob'}).then(zipFile => {
            return saveAs(zipFile, 'excel_reports.zip');
        });
    };

    $scope.downloadExcelFile = function(callId) {
        var excelFile = encodeURI($scope.downloadedExcels[callId]);
        excelFile = $scope.b64toBlob(excelFile, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet');
        return saveAs(excelFile, callId);
    };

    $scope.downloadJsonZip = function() {
        const zip = JSZip();
        for (let callId in $scope.downloadedJsons) {
            var jsonFile = $scope.downloadedJsons[callId];
            jsonFile = JSON.stringify(JSON.parse(jsonFile), null, 4);
            zip.file(`${callId}.json`, jsonFile);
        }

        zip.generateAsync({type: 'blob'}).then(zipFile => {
            return saveAs(zipFile, 'teams_reports.zip');
        });
    };

    $scope.downloadJson = function(callId) {
        var jsonFile = $scope.downloadedJsons[callId];
        jsonFile = JSON.stringify(JSON.parse(jsonFile), null, 4);
        jsonFile = new Blob([jsonFile], { type: 'application/json' });
        return saveAs(jsonFile, `${callId}.json`);
    };

    $scope.countChecked = function () {
        var selectedItems = [];
        $('#event-selection :checked').each(function() {
            selectedItems.push($(this).val());
        });

        $scope.stopProceed = (selectedItems.length <= 0);
    }

    $scope.selectCheck = function (cid) {
        if ($("#" + cid).prop('checked')) {
            $("#" + cid).removeClass('checked');
            $("#" + cid).prop('checked', false);
        }
        else {
            $("#" + cid).addClass('checked');
            $("#" + cid).prop('checked', true);
        }

        $scope.countChecked();
    };
}]);