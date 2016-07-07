define(["dojo/_base/declare", "esri/layers/FeatureLayer"],
function(declare, FeatureLayer){
	return declare([], {
		url: null,
		mode: null,
		outFields: null,
		infoTemplate: null,
		constructor: function(options){
			this.url = options.url,
			this.mode = options.mode,
			this.outFields = options.outFields,
			this.infoTemplate = options.infoTemplate
		},
		initFeatureLayer: function(popup){
			var featureLayer = new esri.layers.FeatureLayer(this.url, {
				mode: esri.layers.FeatureLayer.MODE_ONEDEMAND,
				infoTemplate: popup.setInfoTemplate('Table'),
        // infoTemplate: popup.setInfoTemplate(),
				outFields: ["*"]
				})
      return featureLayer
			}
		})
	})