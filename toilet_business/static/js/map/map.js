//Declare
var map; //Google Map Object
var taipei = new google.maps.LatLng(25.048069, 121.517101); //init position：Taipei station

$(function() {
    initMap();

    $("#address").keyup(function(event) {
        if (event.keyCode === 13) {
            $("#specificSearch").click();
        }
    });

    $("#specificSearch").click(function () {
        var geocoder = new google.maps.Geocoder();
        geocodeAddress(geocoder, map);
    });

    $("#currentSearch").click(function () {
        var form = $("#form");
        form.attr("action", "/map/");
        form.attr("method", "POST");
        form.submit();
    });

    $("#home").click(function () {
        var form = $("#form");
        form.attr("action", "/");
        form.attr("method", "POST");
        form.submit();
    });
});

//init map ver00
function initMap(){
    //map setting
    var mapOptions = {
        center: {lat: 24.052181, lng: 121.088073}, //Start Center{lat:經度, lng:緯度} (注意經緯度必須要是數值，不可放字串)
        zoom: 15
    };
    //initial map
    map = new google.maps.Map($("#map")[0], mapOptions);

    //geolocation current position
    if(navigator.geolocation){
        navigator.geolocation.getCurrentPosition(function(position) {
            start = new google.maps.LatLng(position.coords.latitude,position.coords.longitude);
            setStartPoint(start);
            markerPosition(position.coords.latitude, position.coords.longitude)

            // test mark multiple location
            // addMarker("25.056334,121.543894", "post office");  //（latitude,longitude）
            // addMarker("25.055705,121.543832", "cafe");         //（latitude,longitude）
            // addMarker("25.055191,121.545222", "park");         //（latitude,longitude）
        }, function errorCallback(error) {
            var errorTypes={
                0:"不明原因錯誤",
                1:"使用者拒絕提供位置資訊",
                2:"無法取得位置資訊",
                3:"位置查詢逾時"
            };
            alert(errorTypes[error.code]);
        });
    }else{
        alert("你的瀏覽器不支援地理定位");
        start = taipei;
        setStartPoint(start);
    }

}

//set start point
function setStartPoint(point) {
    map.setCenter(point);
    //Start Marker
    startMarker = new google.maps.Marker({
        icon : 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png',
        position : point,
        title : "您的位置",
        map : map
    });
}

//add marker
function addMarker(data, title){ // data(latitude,longitude)
    var str = data.split(",");
    var L1 = str[0]; //latitude
    var L2 = str[1]; //longitude
    var myLatLng = {lat: parseFloat(L1), lng: parseFloat(L2)}; //{lat:latitude, lng:longitude}
    // console.log(myLatLng);
    var marker = new google.maps.Marker({
        position : myLatLng,
        map : map,
        title : title
    });
    map.setCenter(myLatLng);
}

//Ajax
function markerPosition(latitude, longitude){
    var data = {"latitude":latitude, "longitude":longitude};

    $.ajax({
        type: 'POST',
        url: '/map/flaskajax',
        dataType: 'json',
        contentType: 'application/json; charset=utf-8',
        data: JSON.stringify(data),
        success: function(callback) {
            callback.resultList.forEach(function myFunction(item, index) {
                var position = item.position
                var title = item.title
                console.log(position +" ; "+title)
                addMarker(position, title);  //（position, title）
            });
        },
        error: function() {
            console.log("error!");
        }
    });
}

/*
    1. search place by address and mark on the map
    2. get new place's latitude and longitude
    3. marker position and get around place by ajax function
*/
function geocodeAddress(geocoder, resultsMap) {
    var address = document.getElementById('address').value;
    var mapOptions = {
        center: {lat: 24.052181, lng: 121.088073}, //Start Center{lat:經度, lng:緯度} (注意經緯度必須要是數值，不可放字串)
        zoom: 15
    };
    //initial map
    map = new google.maps.Map($("#map")[0], mapOptions);

    geocoder.geocode({'address': address}, function (results, status) {
        if (status === 'OK') {
            // console.log(results[0].geometry.location.lat());
            // console.log(results[0].geometry.location.lng());

            //get address location data
            latitude = results[0].geometry.location.lat();
            longitude = results[0].geometry.location.lng();

            //marker the new start point
            setStartPoint(results[0].geometry.location)

            //marker position and get around place by ajax function
            markerPosition(latitude, longitude);
        } else {
            alert('Geocode was not successful for the following reason: ' + status);
        }
    });
}