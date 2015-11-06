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
                console.log('Some error happened (function SetViewed)' + data);
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


// CSRF
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
function sameOrigin(url) {
    // test that a given url is a same-origin URL
    // url could be relative or scheme relative or absolute
    var host = document.location.host; // host + port
    var protocol = document.location.protocol;
    var sr_origin = '//' + host;
    var origin = protocol + sr_origin;
    // Allow absolute or scheme relative URLs to same origin
    return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
        (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
        // or any other URL that isn't scheme relative or absolute i.e relative.
        !(/^(\/\/|http:|https:).*/.test(url));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
            // Send the token to same-origin, relative URLs only.
            // Send the token only if the method warrants CSRF protection
            // Using the CSRFToken value acquired earlier
            xhr.setRequestHeader('X-CSRFToken', csrftoken);
        }
    }
});
// END CSRF

});
