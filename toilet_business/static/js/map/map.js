//Declare
//Google Map Object
var map;
//init position：Taipei station
var taipei = new google.maps.LatLng(25.048069, 121.517101);
//set infowindow last time
var oldinfowindow = null;
//set current start Marker
var currentStartMarkder = null;
//set current start Marker
var currentDestinationMarkder = null;
//set current start
var currentStart = null;
//set current destination
var currentDestination = null;
//toilet detail info
var currentToiletDetail = null;
//real time location
var enableRealTimeLocation = true;
//max key
var minKey = null;
//max marker
var minMarker = null;
//room type
var defaultRoomType = "ALL";


// var pubnub = new PubNub({
//     publishKey:   'pub-c-fc8119f1-3289-4e26-ae45-1dbd30e9b970',
//     subscribeKey: 'sub-c-ae59e504-e9f4-11e7-9723-66707ad51ffc'
// });

//set map style
var stylesArray = [
    {elementType: 'geometry', stylers: [{color: '#242f3e'}]},
    {elementType: 'labels.text.stroke', stylers: [{color: '#242f3e'}]},
    {elementType: 'labels.text.fill', stylers: [{color: '#746855'}]},
    {
        featureType: 'administrative.locality',
        elementType: 'labels.text.fill',
        stylers: [{color: '#d59563'}]
    },
    {
        featureType: 'poi',
        elementType: 'labels.text.fill',
        stylers: [{color: '#d59563'}]
    },
    {
        featureType: 'poi.park',
        elementType: 'geometry',
        stylers: [{color: '#263c3f'}]
    },
    {
        featureType: 'poi.park',
        elementType: 'labels.text.fill',
        stylers: [{color: '#6b9a76'}]
    },
    {
        featureType: 'road',
        elementType: 'geometry',
        stylers: [{color: '#38414e'}]
    },
    {
        featureType: 'road',
        elementType: 'geometry.stroke',
        stylers: [{color: '#212a37'}]
    },
    {
        featureType: 'road',
        elementType: 'labels.text.fill',
        stylers: [{color: '#9ca5b3'}]
    },
    {
        featureType: 'road.highway',
        elementType: 'geometry',
        stylers: [{color: '#746855'}]
    },
    {
        featureType: 'road.highway',
        elementType: 'geometry.stroke',
        stylers: [{color: '#1f2835'}]
    },
    {
        featureType: 'road.highway',
        elementType: 'labels.text.fill',
        stylers: [{color: '#f3d19c'}]
    },
    {
        featureType: 'transit',
        elementType: 'geometry',
        stylers: [{color: '#2f3948'}]
    },
    {
        featureType: 'transit.station',
        elementType: 'labels.text.fill',
        stylers: [{color: '#d59563'}]
    },
    {
        featureType: 'water',
        elementType: 'geometry',
        stylers: [{color: '#17263c'}]
    },
    {
        featureType: 'water',
        elementType: 'labels.text.fill',
        stylers: [{color: '#515c6d'}]
    },
    {
        featureType: 'water',
        elementType: 'labels.text.stroke',
        stylers: [{color: '#17263c'}]
    }
];

$(function() {
    initSetting();

    initMap(taipei);

    var optn = {
        enableHighAccuracy: true,
        timeout: Infinity,
        maximumAge: 0
    }

    navigator.geolocation.watchPosition(
        function (position) {
            console.log("watchPosition");
            //continuous track current location
            if(enableRealTimeLocation) {
                // console.log("enableRealTimeLocation");
                // console.log(position.coords.latitude + "," + position.coords.longitude);
                currentStart = new google.maps.LatLng(position.coords.latitude, position.coords.longitude);
                setStartPoint(currentStart);
            }
        });

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

    $("#roomTypeAll").click(function () {
        searchByRoomType('ALL');
    });

    $("#roomTypeAccessible").click(function () {
        searchByRoomType('rest');
    });

    $("#roomTypeChild").click(function () {
        searchByRoomType('child');
    });

    $("#roomTypeKindly").click(function () {
        searchByRoomType('kindly');
    });

    $("#travelDriving").click(function () {
        changeTravelMode('DRIVING');
    });

    $("#travelWalking").click(function () {
        changeTravelMode('WALKING');
    });
});

