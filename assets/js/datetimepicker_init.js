$(document).ready(function(){
    $(".datewidget").datetimepicker({
        minView: 2,
        autoclose: true,
        startView: 2,
        format: 'yyyy-mm-dd'}).addClass("form-control");
});