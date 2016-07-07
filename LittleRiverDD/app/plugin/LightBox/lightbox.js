function LightBox(content, closeTrigger){

    if($('#lightbox').length == 1){  
    $('#lightbox').show();
        // $('#lightbox').remove();
        // content.remove();
    }
    else{
    var lightBox = $('<div id="lightbox"></div>');

    // :::: STYLE LIGHTBOX ELEMENTS ::::

    lightBox.css({
        'position': 'fixed',
        'background-image': 'url(../plugin/LightBox/overlay.png)',
        'top': 0,
        'left': 0,
        'width': '100%',
        'height': '100%',
        'background-color': '#000',
        'opacity': '0.8',
        'text-align': 'center',
        'display': 'none'
    });

    // :::: STYLE LIGHTBOX ELEMENTS ::::

    $('body').append(lightBox);
    $(lightBox).after(content);
    content.show();
    // content.append('<span id="liBox-close">x</span>')
    
    var positionLightbox = function() {
        var viewWidth = $(window).width(),
        liBoxContentMargin = (viewWidth / 2) - 148,
        viewHeight = $(window).height();
        liBoxContentHeight = (viewHeight/2)
        liBoxContent = $(content),

        liBoxContent.css({
            // 'left' : liBoxContentMargin,
            'left': '280px',
            'top' : $(window).scrollTop() + -500 + 'px'
        });
    };

    console.log('LB: ', $(window).scrollTop())

    lightBox.fadeIn(function() {
        console.log('NOTHING?', content)
        content.show();                               
    });
    positionLightbox();

    $('#liBox-close').click(function() {
        lightBox.hide();
        content.hide();
    });
    /*hide click outside*/
    var closeElement = document
    if (closeTrigger){
        console.log("WHATS CLOSE TRIGGER?", closeTrigger)
    closeElement = closeTrigger;
    }

    $(closeElement).mouseup(function (e)
    {
    if (!content.is(e.target) // if the target of the click isn't the container...
        && content.has(e.target).length === 0) // ... nor a descendant of the container
    {
        lightBox.hide();
        content.hide();
        // content.remove();
    }
  });
}
  }
