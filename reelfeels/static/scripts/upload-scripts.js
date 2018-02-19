//runs on page load
$(document).ready(function(){
    //set up click function
    $(".form-group").on('click', '#upload-next-button', validateYouTubeUrl);
    
    //(doesn't really work...) do same thing when pressing enter
    $("#video-url-input").keyup(function(event){
        //if 'enter' key pressed
        if(event.keyCode === 13)
        {
            $("#upload-next-button").click();
        }
    });

    $("#upload-form fieldset:not(:first-of-type)").hide();
    ///$("#upload-form fieldset").css("background-color", "red");
});

//script for validating YouTube URLs and replacing embedded src with new url
//SOURCE: https://stackoverflow.com/a/28735569
function validateYouTubeUrl(){
    var url = $('#video-url-input').val();
    if (url != undefined || url != '') {
        var regExp = /^.*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|\&v=|\?v=)([^#\&\?]*).*/;
        var match = url.match(regExp);
        if (match && match[2].length == 11) {
            //valid url
            $('#video-preview').attr('src', 'https://www.youtube.com/embed/' + match[2] + '?autoplay=0');
    
            //animate the form now that a valid URL was input
            formAnimate();
        }
        else {
            //invalid url
            alert("Invalid YouTube URL.");
        }
    }
}

//formAnimate function for animating page transitions in a multistep form
//SOURCE: https://codepen.io/designify-me/pen/qrJWpG

//vars for formAnimate
var current_fs, next_fs, previous_fs; //fieldsets
var left, opacity, scale; //fieldset properties which we will animate
var animating; //flag to prevent quick multi-click glitches

function formAnimate(){
    $("#upload-next-button").click(function(){
        if(animating) return false;
        animating = true;
    
        current_fs = $(this).closest("fieldset");
        next_fs = $(this).closest("fieldset").next();

        //activate next step on progressbar using the index of next_fs
        //$("#progressbar li").eq($("fieldset").index(next_fs)).addClass("active");

        //show the next fieldset
        next_fs.show(); 
        //hide the current fieldset with style
        current_fs.animate({opacity: 0}, {
            step: function(now, mx) {
                //as the opacity of current_fs reduces to 0 - stored in "now"
                //1. scale current_fs down to 80%
                scale = 1 - (1 - now) * 0.2;
                //2. bring next_fs from the right(50%)
                left = (now * 50)+"%";
                //3. increase opacity of next_fs to 1 as it moves in
                opacity = 1 - now;
                current_fs.css({
                    'transform': 'scale('+scale+')',
                    'position': 'absolute'
                });
                next_fs.css({'left': left, 'opacity': opacity});
            },
            duration: 800, 
            complete: function(){
                current_fs.hide();
                animating = false;
            }, 
            //this comes from the custom easing plugin
            easing: 'easeInOutBack'
        });
    });

    $(".previous").click(function(){
        if(animating) return false;
        animating = true;

        current_fs = $(this).parent();
        previous_fs = $(this).parent().prev();

        //de-activate current step on progressbar
        //$("#progressbar li").eq($("fieldset").index(current_fs)).removeClass("active");

        //show the previous fieldset
        previous_fs.show(); 
        //hide the current fieldset with style
        current_fs.animate({opacity: 0}, {
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
    });

    //used <a> instead
    //$("#upload-submit-button").click(function(){
        //return false;
    //})
}