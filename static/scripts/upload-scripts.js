$(document).ready(function(){
    $("h3").hide();
    //set up click function
    $(".form-group").on('click', '#test-preview-button', validateYouTubeUrl);
});

//SOURCE: https://stackoverflow.com/a/20910296
//generates an embedded video in '#video-preview' of the link typed in '#video-url-input'
//when '#test-preview-button' is clicked
/*function preview() {
    $("h3").show();
    function generatePreview() {
        var input = $('#video-url-input').val();
        return input.replace(/(?:http:\/\/)?(?:www\.)?(?:youtube\.com|youtu\.be)\/(?:watch\?v=)?(.+)/g, '<iframe src="http://www.youtube.com/embed/$1" allowfullscreen></iframe>');
    }
    //$("#video-prev.iew").replaceWith(generatePreview());
}*/
    
//script for validating YouTube URLs and replacing src with new url
//SOURCE: https://stackoverflow.com/a/28735569
function validateYouTubeUrl(){
    var url = $('#video-url-input').val();
    if (url != undefined || url != '') {
        var regExp = /^.*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|\&v=|\?v=)([^#\&\?]*).*/;
        var match = url.match(regExp);
        if (match && match[2].length == 11) {
            // Do anything for being valid
            // if need to change the url to embed url then use below line
            $('#video-preview').attr('src', 'https://www.youtube.com/embed/' + match[2] + '?autoplay=0');

            //***TO-DO[3/4]: display embedded video preview as well as display description, tag, etc. fields
            //(the rest of the upload page)
            preview();
        }
        else {
            // Do anything for not being valid

            //***TO-DO[4/4]: display message saying it's not a valid YouTube URL, ask to enter new URL
            alert("Enter a valid YouTube video URL pls.");
        }
    }
}