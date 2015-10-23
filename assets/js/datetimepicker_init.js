$(document).ready(function(){
    $(".datetimepicker").datetimepicker({
        minView: 2,
        autoclose: true,
        startView: 2,
        format: 'yyyy-mm-dd'}).find('input').addClass("form-control");
});