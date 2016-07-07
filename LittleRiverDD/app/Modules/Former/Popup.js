define(["dojo/_base/declare", "esri/dijit/InfoWindow", "esri/InfoTemplate", "dijit/registry", "esri/utils", "dojo/parser"],
  function(declare, InfoWindow, InfoTemplate, registry) {
    return declare([], {
      constructor: function(options) {
        this.infoContainer = options.infoContainer,
          this.relateContainer = options.relateContainer
      },
      initPopup: function() {
        console.log('IC', this.infoContainer)
        var infoWindow = new InfoWindow(null, this.infoContainer);
        var relateWindow = new InfoWindow(null, this.relateContainer);

        return {
          infoWindow: infoWindow,
          relateWindow: relateWindow
        }
      },
      popupStartup: function(infoWindow, relateWindow) {
        infoWindow.startup();
        relateWindow.startup();
      },
      setPopupContent: function(feature, infoWindow) {
        if (feature) {
          infoWindow.setContent(feature.getContent());
        }
      },
      setRelateContent: function(feature, relateWindow) {
        relateWindow.setContent(feature.getContent());
      },
      setInfoTemplate: function(Table) {
        if (Table == 'Table') {
          var fields = getFields();
          console.log('???', fields);
          console.log('FIELdS ARE: ', fields)
          var table = "<table class = 'onyx' cellspacing = '0'>"
          for (var key in DataLoad.apps[0].Fields) {
            if (DataLoad.apps[0].Fields.hasOwnProperty(key)) {
              console.log(key, ": ", DataLoad.apps[0].Fields[key]);
              table += "<tr><td>" + DataLoad.apps[0].Fields[key] + "</td><td>${" + key + "}</td></tr>"
            }
          }
          table += '</table>'
          console.log("TABLE IS: ", table)
          var infoTemplate = new InfoTemplate('Feature Information', table)
          return infoTemplate
        } else {
          var infoTemplate = new InfoTemplate()
          return infoTemplate
        }
      }
    });
  })