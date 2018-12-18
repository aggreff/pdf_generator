$(document).ready(function () {
        $('#upload').on('click', function (e) {
            e.preventDefault();
            resetErrors();
            toggleUploadButton(true);
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
                var fileUrl = window.location.href + 'media/' + data.filename;
                clearInterval(intervalId);
                window.open(fileUrl);
                toggleUploadButton(false);
                showSuccessMessage(fileUrl);
                clearFoormData();
            }

        },
        error: function (data) {
            clearInterval(intervalId);
            handleError(data);
        }
    });
}

function handleError(response) {
    var errorMessage = '';
    for (var key in response.responseJSON) {
        errorMessage += key + ' - ' + response.responseJSON[key];
    }
    if (response.status === 413) {
        errorMessage = 'Entity too large!';
    }
    setError(errorMessage);
    toggleUploadButton(false);
}


function resetErrors() {
    setError(null);
    $('#text-success').text(null)
}


function isValid(file, webUrl) {
    var noErrors = true;
    if (file && webUrl) {
        setError('common - Please Choose one!');
        noErrors = false;
    }
    else if (!file && !webUrl) {
        setError('common - Please provide url or HTML file!');
        noErrors = false;
    }
    if (!noErrors) {
        toggleUploadButton(false)
    }
    return noErrors;
}


function setError(text) {
    $('#error').text(text)
}


function toggleUploadButton(disable) {
    $('#upload').prop('disabled', disable);
    if (disable) {
        $('#loader').show();
        $('#button-text').hide();
    }
    else {
        $('#loader').hide();
        $('#button-text').show();
    }
}


function showSuccessMessage(fileUrl) {
    $('#text-success').text('Congratulations you can use this link within 7 days - ' + fileUrl)
}

function clearFoormData() {
    $('form :input').val('');
}
