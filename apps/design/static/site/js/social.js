$(function() {
    $(window).scroll(function(){
        var windowTop = $(window).scrollTop();
        var startSocial = $('#start-social').offset().top;
        var endSocial = $('#end-social').offset().top;

        if (endSocial < windowTop) {
            $('#social').hide();
        } else {
            $('#social').fadeIn();
        } 
        if (startSocial < windowTop) {
            var height = window.innerHeight;
            $('#social').css('top', windowTop - 200);
        } else {
            $('#social').css('top', "");
        }
    });
});