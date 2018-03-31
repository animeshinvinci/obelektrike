$(".like-post-action").click(function(){
    var self = $(this);
    var id = self.attr("data");
    var data = {
        pk:id
    };
    $.ajax({
        type: "POST",
        url: likePostUrl,
        data: data,
        success:function(data){
            var rate = data.rate;
            if (rate) {
                self.off()
                self.parent().find('.unlike-post-action').off();
                self.removeClass('like-post-action');
                self.parent().find('.unlike-post-action').removeClass('unlike-post-action');
                self.parent().find('.like-rate').html(rate);
            }
        }
    });
});

$(".unlike-post-action").click(function(){
    var self = $(this);
    var id = self.attr("data");
    var data = {
        pk:id
    };
    $.ajax({
        type: "POST",
        url: unlikePostUrl,
        data: data,
        success:function(data){
            var rate = data.rate;
            if (rate) {
                self.parent().find('.like-post-action').off();
                self.off()
                self.parent().find('.like-post-action').removeClass('like-post-action');
                self.removeClass('unlike-post-action');
                self.parent().find('.like-rate').html(rate);
            }
        }
    });
});
