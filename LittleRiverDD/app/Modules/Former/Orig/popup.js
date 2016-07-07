var initPopup = (function() {
// _initArcGISJS();

  function _initInfoWindow(InfoWindow) {
    var infoWindow = new InfoWindow(null, dojo.byId("infoPanel"));
    infoWindow.startup();
    return infoWindow
  }

  function _initTemplate(InfoTemplate) {
    var infoTemplate = new InfoTemplate("Feature Information", "<table class = 'onyx' cellspacing='0'>" +
      "<tr><td><b>FID</b></td></td><td>${FID}</td></tr>" + "<tr><td><b>Location ID</b></td></td><td>${LOCATIONID}</td></tr>" + "<tr><td><b>Spaces</b></td></td><td>${NUMSPACES}</td></tr></table>"
    );

    return infoTemplate
  }

  function _initializeWindow(map, infoWindow, connect, registry) {
    var popup = map.infoWindow;

    console.log('HUIH', map)

    connect.connect(popup, "onSelectionChange", function() {
      _displayPopupContent(map, _getPopupFeature(map), infoWindow, registry);
    });

    connect.connect(popup, "onSetFeatures", function() {
      _displayPopupContent(map, _getPopupFeature(map), infoWindow, registry);
    });

  }

  function _getPopupFeature(map) {
    return map.infoWindow.getSelectedFeature();
  }

  function _displayPopupContent(map, feature, infoWindow, registry) {
    var popup = app.map.infoWindow;

    if (feature) {
      var content = feature.getContent();
      infoWindow.setContent(content);

      // STYLE UI
      function _popupContainerUI(feature) {
        $('#contentContainer').css('display', 'block');
        $('.title').empty();
        $('.title').append(feature.attributes.FID);
        $('.title').css('background-color', '#727272').css('color', 'white').css('border-radius', '3px');
        $('.right').css('height', '180px');
        $('#featureCount').remove();
        $('#arrowLeft').remove();
        $('#arrowRight').remove();
        $('#featureCount').remove();
        $('.right').find('.sprite').remove();
        $('.top .right').append('<div id="arrowLeft"></div>').append('<div id="arrowRight"></div>').append('<div id="featureCount">' + popup.features.length + ' Features</div>');
        $('.bottom').empty();
        $('#arrowLeft').click(function() {
          map.infoWindow.selectPrevious();

          function selectPrevious(map) {
            map.infoWindow.selectPrevious();
          }
        });
        $('#arrowRight').click(function() {
          selectNext(map);

          function selectNext(map) {
            map.infoWindow.selectNext();
          }
        });
      }
      // STYLE UI

      _popupContainerUI(feature);

      registry.byId("infoPanel").set(content);
      $('#infoPanel').css('display', 'block');

    }
  }

  function _selectPrevious(map) {
    map.infoWindow.selectPrevious();
  }

  function _selectNext(map) {
    map.infoWindow.selectNext();
  }

  function _initJSPopup(map){
   console.log(map)
   var JSAPI = {};
 require([
  "dojo/parser", 
  "dojo/ready", 
  "esri/dijit/InfoWindow",  
  "esri/InfoTemplate", 
  "dijit/registry",
  "dojo/_base/connect", 
  "dojo/domReady!"], 
  function(parser, ready, InfoWindow, InfoTemplate, registry, connect, dom) {
  // COMPOSE OBJECT TO ADD FL to RESOURCES
         var infoWindow = _initInfoWindow(InfoWindow);
        // console.log('FIJFASJ', infoWindow)
        _initializeWindow(map, infoWindow, connect, registry);

        JSAPi = {
          InfoTemplate: InfoTemplate,
          InfoWindow: InfoWindow
        }

}) // end require function

return JSAPI
}

  return {
    initInfoWindow: _initInfoWindow,
    initTemplate: _initTemplate,
    getPopupFeature: _getPopupFeature,
    selectPrevious: _selectPrevious,
    selectNext: _selectNext,
    initializeWindow: _initializeWindow,
    initJSPopup: _initJSPopup
  }


})();