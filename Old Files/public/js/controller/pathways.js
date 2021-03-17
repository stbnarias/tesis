var myApp = angular.module('myApp', ['ngFileUpload']);
myApp.controller('AppController', ['$scope', '$http', function ($scope, $http) {
    $('.file-form').validator();
    $scope.init = function () {
        var files = document.querySelectorAll(".pathway-name");
        files.forEach(function (file) {
            file.value = "";
        });
    };
    $scope.setActive = function (id) {
        resetNavigationClass();
        var nav = document.getElementById(id);
        nav.className += " active";
    };
    $scope.process = function () {
        var files = [];
        var data = new FormData();
        data.append('file', $scope.pathway1);
        $http.post('upload', data, {
                transformRequest: angular.identity,
                headers: {
                    'Content-Type': undefined
                }
            })
            .success(function (response) {
                files.push(response);
                data = new FormData();
                data.append('file', $scope.pathway2);
                $http.post('upload', data, {
                        transformRequest: angular.identity,
                        headers: {
                            'Content-Type': undefined
                        }
                    })
                    .success(function (response) {
                        files.push(response);
                        $http.post('run', {files: files}).success(function (response) {
                            var output = document.getElementById("output");
                            output.style.display = "block";
                            //output.innerHTML = response.join("\n");
                            //response = response.concat("\n"); // NEW
                            output.innerHTML = response.concat("\n"); // ADDED
                            console.log(response.concat("\n"));
                        });
                    }); 
            });      
    };

    $(document).on('change', '.btn-file :file', function () {
        var input = $(this),
            label = input.val().replace(/\\/g, '/').replace(/.*\//, '');
        input.trigger('fileselect', [label]);
    });

    $('.btn-file :file').on('fileselect', function (event, label) {
        var input = $(this).parents('.input-group').find(':text'),
            log = label;
        if (input.length) {
            input.val(log);
        } else {
            if (log) console.log(log);
        }

    });

    function resetNavigationClass() {
        var navs = document.querySelectorAll('.navigation');
        navs.forEach(function (nav) {
            nav.className = "navigation";
        });
    }
}]);