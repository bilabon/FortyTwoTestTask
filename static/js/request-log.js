$(document).ready(function() {
    // Show last 10 http requests that are stored by middleware
    // This page should update asynchronously as new requests come in, updating page header as well. 
    // If there are N new requests, page title should start with (N).
    // As page is viewed by user, all requests should be considered as read and the title should return to the initial state.

    var title = document.title;

    function HandleVisibility(viewed) {
        console.log(viewed);
        $.ajax({
            type: 'GET',
            url: '/request-count/',
            data: {
                'viewed': viewed
            },
            error: function(data) {
                console.log('Some error happened (function GetData)');
                console.log(data);
            },
            success: function(data) {
                console.log(data['object_list']);
                $.each(data['object_list'], function(index, value) {
                    var li = $('.list-unstyled > li:eq(' + index + ')');
                    li.find('.obj-id').html(value['id']);
                    li.find('.obj-priority').html('Priority: ' + value['priority']);
                    li.find('.obj-title').html(value['title']);
                    li.find('.obj-timestamp').html(value['timestamp']);
                    var viewed_html = viewed ? 'True' : 'False';
                    li.find('.obj-viewed').html(viewed_html);
                });

                count = data['request_count'];
                console.log(count);
                document.title = (!viewed & count > 0) ? '(' + count + ') ' + title : title;

            }
        });
    }

    setInterval(function() {
        HandleVisibility(!Visibility.hidden());
    }, 1000);

});
