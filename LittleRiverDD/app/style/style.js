var Reset = (function(){

return {
	tableWidth: function(){
		$('.srchTbl').children().css('min-width','55px')
		$('#srchHeader').children().css('width','10%')
		$('#srchRslt').css('border-radius','0px').css('border-bottom-left-radius','0.4em').css('border-bottom-right-radius','0.4em')
	},
	resize: function(){
		var winWidth = $(window).width();
		//    case (winWidth <= 375):

	}
}
})();

//#srchHeader.css('height') > 50px