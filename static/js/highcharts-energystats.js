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
        
        series: [
            {
                type: 'column',
                name: 'Erzeugter PV-Strom',
                data: list_energy_pv,
                color: '#2b908f',
                borderColor  : '#2b908f'
            },
            {
                type: 'column',
                name: 'Netzbezug',
                data: list_energy_bez,
                color: '#e74c3c',
                borderColor  : '#e74c3c'
            },
            {
                type: 'column',
                name: 'Netzeinspeisung',
                data: list_energy_einsp,
                color: '#3498db',
                borderColor  : '#3498db'
            }
        ]
    });
    $('#container2').highcharts({
        
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
            categories: ["Gesamt"],
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
        
        series: [
            {
                type: 'column',
                name: 'Erzeugter PV-Strom gesamt',
                data:  total_energy_pv,
                color: '#2b908f',
                borderColor  : '#2b908f'
            },
            {
                type: 'column',
                name: 'Netzbezug gesamt',
                data: total_energy_bez,
                color: '#e74c3c',
                borderColor  : '#e74c3c'
            },
            {
                type: 'column',
                name: 'Netzeinspeisung gesamt',
                data: total_energy_einsp,
                color: '#3498db',
                borderColor  : '#3498db'
            }
        ]
    });
    $('#container3').highcharts({
        
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
            categories: months,
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
        
        series: [
            {
                type: 'column',
                name: 'Erzeugter PV-Strom monatlich',
                data:  list_month_energy_pv,
                color: '#2b908f',
                borderColor  : '#2b908f'
            },
            {
                type: 'column',
                name: 'Netzbezug monatlich',
                data: list_month_energy_bez,
                color: '#e74c3c',
                borderColor  : '#e74c3c'
            },
            {
                type: 'column',
                name: 'Netzeinspeisung monatlich',
                data: list_month_energy_einsp,
                color: '#3498db',
                borderColor  : '#3498db'
            }
        ]
    });
});
