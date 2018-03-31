$(".poll-item").click(function(){
    var self = $(this);
    var id = self.attr("data");
    var data = {
        pk:id
    };
    $.ajax({
        type: "POST",
        url: voteUrl,
        data: data,
        success:function(){
            $(".progress-data").fadeIn();
            $(".poll-data").hide();
        }
    });
});