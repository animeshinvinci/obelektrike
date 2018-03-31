

initControls = function() {
    $(".like-comment-action").off();
    $(".like-comment-action").click(function(){
        var self = $(this);
        var id = self.attr("data");
        var data = {
            pk:id
        };
        $.ajax({
            type: "POST",
            url: likeCommentUrl,
            data: data,
            success:function(data){
                var rate = data.rate;
                if (rate) {
                    self.off()
                    self.parent().find('.unlike-comment-action').off();
                    self.removeClass('like-comment-action');
                    self.parent().find('.unlike-comment-action').removeClass('unlike-comment-action');
                    self.parent().find('.like-rate').html(rate);
                }
            }
        });
    }); 

    $(".unlike-comment-action").off();
    $(".unlike-comment-action").click(function(){
        var self = $(this);
        var id = self.attr("data");
        var data = {
            pk:id
        };
        $.ajax({
            type: "POST",
            url: unlikeCommentUrl,
            data: data,
            success:function(data){
                var rate = data.rate;
                if (rate) {
                    self.parent().find('.like-comment-action').off();
                    self.off()
                    self.parent().find('.like-comment-action').removeClass('like-comment-action');
                    self.removeClass('unlike-comment-action');
                    self.parent().find('.like-rate').html(rate);
                }
            }
        });
    });

    $(".comment-answer-show").off();
    $(".comment-answer-show").click(function(){
        var self = $(this);
        var id = self.attr("data");
        $('.comment-update-form').hide();
        $('.comment-answer-form').hide();
        $('#comment-answer-form-' + id).show();
        $('.comment-answer-form').find('form').off();
        var answerForm = $('#comment-answer-form-' + id).find('form');
        answerForm.submit(function (e) {
            $.ajax({
                type: answerForm.attr('method'),
                url: answerForm.attr('action'),
                data: answerForm.serialize(),
                success: function (data) {
                    if(data.result == 'success') {
                        var dataHtml = '<ul class="media-list child"><li class="media" id="comment_' + data.id + '">' + data.html_data + '</li></ul>';
                        $('#comment-answer-form-' + data.parent_id).before(dataHtml);
                        $('#comment-answer-form-' + data.parent_id + ' textarea').val('');
                        initControls();
                    } else {
                        $('#comment-answer-form-' + id + ' .errors').html(data.data + '<br>');
                    }
                }
            });
            e.preventDefault();
        });
    });

    $('#comment-create-form-id').off();
    var createForm = $('#comment-create-form-id');
    createForm.submit(function (e) {
        $.ajax({
            type: createForm.attr('method'),
            url: createForm.attr('action'),
            data: createForm.serialize(),
            success: function (data) {
                if(data.result == 'success') {
                    $('#place-create-comment').html(data.html_data);
                    $('#place-create-comment').after('<li class="media" id="place-create-comment"></li>');
                    $('#place-create-comment').attr("id", "comment_" + data.id);
                    $('#comment-create-form-id textarea').val('');
                    initControls();
                } else {
                    $('#comment-create-form-id .errors').html(data.data + '<br>');
                }
            }
        });
        e.preventDefault();
    });
}

initControls();
