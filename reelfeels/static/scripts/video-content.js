let statType = {
    user: "user-stats",
    general: "general-stats",
    user_history: "user_history-stats"
}

//store boolean that's true if the user_history-stats div exists; false otherwise
var previouslyViewed = ($('#user_history-stats').length > 0);

//adjust the css if the third tab needs to be there (which is also if previouslyViewed is true)
if (previouslyViewed) {
    $('.tab button.tablinks').css('width', '33%');
}

//keep track of whether there's a face detected
var faceDetected = false;

function openStats(evt, sType) {
    var i, tabcontent, tablinks;

    // Initially hide all the tabs
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }

    // Remove the 'active' class
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }

    // Show the selected tab and make it active
    document.getElementById(sType).style.display = "block";
    evt.currentTarget.className += " active";
}

// Chart for emotions
google.charts.load('current', {'packages':['corechart', 'bar']});
google.charts.setOnLoadCallback(drawInitial);

var userChart, generalChart, userHistoricalChart;

var chartOptions = {
    title : 'Emotion Probabilities',
    vAxis: {
        title: 'Probability',
        maxValue: 100,
        minValue: 0,
        viewWindowMode: 'maximized'
    },
    legend:{
        position: 'none'
    },
    seriesType: 'bars',
    series: {5: {type: 'line'}},
    animation: {
        startup: true,
        duration: 25,
        easing: "out",

    }
};

var userEmotionsData = [
    ['Emotion', 'Level', {role: "style"}],
    ['Joy', 0, "#fff176"],
    ['Sadness', 0, "#1565c0"],
    ['Disgust', 0, "#388e3c"],
    ['Anger', 0, "#d32f2f"],
    //['Fear', 0, "#8e24aa"]
    ['Surprise', 0, '#8e24aa']
];

//get global data from template
var generalEmotionsData = [
    ['Emotion', 'Level', {role: "style"}],
    ['Joy', parseInt($('#global-happiness').html()), "#fff176"],
    ['Sadness', parseInt($('#global-sadness').html()), "#1565c0"],
    ['Disgust', parseInt($('#global-disgust').html()), "#388e3c"],
    ['Anger', parseInt($('#global-anger').html()), "#d32f2f"],
    //['Fear', 30, "#8e24aa"]
    ['Surprise', parseInt($('#global-surprise').html()), '#8e24aa']
];

//get user's past view data from template if a past view exists
if (previouslyViewed) {
    //normalize the stats so they're all real percentages
    let past_joy = parseInt($('#user-past-happiness').html());
    let past_sadness = parseInt($('#user-past-sadness').html());
    let past_disgust = parseInt($('#user-past-disgust').html());
    let past_anger = parseInt($('#user-past-anger').html());
    let past_surprise = parseInt($('#user-past-surprise').html());

    let past_sum = past_joy + past_sadness + past_disgust + past_anger + past_surprise;
    past_joy = (past_joy/past_sum) * 100;
    past_sadness = (past_sadness/past_sum) * 100;
    past_disgust = (past_disgust/past_sum) * 100;
    past_anger = (past_anger/past_sum) * 100;
    past_surprise = (past_surprise/past_sum) * 100;

    $('#user-past-happiness').html(Math.round(past_joy));
    $('#user-past-sadness').html(Math.round(past_sadness));
    $('#user-past-disgust').html(Math.round(past_disgust));
    $('#user-past-anger').html(Math.round(past_anger));
    $('#user-past-surprise').html(Math.round(past_surprise));
    

    var userHistoricalEmotionsData = [
        ['Emotion', 'Level', {role: "style"}],
        ['Joy', past_joy, "#fff176"],
        ['Sadness', past_sadness, "#1565c0"],
        ['Disgust', past_disgust, "#388e3c"],
        ['Anger', past_anger, "#d32f2f"],
        ['Surprise', past_surprise, '#8e24aa']
    ]
}

var userChartTable, generalChartTable, userHistoricalChartTable;

function drawInitial() {

    userChartTable = google.visualization.arrayToDataTable(userEmotionsData);
    generalChartTable = google.visualization.arrayToDataTable(generalEmotionsData);

    userChart = new google.visualization.ColumnChart(document.getElementById('user-emotions-chart'));
    generalChart = new google.visualization.ColumnChart(document.getElementById('general-emotions-chart'));
    
    userChart.draw(userChartTable, chartOptions);
    generalChart.draw(generalChartTable, chartOptions);

    //render the user's past stats if they exist
    if (previouslyViewed) {
        userHistoricalChartTable = google.visualization.arrayToDataTable(userHistoricalEmotionsData);
        userHistoricalChart = new google.visualization.ColumnChart(document.getElementById('user-historical-emotions-chart'));
        userHistoricalChart.draw(userHistoricalChartTable, chartOptions);
    }
}

// Open default tab
document.getElementById("defaultOpen").click();

/** --- Affectiva Implementation --- **/

var divRoot = $('#affdex_elements')[0];

//get width and height from the css for this div element (kind of irrelevant since the cam feed is hidden, but required)
var width = $('#affdex_elements').width();
var height = $('#affdex_elements').height();

var faceMode = affdex.FaceDetectorMode.LARGE_FACES;

//the emotion detector itself
var detector = new affdex.CameraDetector(divRoot, width, height, faceMode);

//we only care about the emotions
detector.detectAllEmotions();

