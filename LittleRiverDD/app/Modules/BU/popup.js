var initPopup = (function(){

function _intitialize(InfoWindow, InfoTemplate){

    var infoTemplate = new InfoTemplate("Feature Information", "<table class = 'onyx' cellspacing='0'>"
    +"<tr><td><b>FID</b></td></td><td>${FID}</td></tr>"+"<tr><td><b>Location ID</b></td></td><td>${LOCATIONID}</td></tr>" + "<tr><td><b>Spaces</b></td></td><td>${NUMSPACES}</td></tr></table>"
            );

 return infoTemplate

}

function _initializeWindow(map, connect){
  console.log("MAPWHAT?", map)
  var popup = map.infoWindow;



//     connect.connect(popup,"onSetFeatures", function(){
//  displayPopupContent(popup.getSelectedFeature());
// })

  connect.connect(popup,"onSelectionChange", function(){
    displayPopupContent(popup.getSelectedFeature());
  })
}

  function displayPopupContent(feature){
    console.log("FEATURE IS??", feature)
    var popup = app.map.infoWindow;



    if(feature){
      var content = feature.getContent();
      infoWindow.setContent(content);

      styleUI(feature);

      console.log('Feature Count: ', popup.count);

      registry.byId("infoPanel").set(content);
      $('#infoPanel').css('display', 'block');

      // STYLE UI
function styleUI(feature){
    // DEPENDENCIES: popup

    $('#contentContainer').css('display', 'block');
    $('.title').empty();
    $('.title').append(feature.attributes.FID);
    $('.title').css('background-color', '#727272').css('color', 'white').css('border-radius', '3px');
    $('.right').css('height','180px');
    $('#featureCount').remove();
    $('#arrowLeft').remove();
    $('#arrowRight').remove();
    $('#featureCount').remove();
    $('.right').find('.sprite').remove();
    $('.top .right').append('<div id="arrowLeft"></div>').append('<div id="arrowRight"></div>').append('<div id="featureCount">' + popup.features.length + ' Features</div>');
    $('.bottom').empty();
    $('#arrowLeft').click(function(){
      // selectPrevious(map);
      map.infoWindow.selectPrevious();
      // initPopup.selectPrevious(map);
    
    function selectPrevious(map){
    map.infoWindow.selectPrevious();
  }


    });
    $('#arrowRight').click(function(){
      selectNext(map);
      //initPopup.selectNext(map);


  function selectNext(map){
    map.infoWindow.selectNext();
  }

  //   var _selectPrevious = function(map){
  //   map.infoWindow.selectPrevious();
  // }

  // var _selectNext = function(map){
  //   map.infoWindow.selectNext();
  // }


    });
  }
// STYLE UI

      // registry.byId($('#BC').children()).set(content);
      // $('#infoPanel').css('display', 'block');
    }
  }

  var _selectPrevious = function(map){
    map.infoWindow.selectPrevious();
  }

  var _selectNext = function(map){
    map.infoWindow.selectNext();
  }

  return {  	initialize: _intitialize,
  	selectPrevious: _selectPrevious,
  	selectNext: _selectNext,
  	initializeWindow: _initializeWindow
  }


})();