
var firstPoint = secondPoint = null;

var handle_feature_usage = function(feature_data) {
	var add_list = feature_data['add'];
	var rm_list = feature_data['rm'];

	ret_html = "<ul class=\"list-group\">";
	for(var i=0; i < add_list.length; i++) {
		ret_html += "<li class=\"list-group-item-success\">" + add_list[i] + "</li>";
	}
	for(var i=0; i < rm_list.length; i++) {
		ret_html += "<li class=\"list-group-item-danger\">" + rm_list[i] + "</li>";
	}
	ret_html += "</ul>";
	return ret_html;
}

var handle_dbsc = function(dbsc_data) {
	ret_html = "<div class=\"card-deck\">";
	for(var i=0; i < dbsc_data.length; i++) {
		ret_html += "<div class=\"card\">";
		ret_html += "<div class=\"card-header\">" + dbsc_data[i]["name"] + "</div>";
		ret_html += "<div class=\"card-block\">";
		ret_html += "<ul class=\"list-group\">";
		ret_html += "<li class=\"list-group-item-success\">" + dbsc_data[i]["new"] + "</li>";
		ret_html += "<li class=\"list-group-item-danger\">" + dbsc_data[i]["old"] + "</li>";
		ret_html += "</ul></div></div>"
	}
	return ret_html + "</div>";
}

var handle_tasm = function(tasm_data) {
	var add_list = tasm_data['add'];
	var rm_list = tasm_data['rm'];

	ret_html = "<ul class=\"list-group\">";
	var i = j = 0;
	while(i < add_list.length && j < add_list.length) {
		ret_html += "<li class=\"list-group-item-success\">" + add_list[i] + "</li>";
		if(String(add_list[i]).split("::")[0] == String(rm_list[j]).split("::")[0]) {
			ret_html += "<li class=\"list-group-item-danger\">" + rm_list[j] + "</li>";
			++j;
		}
		++i;
	}
	while(i < add_list.length) {
		ret_html += "<li class=\"list-group-item-success\">" + add_list[i++] + "</li>";
	}
	while(j < rm_list.length) {
		ret_html += "<li class=\"list-group-item-danger\">" + rm_list[j++] + "</li>";
	}
	ret_html += "</ul>";
	return ret_html;
}

