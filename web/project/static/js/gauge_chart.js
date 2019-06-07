$(document).ready(function() {
        namespace = '/device_reading';
        var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port + namespace);
        socket.on('sensor_reading', function(msg) {
            console.log('do you see me')
            if (msg.lamp == 1) {
                document.getElementById("container-light").style.background = '#FFFF88';
                $('#container-light').text('Light is on! \n last changed: ' + timeStamp(msg.lamp_dt)).html();
            }
            else if (msg.lamp == 0) {
                document.getElementById("container-light").style.background = '#003366';
                document.getElementById("container-light").style.color = '#FFFFFF';
                $('#container-light').text('light is off \n last changed: ' + timeStamp(msg.lamp_dt)).html();  
            }
            else {
                $('#container-light').text('¯\\_(ツ)_/¯ \n last changed: ' + timeStamp(msg.lamp_dt)).html();
            }
        });
        socket.on('test_emit', function(){
            console.log('this is a message from the other side ~~~~~~')
        })
    });

var gaugeOptions = {
    chart: {
        type: 'solidgauge'
    },

    title: null,

    pane: {
        center: ['50%', '85%'],
        size: '140%',
        startAngle: -90,
        endAngle: 90,
        background: {
            backgroundColor: (Highcharts.theme && Highcharts.theme.background2) || '#EEE',
            innerRadius: '60%',
            outerRadius: '100%',
            shape: 'arc'
        }
    },

    tooltip: {
        enabled: false
    },

    // the value axis
    yAxis: {
        stops: [
            [0.1, '#55BF3B'], // green
            [0.5, '#DDDF0D'], // yellow
            [0.9, '#DF5353'] // red
        ],
        lineWidth: 0,
        minorTickInterval: null,
        tickAmount: 2,
        title: {
            y: -70
        },
        labels: {
            y: 16
        }
    },

    plotOptions: {
        solidgauge: {
            dataLabels: {
                y: 5,
                borderWidth: 0,
                useHTML: true
            }
        }
    }
};

// The speed gauge
var chartTemp = Highcharts.chart('container-temp', Highcharts.merge(gaugeOptions, {
    yAxis: {
        min: 10,
        max: 40,
    },
    credits: {
        enabled: false
    },
    title: {
        text: 'Temperature'
    },
    subtitle:{
        text: 'last checked: ' + startingTemperatureDt
    },
    series: [{
        name: 'Temperature',
        data: [startingTemp],
        dataLabels: {
            format: '<div style="text-align:center"><span style="font-size:25px;color:' +
                ((Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black') + '">{y}</span><br/>' +
                   '<span style="font-size:12px;color:silver">ºC</span></div>'
        },
        tooltip: {
            valueSuffix: ' ºC'
        }
    }]

}));

var chartHumid = Highcharts.chart('container-humid', Highcharts.merge(gaugeOptions, {

    yAxis: {
        min: 10,
        max: 80,
    },
    title: {
        text: 'Humidity'
    },
    subtitle: {
        text: 'last checked: '+ timeStamp(startingHumidityDt)
    },
    series: [{
        name: 'Humidity',
        data: [startingHumidity],
        dataLabels: {
            format: '<div style="text-align:center"><span style="font-size:25px;color:' +
                ((Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black') + '">{y:.1f}</span><br/>' +
                   '<span style="font-size:12px;color:silver">%</span></div>'
        },
        tooltip: {
            valueSuffix: ' %'
        }
    }],
    credits: {
        enabled: false
    },

}));

var chartLightIntensity = Highcharts.chart('container-light-intensity', Highcharts.merge(gaugeOptions, {

    yAxis: {
        min: 0,
        max: 800,
    },
    title: {
        text: 'Light Intensity'
    },
    subtitle: {
        text: 'last checked: '+ timeStamp(startingLightIntensityDt)
    },
    series: [{
        name: 'Light Intensity',
        data: [startingLightIntensity],
        dataLabels: {
            format: '<div style="text-align:center"><span style="font-size:25px;color:' +
                ((Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black') + '">{y:.1f}</span><br/>' +
                   '<span style="font-size:12px;color:silver">lux</span></div>'
        },
        tooltip: {
            valueSuffix: ' lux'
        }
    }],
    credits: {
        enabled: false
    },

}));

setInterval(function() {
    var point,
        newVal,
        inc;	
    namespace = '/device_reading';
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port + namespace);
    if (chartTemp) {
    	socket.on('sensor_reading', function (msg) {
    	point = chartTemp.series[0].points[0];
        inc = msg.temperature
        newVal = point.y + inc;
        point.update(inc);
        chartTemp.setTitle(null, {text: 'last checked: ' + timeStamp(msg.temperature_dt)})
        // when a sample arrives we plot it
    });
    }
    if (chartHumid) {
    	socket.on('sensor_reading', function (msg) {
    	point = chartHumid.series[0].points[0];
        inc = msg.humidity
        newVal = point.y + inc;
        point.update(inc);
        chartHumid.setTitle(null, {text: 'last checked: ' + timeStamp(msg.humidity_dt)})
        console.log('title should have changed')
        // when a sample arrives we plot it
    });
    }
    if (chartLightIntensity) {
        socket.on('sensor_reading', function (msg) {
        point = chartLightIntensity.series[0].points[0];
        inc = msg.light_intensity
        newVal = point.y + inc;
        point.update(inc);
        chartTemp.setTitle(null, {text: 'last checked: ' + timeStamp(msg.light_intensity_dt)})
        // when a sample arrives we plot it
    });
    }

}, 2000);