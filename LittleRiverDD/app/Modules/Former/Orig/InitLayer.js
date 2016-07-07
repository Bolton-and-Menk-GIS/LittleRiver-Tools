// FEATURE LAYER INSTANTIATION WRAPPER
var initLayer = (function(url, mode, outFields){
	console.log(url,mode,outFields)
	var _featureLayer = new esri.layers.FeatureLayer(url, {
		mode: esri.layers.FeatureLayer.MODE_ONEDEMAND,
		infoTemplate: esri.layers.featureLayerInfoTemplate,
		outFields: ["*"]
	}
	)
	return {
		featureLayer: _featureLayer
	}
})