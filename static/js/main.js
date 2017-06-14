$(document).ready(function() {
	$('#scatterplot').highcharts({
	    chartID: "scatter1",
			title: {
					text: "Query Analyzer"
			},
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
		        align: 'right',
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
		series: series
	});
});
