//runs on page load
$(document).ready(function(){
    //set up click function
    $("#fs1").on('click', '#upload-next-button', validateYouTubeUrl);
    
    //(doesn't really work...) do same thing when pressing enter
    $("#video-url-input").keyup(function(event){
        //if 'enter' key pressed
        if(event.keyCode === 13)
        {
            $("#upload-next-button").click();
        }
    });
});

//script for validating YouTube URLs and replacing embedded src with new url
//SOURCE (modified): https://stackoverflow.com/a/28735569
function validateYouTubeUrl(){
    var url = $('#video-url-input').val();
    if (url != undefined || url != '') {
        var regExp = /^.*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|\&v=|\?v=)([^#\&\?]*).*/;
        var match = url.match(regExp);
        if (match && match[2].length == 11) {
             $('#video-preview').attr('src', 'https://www.youtube.com/embed/' + match[2] + '?autoplay=0');
            //animate the form now that a valid URL was input
            formAnimate(1);           
        }
        else {
            //invalid url
            alert("Invalid YouTube URL.");
        }
    }
}

//formAnimate function for animating page transitions in a multistep form
//SOURCE (modified): https://codepen.io/designify-me/pen/qrJWpG

//vars for formAnimate
var left, opacity, scale; //fieldset properties which we will animate
var animating; //flag to prevent quick multi-click glitches

function formAnimate(fsNum){
    if(fsNum === 1){
        if(animating) return false;
        animating = true;

        //show the preview fieldset
        $("#fs2").show();
      
        $("#fs1").hide();

        //hide the current fieldset with style
        $("#fs1").animate({opacity: 0}, {
            step: function(now, mx) {
                //as the opacity of current_fs reduces to 0 - stored in "now"
                //1. scale current_fs down to 80%
                scale = 1 - (1 - now) * 0.2;
                //2. bring next_fs from the right(50%)
                left = (now * 50)+"%";
                //3. increase opacity of next_fs to 1 as it moves in
                opacity = 1 - now;
                $("#fs1").css({
                    'transform': 'scale('+scale+')',
                    'position': 'absolute'
                });
                $("#fs2").css({'left': left, 'opacity': opacity});
            },
            duration: 800, 
            complete: function(){
                $("#fs1").hide();
                animating = false;
            }, 
            //this comes from the custom easing plugin
            easing: 'easeInOutBack'
        });
    }
    //else if 'previous' button is clicked...
    else{
        if(animating) return false;
        animating = true;

        current_fs = $("#fs2");
        previous_fs = $("#fs1");

        //show the URL input fieldset
        $("#fs1").show(); 
        //hide the current fieldset with style
        $("#fs2").animate({opacity: 0}, {
            step: function(now, mx) {
                //as the opacity of current_fs reduces to 0 - stored in "now"
                //1. scale previous_fs from 80% to 100%
                scale = 0.8 + (1 - now) * 0.2;
                //2. take current_fs to the right(50%) - from 0%
                left = ((1-now) * 50)+"%";
                //3. increase opacity of previous_fs to 1 as it moves in
                opacity = 1 - now;
                current_fs.css({'left': left});
                previous_fs.css({'transform': 'scale('+scale+')', 'opacity': opacity});
            }, 
            duration: 800, 
            complete: function(){
                current_fs.hide();
                animating = false;
            }, 
            //this comes from the custom easing plugin
            easing: 'easeInOutBack'
        });
    }
}