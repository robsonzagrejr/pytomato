function addNode(visited_node, nodes, node, automaton){
    if (!(visited_node.includes(node))) {
        var color = {
            border: '#343a40',
            background: '#6c757d'
        };
        var shape = {borderDashes: false};
        var node_label = node; 
        if (node == automaton['inicial']) {
            color['border'] = '#121820';
            node_label = "->"+node_label;
            shape['borderDashes'] = true;
        }
        if (automaton['aceitacao'].includes(node)) {
            color['background'] = '#ed4656';
            node_label = "*"+node_label;
        }
        

        var val = {
            id: node,
            label: node_label,
            borderWidth: 1,
            shapeProperties:shape,
            color: color,
            font: {
                color: "#ffffff"
            }
        };
   
        nodes.push(val);
        visited_node.push(node);
    }
    return visited_node, nodes
}

function updateGraph(automatonData, automatonSelected){
    if (automatonSelected) {
        // create an array with nodes
        var automaton = automatonData[automatonSelected];

        var visited_node = [];
        var states_nodes = [];
        var states_edges = [];

        var transitions = automaton['transicoes'];
        for (var state in transitions) {
            var state_val = transitions[state];
            visited_node, states_nodes = addNode(visited_node, states_nodes, state, automaton);
            var t = {};
            for (var alph in state_val) {
                for (var i=0; i < state_val[alph].length; i++) {
                    s = state_val[alph][i];
                    visited_node, states_nodes = addNode(visited_node, states_nodes, s, automaton);
                    if (s in t) {
                        t[s].push(alph);
                    } else {
                        t[s] = [alph];
                    }
                }
            }
            for (var s in t) {
                alph = t[s].join(',');
                var val = {from: state, to: s, label:alph, arrows:"to"}
                states_edges.push(val);
            }
        }
        var nodes = new vis.DataSet(states_nodes);

        // create an array with edges
        var edges = new vis.DataSet(states_edges);

        // create a network
        var container = document.getElementById("automaton-graph");
        var data = {
          nodes: nodes,
          edges: edges,
        };
        var options = {};
        var network = new vis.Network(container, data, options);
    } else {
        var container = document.getElementById("automaton-graph");
        var data = {
          nodes: new vis.DataSet([]),
          edges: new vis.DataSet([]),
        };
        var options = {};
        var network = new vis.Network(container, data, options);
    }

     
    return '';
}
