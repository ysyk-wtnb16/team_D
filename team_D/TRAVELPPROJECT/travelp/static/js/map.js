var map;
var marker;
var searchBox;
 
function initMap() {
    // 初期位置（例: 東京）
    var initialLocation = { lat: 35.6895, lng: 139.6917 };
 
    // 地図を表示
    map = new google.maps.Map(document.getElementById('map'), {
        center: initialLocation,
        zoom: 13
    });
 
    // マーカーを作成
    marker = new google.maps.Marker({
        position: initialLocation,
        map: map,
        draggable: true, // ドラッグ可能にする
        title: '選択された場所'
    });
 
    // 地図をクリックしてマーカーを移動
    google.maps.event.addListener(map, 'click', function(event) {
        marker.setPosition(event.latLng);
        document.getElementById('latitude').value = event.latLng.lat();
        document.getElementById('longitude').value = event.latLng.lng();
    });
 
    // 場所検索のインプットボックス
    var input = document.getElementById('location-search');
    searchBox = new google.maps.places.SearchBox(input);
 
    // 地図上で検索結果の位置を更新
    google.maps.event.addListener(searchBox, 'places_changed', function() {
        var places = searchBox.getPlaces();
 
        if (places.length == 0) {
            return;
        }
 
        // 最初に見つかった場所を選択
        var place = places[0];
 
        // 地図の中心を選択した場所に移動
        map.setCenter(place.geometry.location);
        map.setZoom(15);
 
        // マーカーを新しい位置に移動
        marker.setPosition(place.geometry.location);
 
        // 緯度経度を隠しフィールドにセット
        document.getElementById('latitude').value = place.geometry.location.lat();
        document.getElementById('longitude').value = place.geometry.location.lng();
    });
}