$(document).ready(function(){

var bar = $('.progress-bar');
var percent = $('.progress-bar');
var status = $('.sr-only');
   
$('form').ajaxForm({
    beforeSend: function() {

        // remove all errors
        $('.form-group').removeClass('has-error').find('.help-block').remove();

        // disable submit button
        $("input[type=submit]").val('Loading...').attr("disabled", "disabled");

        console.log('beforeSend');
        $("#id_avatar").replaceWith($("#id_avatar").clone());
        status.empty();
        var percentVal = '0%';
        bar.width(percentVal)
        percent.html(percentVal + ' Complete');
    },
    uploadProgress: function(event, position, total, percentComplete) {
        var percentVal = percentComplete + '%';
        bar.width(percentVal)
        percent.html(percentVal + ' Complete');
    },
    success: function(data) {
        $("input[type=submit]").removeAttr("disabled");
        var percentVal = '100%';
        bar.width(percentVal)
        percent.html(percentVal + ' Complete');
        console.log('success: ' + data);
        if (data['avatar_thumbnail']){
            $("#avatar_thumbnail").attr("src", data['avatar_thumbnail']);
            $("#avatar_container").show();
        }
    },
    error: function(data) {
        console.log(data);
        $.each($.parseJSON(data.responseText), function(key, value){
            console.log(key, value);
            $('#div_id_' + key).addClass("has-error").find('.controls').append('<p id="error_1_id_' + key + '" class="help-block"><strong>' + value + '</strong></p>')
        });
    },
    complete: function(data) {
        // enable submit button
        $("input[type=submit]").val('Update').removeAttr('disabled');

        console.log(data);
    }
}); 

});