function initSetting() {
    console.log("initSetting");
    oldinfowindow = null;
    currentStartMarkder = null;
    currentStart = null;
    currentDestination = null;
    currentToiletDetail = null;

    $("#messageBlock").hide();
    $("#minPath").hide();
    $("#directionsPanel").hide();


    //initial hidden
    $("#travelMode").val('DRIVING');
}

function newMapObject(centerPoint) {
    //map setting
    var mapOptions = {
        center: centerPoint, //Start Center{lat:經度, lng:緯度}(LatLng物件) (注意經緯度必須要是數值，不可放字串)
        zoom: 15,
        styles: stylesArray
    };

    //initial map
    map = new google.maps.Map($("#map")[0], mapOptions);
}

//init map ver00
function initMap(centerPoint){
    newMapObject(centerPoint);

    // geolocation current position
    geoloactionProcess();
}

// geolocation current position
function geoloactionProcess(){
    //geolocation current position
    if(navigator.geolocation){
        navigator.geolocation.getCurrentPosition(function(position) {
            currentStart = new google.maps.LatLng(position.coords.latitude,position.coords.longitude);
            setStartPoint(currentStart);
            markerPosition(position.coords.latitude, position.coords.longitude);

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
        currentStart = taipei;
        setStartPoint(currentStart);
    }
}

//set start point
function setStartPoint(point) {
    map.setCenter(point);
    //Start Marker
    startMarker = new google.maps.Marker({
        icon : 'https://maps.google.com/mapfiles/ms/icons/blue-dot.png',
        position : point,
        title : "您的位置",
        map : map
    });

    //set real time location
    if(currentStartMarkder){
        currentStartMarkder.setMap(null);
    }
    currentStartMarkder = startMarker;
}

//add marker
function addMarker(position, title, label){ // data(latitude,longitude)
    //create new marker
    var marker = new google.maps.Marker({
        position : position,
        map : map,
        title : title,
        label: label
    });

    return marker;
}

//set infowindow
function addMarkerInfo(position, markerObj, itemObj, isCalc){
    var marker = markerObj;
    var item = itemObj;
    var comparaKey = item.latitude+","+item.longitude;
    var contentString = '<div id="content">'+
        '<div id="siteNotice">'+
        '</div>'+
        '<h3 id="firstHeading" class="firstHeading">'+item.title+'</h3>'+
        '<div id="bodyContent">'+
        '<p><b>總座數: </b>'+item.number+'</p>'+
        '<p><b>友善空間: </b>'+item.rest+'</p>'+
        '<p><b>親子廁間: </b>'+item.child+'</p>'+
        '<p><b>貼心公廁: </b>'+item.kindly+'</p>'+
        '</div>'+
        '</div>';

    //create marker infowindow
    var infowindow = new google.maps.InfoWindow({
        content: contentString
    });

    //open current marker infowindow
    //優先顯示最近位置的infowindow

    if (comparaKey == minKey){
        // console.log("最近的座標"+comparaKey);
        $("#minPath").html("最近的公廁 >>> "+item.title);
        $("#minPath").show();
        minMarker = marker;
    }

    //if there are any info window open, close it
    if (oldinfowindow){
        oldinfowindow.close();
    }
    oldinfowindow = infowindow;

    infowindow.open(map, marker);
    //listener for click event
    marker.addListener('click', function() {
        //if there are any info window open, close it
        if (oldinfowindow){
            oldinfowindow.close();
        }
        oldinfowindow = infowindow;

        //open current marker infowindow
        infowindow.open(map, marker);

        //select different travel way and show the route
        if(isCalc){
            var msg = confirm("是否前往目的地 "+item.title+" ?");
            if(msg) {
                calcRoute(currentStart, position, item, $("#travelMode").val());
            }
        }
    });
}

//Ajax
function markerPosition(latitude, longitude){
    var data = {"current_lat":latitude, "current_lng":longitude, "room_type": defaultRoomType};

    $.ajax({
        type: 'POST',
        url: '/map/flaskajax',
        dataType: 'json',
        contentType: 'application/json; charset=utf-8',
        data: JSON.stringify(data),
        success: function(callback) {
            minMarker = null;
            minKey = callback.minKey;
            resultList = callback.resultList;

            if(resultList != null && resultList.length > 0) {
                resultList.forEach(function myFunction(item, index) {
                    // console.log("地點:" + item.title + ", 友善:" + item.rest + ", 親子:" + item.child + ", 貼心:" + item.kindly);
                    var lat = item.latitude;
                    var lng = item.longitude;
                    var position = new google.maps.LatLng(parseFloat(lat), parseFloat(lng));
                    var markerObj = addMarker(position, item.title, null);  //（position, title)
                    addMarkerInfo(position, markerObj, item, true);
                });
                google.maps.event.trigger(minMarker, 'click');
            }else{
                alert("查無資訊");
            }
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
    currentDestination = null;
    var address = document.getElementById('address').value;
    geocoder.geocode({'address': address}, function (results, status) {
        if (status === 'OK') {
            // console.log(results[0].geometry.location.lat());
            // console.log(results[0].geometry.location.lng());

            var current_lat = currentStart.lat();
            var current_lng = currentStart.lng();

            //initial map for marker new position
            newMapObject(taipei);

            //get address location data
            var latitude = results[0].geometry.location.lat();
            var longitude = results[0].geometry.location.lng();

            var data = {"current_lat": current_lat,
                        "current_lng": current_lng,
                        "search_lat": latitude,
                        "search_lng": longitude};

            //get distance infomation
            getDistanceInfo(data);

            //marker the new start point
            currentStart = results[0].geometry.location;
            setStartPoint(currentStart);

            //marker position and get around place by ajax function
            markerPosition(latitude, longitude);
        } else {
            alert('請輸入正確的地點資訊');
            initMap(taipei);
        }
    });
}

//call distance_ajax
function getDistanceInfo(data) {
    var distance = null;
    $.ajax({
        type: 'POST',
        url: '/map/distanceajax',
        dataType: 'json',
        contentType: 'application/json; charset=utf-8',
        data: JSON.stringify(data),
        success: function(callback) {
            var distance = callback.distance;
            // console.log(distance);
            if (distance){
                if(distance >= 1){
                    enableRealTimeLocation = false;
                }else{
                    enableRealTimeLocation = true;
                }
            }
        },
        error: function() {
            console.log("無法取得距離資訊!");
        }
    });

}

//select different travel way and show the route
function calcRoute(start, end, itemObj, mode) {
    // console.log(start.lat()+","+start.lng);
    // console.log(end.lat(), end.lng);
    // console.log(title);
    // console.log(mode);
    currentToiletDetail = itemObj;

    //initial map for route
    newMapObject(start);
    setStartPoint(start);
    var directionsDisplay = new google.maps.DirectionsRenderer({ suppressMarkers: true });
    var directionsService = new google.maps.DirectionsService;
    var request = {
        origin:start,
        destination:end,
        travelMode: google.maps.TravelMode[mode],
        transitOptions: {
            departureTime: new Date(1337675679473),
            modes: ['BUS'],
            routingPreference: 'FEWER_TRANSFERS'
        }
    };

    $("#directionsPanel").hide();
    directionsDisplay.setMap(map);
    directionsDisplay.setPanel($("#directionsPanel")[0]);

    directionsService.route(request, function(response, status) {
        if (status == 'OK') {
            $("#directionsPanel").show();
            var route = response.routes[0].legs[0];
            directionsDisplay.setDirections(response);

            var startMarkerObj = addMarker(route.start_location, '起點', 'A');
            var endMarkerObj = addMarker(route.end_location, currentToiletDetail.title, 'B');
            addMarkerInfo(route.end_location, endMarkerObj, currentToiletDetail, false);

            $("#msgInfo").html(currentToiletDetail.title);
            $("#messageBlock").show();
        }
    });


    //set current destination for change travel mode
    currentDestination = end;
}

//set travel mode
function changeTravelMode(mode){
    $("#travelMode").val(mode);
    if (currentDestination) {
        calcRoute(currentStart, currentDestination, currentToiletDetail, mode);
    }else{
        alert("請選擇目的地");
    }
}

//search by room type
function searchByRoomType(roomType) {
    $("#directionsPanel").hide();
    currentDestination = null;
    defaultRoomType = roomType;
    var current_lat = currentStart.lat();
    var current_lng = currentStart.lng();
    newMapObject(currentStart);
    setStartPoint(currentStart);
    markerPosition(current_lat, current_lng);
}