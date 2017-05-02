$(document).ready(function() {
    var bc = echarts.init(document.getElementById('blockchain'));
    var network_x = echarts.init(document.getElementById('node-x'));
    var network_y = echarts.init(document.getElementById('node-y'));
    bc.showLoading();
    network_x.showLoading();
    network_y.showLoading();
    $.get("/show", function(data) {
        var last_id = data.last_id;
        var nodes = data.nodes;
        var links = data.links;
        var offset = data.offset;
        var nodes_route = data.route_nodes;
        var links_route = data.route_links;
        var nodes_route_x = data.route_nodes_x;
        var links_route_x = data.route_links_x;
        
        // blockchain
        var graph = {
            'nodes' : nodes, 
            'links' : links,
        };
        var categories = [{'name' : 'block'}, {'name' : 'island'}];
        var opt = {
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

        // route_x
        var graph_route_x = {
            'nodes' : nodes_route, 
            'links' : links_route,
        };
        var categories_route = [{'name' : 'free'}, {'name' : 'transfer'}];
        var opt_route_x = {
            title: {
                text: 'transfer',
                top: 'bottom',
                left: 'center'
            },
            tooltip: { 
                formatter: function(param){
                    param = param.data.value;
                    return [
                        param,
                    ].join('');
                },
            },
            legend: [{
                // selectedMode: 'single',
                data: categories_route.map(function (a) {
                    return a.name;
                })
            }],
            animation: false,
            series : [
                {
                    name: 'blockchain',
                    type: 'graph',
                    layout: 'force',
                    data: graph_route_x.nodes,
                    links: graph_route_x.links,
                    categories: categories_route,
                    edgeSymbol: ['circle', 'line'],
                    edgeSymbolSize: [4, 10],
                    roam: true,
                    label: {
                        normal: {
                            show    : false,
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

        // route_y
        var graph_route_y;
        var graph_route_y = {
             'nodes' : nodes_route_x, 
             'links' : links_route_x,
        };
        
        var categories_route_y = [{'name' : 'free'}, {'name' : 'mining'}];
        var opt_route_y = {
            title: {
                text: 'mining',
                top: 'bottom',
                left: 'center'
            },
            tooltip: { 
                formatter: function(param){
                    param = param.data.value;
                    return [
                        param,
                    ].join('');
                },
            },
            legend: [{
                // selectedMode: 'single',
                data: categories_route_y.map(function (a) {
                    return a.name;
                })
            }],
            animation: false,
            series : [
                {
                    name: 'blockchain',
                    type: 'graph',
                    layout: 'force',
                    data: graph_route_y.nodes,
                    links: graph_route_y.links,
                    categories: categories_route_y,
                    edgeSymbol: ['circle', 'line'],
                    edgeSymbolSize: [4, 10],
                    roam: true,
                    label: {
                        normal: {
                            show    : false,
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
        }

        bc.hideLoading();
        network_x.hideLoading();
        network_y.hideLoading();
        bc.setOption(opt); 
        network_x.setOption(opt_route_x); 
        network_y.setOption(opt_route_y); 

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
                    bc.setOption({
                        series: [{
                            data: graph.nodes,
                            links: graph.links,
                        }],
                    });
                });
        }, 5000);

        var flag_x = 0, flag_y = 0;
        setInterval(function () {
            graph_route_x.nodes[flag_x].category = 0;
            graph_route_y.nodes[flag_y].category = 0;

            $.get('/new_route_info', {}, 
                function(data) {
                    for(var i = 0; i < data.node_x.length; i++)
                        for(var j = 0; j < graph_route_x.nodes.length; j++)
                            if(graph_route_x.nodes[j].name == data.node_x[i]) {
                                graph_route_x.nodes[j].category = 1;
                                flag_x = j;
                            }
                    for(var i = 0; i < data.node_y.length; i++)
                        for(var j = 0; j < graph_route_y.nodes.length; j++)
                            if(graph_route_y.nodes[j].name == data.node_y[i]) {
                                graph_route_y.nodes[j].category = 1;
                                flag_y = j;
                            }

                    network_x.setOption({
                        series: [{
                            data: graph_route_x.nodes,
                        }],
                    });

                    network_y.setOption({
                        series: [{
                            data: graph_route_y.nodes,
                        }],
                    });
                });
        }, 2000);

    });
})
