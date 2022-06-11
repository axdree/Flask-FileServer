$(document).ready(function() {
    $('#upload-file-btn').click(function() {
        var form_data = new FormData($('#upload-file')[0]);
        $.ajax({
            xhr: function() {
                var xhr = new window.XMLHttpRequest();
                xhr.upload.addEventListener("progress", function(evt) {
                    if (evt.lengthComputable) {
                        var percentComplete = Math.round((evt.loaded / evt.total) * 100);
                        $("#progressBar").attr('aria-valuenow', percentComplete).css('width', percentComplete +"%").text(percentComplete + "%")
                    }
                }, false);
                return xhr;
            },
            type: 'POST',
            url: '/',
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            success: function(data) {
                var alphaN = /^[a-zA-Z0-9]+$/;
                if(data != "err" && alphaN.test(data) && data.length == 8){
                    window.location.href=`/link?code=${data}`;
                }else{
                    window.location.href="/";
                }
            },
            error: function(err){
                window.location.href="/";
            }
        });
    });
});