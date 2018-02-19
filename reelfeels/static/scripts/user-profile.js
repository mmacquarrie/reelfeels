let infoType = {
    feels: "user-feels",
    content: "user-content"
}

function openTab(evt, iType) {
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
    document.getElementById(iType).style.display = "block";
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
    ['Joy', 80, "#fff176"],
    ['Sadness', 0, "#1565c0"],
    ['Disgust', 20, "#388e3c"],
    ['Anger', 0, "#d32f2f"],
    ['Fear', 0, "#8e24aa"]
];

function drawInitial() {

    var userChartTable = google.visualization.arrayToDataTable(userEmotionsData);

    userChart = new google.visualization.ColumnChart(document.getElementById('user-emotions-chart'));
    
    userChart.draw(userChartTable, chartOptions);
}

// Open default tab
document.getElementById("defaultOpen").click();