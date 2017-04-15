$(document).ready(function() {
    var myChart = echarts.init(document.getElementById('main'));
    myChart.showLoading();
    $.get("/show", function(data) {
        var last_id = data.last_id;
        var nodes = data.nodes;
        var links = data.links;
        var offset = data.offset;
        
        var graph = {
            'nodes' : nodes, 
            'links' : links,
        };

        var categories = [{'name' : 'block'}, {'name' : 'island'}];
        option = {
            title: {
                text: 'blockchain',
                top: 'bottom',
                left: 'center'
            },
            tooltip: { 
                formatter: function(param){
                    param = param.data.value;
                    length_data = param.data.length;
                    data = '';
                    for(var i = 0; i < length_data; i++) {
                        data += param.data[i] + '<br/>'
                    }
                    return [
                        data,
                        'time        : ' + param.timestamp + '<br/>',
                        'prev_hash   : ' + param.prev_hash + '<br/>',
                        'merkle_root : ' + param.merkle_root + '<br/>',
                        
                    ].join('');
                },
            },
            legend: [{
                // selectedMode: 'single',
                data: categories.map(function (a) {
                    return a.name;
                })
            }],
            animation: false,
            series : [
                {
                    name: 'blockchain',
                    type: 'graph',
                    layout: 'force',
                    data: graph.nodes,
                    links: graph.links,
                    categories: categories,
                    edgeSymbol: ['circle', 'arrow'],
                    edgeSymbolSize: [4, 10],
                    roam: true,
                    label: {
                        normal: {
                            show    : true,
                        }
                    },
                    lineStyle : {
                        normal: {
                            color: 'black',
                        }
                    },       
                    force: {
                        repulsion: 1000,
                        edgeLength: [50, 100]
                    }
                }
            ]
        };

        
        myChart.hideLoading();
        myChart.setOption(option); 
        setInterval(function () {
            $.get('/new_block', {last_id : last_id, offset : offset}, 
                function(data) {
                    for(var i = 0; i < data.nodes.length; i++)
                        nodes.push(data.nodes[i]);

                    for(var i = 0; i < data.links.length; i++)
                        links.push(data.links[i]);
                    var graph = {
                        'nodes' : nodes, 
                        'links' : links,
                    };
                    last_id = data.last_id;
                    offset = data.offset;
                    myChart.setOption({
                        series: [{
                            data: graph.nodes,
                            links: graph.links,
                        }],
                    });
                });
        }, 10000);
    });
})