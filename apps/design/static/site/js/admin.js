$(document).ready(function(){
    $('#id_title').syncTranslit({destination: 'id_slug'});  
    
    $('#id_title').keyup(function() {
        $('#id_seo_title').val($(this).val());
    });    
});

