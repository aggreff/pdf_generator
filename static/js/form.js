$(document).ready(function () {
        $('#upload').on('click', function (e) {
            e.preventDefault();
            resetErrors();
            var file = $('#upload-pdf').prop('files')[0];
            var webUrl = $('#web-url').val();
            if (!isValid(file, webUrl)) return;
            var formData = new FormData();
            if (file) formData.append('file', file);
            formData.append('url', webUrl);
            $.ajax({
                url: 'api/pdf/',
                cache: false,
                contentType: false,
                processData: false,
                data: formData,
                type: 'post',
                success: function (data) {
                    handleResponse(data);
                },
                error: function (data) {
                    handleError(data);
                }
            });
        });
    }
);

var intervalId = null;

function handleResponse(response) {
    intervalId = setInterval(function () {
        checkPdfStatus(response.id)
    }, 1000);
}


function checkPdfStatus(taskId) {
    $.ajax({
        url: 'api/pdf/check_task?task_id=' + taskId,
        cache: false,
        contentType: false,
        processData: false,
        type: 'get',
        success: function (data) {
            if (data.filename) {
                clearInterval(intervalId);
                window.open(window.location.href + 'media/' + data.filename)
            }
        }
    });
}

function handleError(response) {
    var errorMessage = '';
    for (var key in response.responseJSON) {
        errorMessage += key + ' - ' + response.responseJSON[key];
    }
   setError(errorMessage);
}


function resetErrors() {
   setError(null)
}


function isValid(file, webUrl) {
    if (file && webUrl){
        setError('common - Please Choose one!');
        return false;
    }
    else if (!file  && !webUrl){
        setError('common - Please provide url or HTML file!')
        return false;
    }
    return true;
}


function setError(text) {
    $('#error').text(text)
}
