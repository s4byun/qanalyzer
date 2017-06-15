let dbsc_file = "../../"

$(document).ready(function() {
	$('#scatterplot').highcharts({
	    chartID: "scatter1",
			title: {
					text: "Query Analyzer"
			},
        tooltip: {
                formatter: function() {
                    return  '<b>'+this.series.name+' </b>' +
                        Highcharts.dateFormat('%Y-%m-%d %H:%M:%S', this.x)
                    + ' date, ' + this.y + ' run duration';
                }
        },
	    chart: {
	        type: 'scatter',
	        zoomType: 'xy',
					width: 1000,
					height: 400
	    },
	    xAxis: {
			type: 'datetime',
            labels: {
                formatter: function() {
                    return Highcharts.dateFormat('%a %d %b %H %M', this.value);
                }
            }
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
		        floating: false,
		        backgroundColor: (Highcharts.theme && Highcharts.theme.legendBackgroundColor) || '#FFF',
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
        },
				series: {
					events: {
						click: function(e) {
							
						}
					}
				}
    },
		series: series
	});
});
