$(function () { 
    $('#container1').highcharts({
        
        colors: ["#2b908f", "#90ee7e"],
        chart: {
            backgroundColor: '#3e3e40',
        },
        title: {
            text: '',
            style: {
                display: 'none'
            }
        },
        xAxis: {
            categories: timestampList,
            gridLineColor: '#707073',
            labels: {
                style: {
                    color: '#ddd',
                    fontSize: '14px'
                }
            },
            lineColor: '#707073',
            minorGridLineColor: '#505053',
            tickColor: '#707073',
        },
        yAxis: {
            title: {
                text: 'Elektrische Energie [ kWh ]',
                style: {
                    color: '#ddd',
                    fontSize: '14px'
                }
            },
            gridLineColor: '#707073',
            labels: {
                style: {
                    color: '#ddd'
                }
            },
            lineColor: '#707073',
            minorGridLineColor: '#505053',
            tickColor: '#707073',
            tickWidth: 1,
        },
        
        legend: {
            layout: 'vertical',
            align: 'right',
            verticalAlign: 'middle',
            borderWidth: 0,
            
            itemStyle: {
                color: '#ddd'
            },
            itemHoverStyle: {
                color: '#fff'
            },
            itemHiddenStyle: {
                color: '#ddd'
            }           
        },
        
        series: [{
            type: 'column',
            name: 'Erzeugter PV-Strom',
            data: list_energy_pv,
            color: '#A33E4A',
            borderColor  : '#A33E4A'
        }]
    });
});