//this event is when Affecitva is ready
detector.addEventListener('onInitializeSuccess', function(){
    //console.log('Affectiva emotion detector successfully initialized :)')
    
    //start updating the current emotions chart every 'chart_draw_interval' milliseonds
    let chart_draw_interval = 15;
    setInterval(
        function(){
            userChart.draw(userChartTable, chartOptions);
        },
        chart_draw_interval
    );
});

detector.addEventListener('onWebcamConnectSuccess', function(){
    //console.log('Successfully connected to webcam :)');
});

detector.addEventListener('onWebcamConnectFailure', function(){
    //console.log('Unable to connect to webcam :(');
    alert("Couldn't access a webcam :'(");
});

var videoPlaying = false;
let joy=0, sadness=0, disgust=0, anger=0, surprise=0;

//faces array contains the data processed from the webcam feed
detector.addEventListener('onImageResultsSuccess', function(faces, image, timestamp){
    if(faces.length > 0) {
        faceDetected = true;

        //update the user emotions data (from 1 face)
        joy = Math.round(faces[0].emotions['joy']);
        sadness = Math.round(faces[0].emotions['sadness']);
        disgust = Math.round(faces[0].emotions['disgust']);
        anger = Math.round(faces[0].emotions['anger']);
        surprise = Math.round(faces[0].emotions['surprise']);

        userChartTable.setValue(0, 1, joy);
        userChartTable.setValue(1, 1, sadness);
        userChartTable.setValue(2, 1, disgust);
        userChartTable.setValue(3, 1, anger);
        userChartTable.setValue(4, 1, surprise);

        if (videoPlaying) {
            //update numbers display
            $('#user-joy').html(joy + '%');
            $('#user-sadness').html(sadness + '%');
            $('#user-disgust').html(disgust + '%');
            $('#user-anger').html(anger + '%');
            $('#user-surprise').html(surprise + '%');
        }
    }
    // Tell user no faces detected if no faces are detected
    else if(faces.length == 0){
        faceDetected = false;

        $('#user-joy').html('<i>...</i>');
        $('#user-sadness').html('<i>...</i>');
        $('#user-disgust').html('<i>No face detected :(</i>');
        $('#user-anger').html('<i>...</i>');
        $('#user-surprise').html('<i>...</i>');
    }
    
    // Set number displays to 'Paused' when video is not playing
    if(!videoPlaying){
        $('#user-joy').html('<i>...</i>');
        $('#user-sadness').html('<i>...</i>');
        $('#user-disgust').html('<i>Paused</i>');
        $('#user-anger').html('<i>...</i>');
        $('#user-surprise').html('<i>...</i>');
    }
});

// getCookie function for sending AJAX request with proper Django CSRF protection (from Django docs: https://docs.djangoproject.com/en/2.0/ref/csrf/)
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Store the CSRF token cookie in a global variable
var csrftoken = getCookie('csrftoken');

// For ajaxSetup below (also from https://docs.djangoproject.com/en/2.0/ref/csrf/)
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

// On page load
$(document).ready(function(){
    //start the detector
    detector.start();

    //hide the face cam (div)
    $('#affdex_elements').hide();

    // Loads the IFrame Player API code asynchronously (from https://stackoverflow.com/a/30991021 and/or Google's YouTube Iframe Player API reference pages)
    let tag = document.createElement('script');
    tag.src = "https://www.youtube.com/iframe_api";
    let firstScriptTag = document.getElementsByTagName('script')[0];
    firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

    // Further jQuery AJAX setup with CSRF token (also from https://docs.djangoproject.com/en/2.0/ref/csrf/)    
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    // Send emotion data to server via AJAX request every 'emotion_data_send_interval' milliseconds
    /* Is setInterval a good way to set the timing for this??? */
    let emotion_data_send_interval = 1000; //change this interval???
    setInterval(
        ajax_send_emotion_data,
        emotion_data_send_interval
    );
});

// function encapsulating the ajax request to send emotion data to the server (processed in the video-content view function)
function ajax_send_emotion_data(){
    // only send data if the video is playing and a face is currenty detected
    if(videoPlaying && faceDetected){
        $.ajax({
            url : window.location.href, //the current url
            type : "POST",
            data : {
                //'csrfmiddlewaretoken' : csrftoken, //I don't think this needs to be here, as it appears to be handled in the ajaxSetup function (?)
                'joy' : joy,
                'sadness' : sadness,
                'disgust' : disgust,
                'anger' : anger,
                'surprise' : surprise
            },
            success : function(json) {
                //console.log(json); // log the returned json to the console
                //console.log("AJAX success");
            },
            // handle a non-successful response
            error : function(xhr,errmsg,err) {
                //console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
                //console.log('AJAX error');
            }
        });
    }
}


// Use the YouTube Iframe API to detect whether the video is currently playing
let player;
function onYouTubeIframeAPIReady() {
    player = new YT.Player('player', {
        events: {
            'onReady': onPlayerReady,
            'onStateChange': onPlayerStateChange
        }
    });
}

// This function runs when the Iframe YouTube player is ready/initialized
function onPlayerReady(event){  
    //event.target.playVideo();
    //un-comment above if you want video to play immediately on page load (other options available too if we need to do anything to the video iframe on page load...)
}

// This function runs when the player changes between playing and paused
function onPlayerStateChange(event) {
    if(event.data === YT.PlayerState.PLAYING) {
        //mark the boolean as true so we know the video is currently playing
        videoPlaying = true;
    }
    else{
        videoPlaying = false;
    }
}