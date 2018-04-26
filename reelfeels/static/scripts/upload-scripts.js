//runs on page load
$(document).ready(function(){
    //focus cursor in URL field on page load
    $("#video-url-input").focus();

    //binds function to 'Next' button click
    $("body").on("click", "#upload-next-button", validateYouTubeUrl);

    //pressing enter replicates clicking 'Next'
    $("#video-url-input").keyup(function(event){
        //if 'enter' key pressed
        if(event.keyCode === 13)
        {
            $("#upload-next-button").click();
        }
    });

    //binds function to 'Previous' button click
    $("body").on("click", "#upload-previous-button", function(){
        toggleForm();
    });

    //really strange bug that requires this input to exist in order for 'enter' key to work...
    $("#bug").hide();

    //have video-url-input (text field) give its 'name' to the hidden input field so that the hidden input is the one submitted when user clicks submit (instead of the user text input field) (needs to be done to submit just the video code part of the YouTube url instead of the entire link)
    $('#video-url-code').attr('name', $('#video-url-input').attr('name'));
    $('#video-url-input').attr('name', '');
});

//script for validating YouTube URLs and replacing embedded src with new url
//SOURCE (modified): https://stackoverflow.com/a/28735569
function validateYouTubeUrl(){
    var url = $('#video-url-input').val();
    if (url != undefined || url != '') {
        var regExp = /^.*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|\&v=|\?v=)([^#\&\?]*).*/;
        var match = url.match(regExp);
        if (match && match[2].length == 11) {   
             $("#video-preview").attr("src", "https://www.youtube.com/embed/" + match[2] + "?autoplay=0");

            //for passing YouTube video code to the Django form to be handled
            $('#video-url-code').attr('value', match[2]);

            //toggle the form now that a valid URL was input
            toggleForm();
        }
        else {
            //invalid url
            alert("Invalid YouTube URL.");
        }
    }
}

//var for tracking which page you're on for toggle function
var fsNum = 1;

//toggle between the two pages of the form
function toggleForm(){
    //if 'next' button was clicked
    if(fsNum === 1){
        fsNum = 2;

        //hide URL form fieldset
        $("#fs1").hide();

        //show the preview fieldset
        $("#fs2").show();
    }
    //else if 'previous' button was clicked
    else{
        fsNum = 1;

        //hide preview fieldset
        $("#fs2").hide();

        //reset src
        $("#video-preview").attr("src", "");

        //show the url form fieldset
        $("#fs1").show();
    }
}