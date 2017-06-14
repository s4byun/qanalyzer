$(document).ready(function() {
	$('#scatterplot').highcharts({
	    chartID: "scatter1",
	    chart: {
	        type: 'scatter',
	        zoomType: 'xy',
					height: 400
	    },
	    xAxis: {
				type: 'datetime',
	        "title": {
	            enabled: true,
	            text: "Time"
	        },
					dateTimeLabelFormats: {
						millisecond: '%H:%M:%S.%L',
						second: '%H:%M:%S',
						minute: '%H:%M',
						hour: '%H:%M',
						day: '%e. %b',
						week: '%e. %b',
						month: '%b \'%y',
						year: '%Y'
					},
	        startOnTick: true,
	        endOnTick: true,
	        showLastLabel: true
	    },
	    yAxis: {
	        title: {
	            text: "Run duration (s)"
	        }
	    },
			legend: {
		        layout: 'vertical',
		        align: 'left',
		        verticalAlign: 'top',
		        x: 100,
		        y: 70,
		        floating: true,
		        backgroundColor: (Highcharts.theme && Highcharts.theme.legendBackgroundColor) || '#FFFFFF',
		        borderWidth: 1
	    },
			plotOptions: {
        scatter: {
            marker: {
                radius: 4,
                states: {
                    hover: {
                        enabled: true,
                        lineColor: 'rgb(100,100,100)'
                    }
                }
            },
            states: {
                hover: {
                    marker: {
                        enabled: false
                    }
                }
            },
            tooltip: {
                headerFormat: '<b>{series.name}</b><br>',
                pointFormat: '{point.x} , {point.y}'
            }
        }
    },
		series: [
	        {
	            "name": 'Sample Query 1 - Success',
	            "color": 'rgba(71, 206, 244, 0.5)',
	            "data": [
	                [Date.UTC(2017, 06, 13, 00, 05, 02), 10.0],
	                [Date.UTC(2017, 06, 13, 01, 10, 02), 8.1],
	                [Date.UTC(2017, 06, 13, 02, 00, 39), 9.5],
	                [Date.UTC(2017, 06, 13, 03, 23, 42), 10.2],
	                [Date.UTC(2017, 06, 13, 03, 30, 27), 8.2],
	                [Date.UTC(2017, 06, 14, 00, 17, 12), 5.2],
	                [Date.UTC(2017, 06, 14, 02, 52, 33), 6.9],
	                [Date.UTC(2017, 06, 14, 05, 39, 51), 3.0],
	                [Date.UTC(2017, 06, 15, 16, 25, 20), 4.2]
	            ]
	        },
	        {
	            "name": "Sample Query 2 - Fail",
	            "color": 'rgba(255, 0, 0, 0.5)',
	            "data": [
	                [Date.UTC(2017, 06, 13, 09, 12, 32), 20.2],
	                [Date.UTC(2017, 06, 14, 07, 05, 02), 25.2],
	                [Date.UTC(2017, 06, 15, 17, 05, 02), 31.2]
	            ]
	        }
	    	]
	});
});