$(document).ready(function() {
	Highcharts.theme = {
	  "colors": ["#A9CF54", "#C23C2A", "#FFFFFF", "#979797", "#FBB829"],
	  "chart": {
	    "backgroundColor": "#242F39",
	    "style": {
	      "color": "white"
	    }
	  },
	  "legend": {
	    "enabled": true,
	    "align": "right",
	    "verticalAlign": "bottom",
	    "itemStyle": {
	      "color": "#C0C0C0"
	    },
	    "itemHoverStyle": {
	      "color": "#C0C0C0"
	    },
	    "itemHiddenStyle": {
	      "color": "#444444"
	    }
	  },
	  "title": {
	    "text": {},
	    "style": {
	      "color": "#FFFFFF"
	    }
	  },
	  "tooltip": {
	    "backgroundColor": "#1C242D",
	    "borderColor": "#1C242D",
	    "borderWidth": 1,
	    "borderRadius": 0,
	    "style": {
	      "color": "#FFFFFF"
	    }
	  },
	  "subtitle": {
	    "style": {
	      "color": "#666666"
	    }
	  },
	  "xAxis": {
	    "gridLineColor": "#2E3740",
	    "gridLineWidth": 1,
	    "labels": {
	      "style": {
	        "color": "#525252"
	      }
	    },
	    "lineColor": "#2E3740",
	    "tickColor": "#2E3740",
	    "title": {
	      "style": {
	        "color": "#FFFFFF"
	      },
	      "text": {}
	    }
	  },
	  "yAxis": {
	    "gridLineColor": "#2E3740",
	    "gridLineWidth": 1,
	    "labels": {
	      "style": {
	        "color": "#525252"
	      },
	      "lineColor": "#2E3740",
	      "tickColor": "#2E3740",
	      "title": {
	        "style": {
	          "color": "#FFFFFF"
	        },
	        "text": {}
	      }
	    }
	  }
	};
	Highcharts.setOptions(Highcharts.theme);

	var scatterplot = $('#scatterplot').highcharts({
	    chartID: "scatter1",
			title: {
				text: "Query Guru",
				align: "center"
			},
	    tooltip: {
        formatter: function() {
					var ret = "<b>" + this.series.name + "</b><br/>";
					ret += "StartTime: " + Highcharts.dateFormat('%Y-%m-%d %H:%M:%S', this.x) + "<br/>";
					ret += "Duration: " + this.y + " minutes<br/>";
					ret += "Run ID: " + this.point.run_id + "<br/>";
					return ret;
        }
      },
	    chart: {
        type: 'scatter',
        zoomType: 'xy',
				height: screen.height*0.5
	    },
	    xAxis: {
				title: {
					text: "Run time"
				},
				type: 'datetime',
        	labels: {
	          formatter: function() {
	            return Highcharts.dateFormat('%b %d %H:%M', this.value);
	          }
      	}
	    },
	    yAxis: {
        title: {
          text: "Run duration (min)"
        }
	    },
			legend: {
        layout: 'vertical',
        align: 'left',
        verticalAlign: 'top',
        floating: false,
        backgroundColor: (Highcharts.theme && Highcharts.theme.legendBackgroundColor) || '#FFF',
        borderWidth: 1
	    },
			plotOptions: {
        scatter: {
					lineWidth:2,
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
                enabled: true
              }
            }
          },
        },
				series: {
					visible: false,
					allowPointSelect: true,
					marker: {
          	states: {
            	select: {
                fillColor: 'red',
                lineWidth: 0
              }
          	}
        	},
					point: {
						events: {
							click: function(e) {
								var details_fn = function(obj) {
									var details_list = "<ul>";
									details_list += "<li>Collect Timestamp: " + Highcharts.dateFormat('%Y-%m-%d %H:%M:%S', obj.x) + "</li>";
									details_list += "<li>Run Duration: " + obj.y + " minutes</li>";
									details_list += "<li>Run ID: " + obj.run_id + "</li>";
									details_list += "<li>Run Number: " + obj.run_num + "</li>";
									details_list += "</ul>"
									return details_list;
								}
								if(firstPoint == null) {
									firstPoint = this;
									$('#query1').text(this.series.name + " (" + this.run_num + ")");
									$('#query1_details').html(details_fn(this));
								}
								else if(secondPoint == null) {
									secondPoint = this;
									$('#query2').text(this.series.name + " (" + this.run_num + ")");
									$('#query2_details').html(details_fn(this));
									$('#dbsc').html("<i class=\"fa fa-spinner fa-spin\" style=\"font-size:24px\"></i>");
									$('#feature').html("<i class=\"fa fa-spinner fa-spin\" style=\"font-size:24px\"></i>");
									$('#tasm').html("<i class=\"fa fa-spinner fa-spin\" style=\"font-size:24px\"></i>");

									$.post("/tasm", {
											tasm_file1: firstPoint.tasm_file,
											tasm_file2: secondPoint.tasm_file
									}, function(data) {
										$('#tasm').html(handle_tasm(data));
									});

									$.post("/feature", {
											run_id1: firstPoint.run_id,
											run_id2: secondPoint.run_id
									}, function(data) {
										$('#feature').html(handle_feature_usage(data));
									});

									$.post("/dbsc", {
											run_id1: firstPoint.run_id,
											run_id2: secondPoint.run_id
									}, function(data) {
										$('#dbsc').html(handle_dbsc(data));
									});

								}
								else {
									secondPoint = null;
									firstPoint = this;
									$('#query2').text("SELECT A POINT");
									$('#query2_details').text("");
									$('#query1').text(this.series.name + " (" + this.run_num + ")");
									$('#query1_details').html(details_fn(this));
									$('#dbsc').html("");
									$('#feature').html("");
									$('#tasm').html("");
								}
							}
						}
					}
				}
    },
		series: series
	});
});
