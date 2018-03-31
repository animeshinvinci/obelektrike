function addFavorite(a) {
    var title = document.title;
    var url = document.location;
    try {
        // Internet Explorer
        window.external.AddFavorite(url, title);
    }
    catch (e) {
        try {
            // Mozilla
            window.sidebar.addPanel(title, url, "");
        }
        catch (e) {
            // Opera
            if (typeof(opera)=="object" || window.sidebar) {
                a.rel="sidebar";
                a.title=title;
                a.url=url;
                a.href=url;
                return true;
            }
            else {
                // Unknown
                alert('Нажмите Ctrl-D чтобы добавить страницу в закладки');
            }
        }
    }
    return false;
}


$(function() {
    var source_link = '<p>Источник: <a href="' + location.href + '">' + location.href + '</a></p>';
    if (window.getSelection) $('.post-data-copy').bind(
        'copy',
        function()
        {
            var selection = window.getSelection();
            var range = selection.getRangeAt(0);

            var magic_div = $('<div>').css({ overflow : 'hidden', width: '1px', height : '1px', position : 'absolute', top: '-10000px', left : '-10000px' });
            magic_div.append(range.cloneContents(), source_link);
            $('body').append(magic_div);

            var cloned_range = range.cloneRange();
            selection.removeAllRanges();

            var new_range = document.createRange();
            new_range.selectNode(magic_div.get(0));
            selection.addRange(new_range);

            window.setTimeout(
                function()
                {
                    selection.removeAllRanges();
                    selection.addRange(cloned_range);
                    magic_div.remove();
                }, 0
            );
        }
    );

    var start = $('#bottom-right').offset().top;
    $(window).scroll(function(){
        var windowTop = $(window).scrollTop();
        if (start < windowTop) {
            var height = window.innerHeight;
            $('.right-rek').css('position', 'fixed');
            $('.right-rek').css('top', 10);
        } else {
            $('.right-rek').css('position', 'relative');
            $('.right-rek').css('top', 0);
        }
    });

});