CKEDITOR.plugins.add( 'adverts', {
    icons: 'insadv',
    init: function (editor) {
        editor.ui.addButton('Advert', {
            command: 'insadv',
            icon: this.path + 'icons/adv.png',
            label: 'Insert advert block',
        });
        var cmd = editor.addCommand('insadv', {exec: insAdv});
    }
});

function insAdv(e) {
    var div = e.document.createElement('div');
    div.setStyle('background-color', '#8f8f8f');
    div.setStyle('text-align', 'center');
    div.setHtml('advert');
    div.addClass('advert');
    e.insertElement(div);
}
