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
		initFeatureLayer: function(){
			console.log("URL IS????", this.url)
			var featureLayer = new esri.layers.FeatureLayer(this.url,{
				mode: esri.layers.FeatureLayer.MODE_ONEDEMAND,
				infoTemplate: initTemplate(InfoTemplate, 'Table'),
				outFields: ["*"]
				})
			return featureLayer
			}
		})
	})