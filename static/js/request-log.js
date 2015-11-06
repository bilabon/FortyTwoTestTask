$(document).ready(function() {
    // Show last 10 http requests that are stored by middleware
    // This page should update asynchronously as new requests come in, updating page header as well. 
    // If there are N new requests, page title should start with (N).
    // As page is viewed by user, all requests should be considered as read and the title should return to the initial state.

    var title = document.title;

    function GetData() {
        $.ajax({
            type: 'GET',
            url: '/request-count/',
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
                    li.find('.obj-viewed').html('Viewed: ' + value['viewed']);
                });

                count = data['request_count'];
                console.log(count);
                if (count > 0) {
                    document.title = '(' + count + ') ' + title;
                } else {
                    document.title = title;
                }

            }
        });
    }

    setInterval(function() {
        GetData();
    }, 1000);

    // DETECT USER IS ACTIVE AND UPDATE $('.obj-viewed').html() WITH 'Viewed: True'
    function SetViewed() {
        $.ajax({
            type: 'POST',
            url: '/request-count/',
            error: function(data) {
                console.log('Some error happened (function SetViewed)');
                console.log(data);
            },
            success: function(data) {
                console.log(data);
                $('.obj-viewed').html('Viewed: True');
            }
        });
    }

    var idleState = false;
    var idleTimer = null;

    $('*').bind('mousemove click mouseup mousedown keydown keypress keyup submit change mouseenter scroll resize dblclick', function() {
        clearTimeout(idleTimer);
        if (idleState === true) {
            SetViewed();
        }
        idleState = false;
        idleTimer = setTimeout(function() {
            idleState = true;
        }, 1000);
    });

    $('body').trigger('mousemove');
    // END DETECT USER IS ACTIVE


});
