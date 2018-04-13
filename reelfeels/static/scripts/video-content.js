let statType = {
    user: "user-stats",
    general: "general-stats"
}

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

var userChart, generalChart;

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
        duration: 500,
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

var generalEmotionsData = [
    ['Emotion', 'Level', {role: "style"}],
    ['Joy', 0, "#fff176"],
    ['Sadness', 0, "#1565c0"],
    ['Disgust', 0, "#388e3c"],
    ['Anger', 0, "#d32f2f"],
    //['Fear', 0, "#8e24aa"]
    ['Surprise', 0, '#8e24aa']
];

var userChartTable, generalChartTable;

function drawInitial() {

    userChartTable = google.visualization.arrayToDataTable(userEmotionsData);
    generalChartTable = google.visualization.arrayToDataTable(generalEmotionsData);

    userChart = new google.visualization.ColumnChart(document.getElementById('user-emotions-chart'));
    generalChart = new google.visualization.ColumnChart(document.getElementById('general-emotions-chart'));
    
    //commented out initial draw for now (it doens't draw until Affectiva is ready)
    //userChart.draw(userChartTable, chartOptions);
    generalChart.draw(generalChartTable, chartOptions);
}

// Open default tab
document.getElementById("defaultOpen").click();

/***                          ***
 *** Affectiva Implementation *** 
 ***                          ***/
var divRoot = $('#affdex_elements')[0];

//get width and height from the css for this div element
var width = $('#affdex_elements').width();
var height = $('#affdex_elements').height();

var faceMode = affdex.FaceDetectorMode.LARGE_FACES;

//the emotion detector itself
var detector = new affdex.CameraDetector(divRoot, width, height, faceMode);

//we only care about the emotions
detector.detectAllEmotions();

detector.addEventListener('onInitializeSuccess', function(){
    console.log('Affectiva emotion detector successfully initialized :)')
    
    //update the user emotions chart every ms time interval
    setInterval(updateEmotionsChart, 10);
});

detector.addEventListener('onWebcamConnectSuccess', function(){
    console.log('Successfully connected to webcam :)');
});

detector.addEventListener('onWebcamConnectFailure', function(){
    console.log('Unable to connect to webcam :(');
});

//faces array contains the data processed from the webcam feed
detector.addEventListener('onImageResultsSuccess', function(faces, image, timestamp){
    if(faces.length > 0){
        //update the user emotions data (from 1 face)
        let joy = faces[0].emotions['joy'];
        let sadness = faces[0].emotions['sadness'];
        let disgust = faces[0].emotions['disgust'];
        let anger = faces[0].emotions['anger'];
        //let fear = faces[0].emotions['fear'];
        let surprise = faces[0].emotions['surprise'];

        userChartTable.setValue(0, 1, joy);
        userChartTable.setValue(1, 1, sadness);
        userChartTable.setValue(2, 1, disgust);
        userChartTable.setValue(3, 1, anger);
        //userChartTable.setValue(4, 1, fear);
        userChartTable.setValue(4, 1, surprise);

        /*
        userEmotionsData[1] = ['Joy', joy, "#fff176"];
        userEmotionsData[2] = ['Sadness', sadness, "#1565c0"];
        userEmotionsData[3] = ['Disgust', disgust, "#388e3c"];
        userEmotionsData[4] = ['Anger', anger, "#d32f2f"];
        userEmotionsData[5] = ['Fear', fear, "#8e24aa"];
        */
    }       
});

var updateEmotionsChart = function(){
    //let userChartTable = google.visualization.arrayToDataTable(userEmotionsData);
    userChart.draw(userChartTable, chartOptions);
}

//start the detector
$(document).ready(function(){
    detector.start();
    //hide the face cam
    $('#affdex_elements').hide();
});