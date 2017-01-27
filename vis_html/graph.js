var Graph = function(fileName, containerId){
  this.fileName = fileName;
  this.containerId = containerId;
  this.LENGTH_MAIN = 350,
    LENGTH_SERVER = 150,
    LENGTH_SUB = 50,
    WIDTH_SCALE = 2,
    GREEN = 'green',
    RED = '#C5000B',
    ORANGE = 'orange',
    GRAY = 'gray',
    BLACK = '#2B1B17';

  this.options = {
    nodes: {
      scaling: {
        min: 160,
        max: 320
      }
    },
    edges: {
      color: GRAY,
      smooth: true
    },
    physics:{
      barnesHut:{gravitationalConstant:-30000},
      stabilization: {iterations:2500}
    },
    groups: {
      1: {
        shape: 'triangle',
        color: "#FF9900" // orange
      },
      2: {
        shape: 'dot',
        color: "#2B7CE9" // blue
      },
      3: {
        shape: 'square',
        color: "#5A1E5C" // purple
      },
      4: {
        shape: 'square',
        color: "#C5000B" // red
      },
      5: {
        shape: 'square',
        color: "#109618" // green
      }
    }
  }
}

Graph.prototype = {
  show: function(){
    this.readJson(this.fileName, this.containerId);
  },
  readTextFile: function(file, callback){
    var rawFile = new XMLHttpRequest();
    rawFile.overrideMimeType("application/json");
    rawFile.open("GET", file, true);
    var isFinished = false;
    rawFile.onreadystatechange = function() {
      if(isFinished){
        return;
      }

      if(rawFile.readyState == 4){
        callback(rawFile.responseText);
        isFinished = true;
      }
    }
    rawFile.send(null);
  },
  readJson: function(filename, containter_name){
    var options = this.options;
    this.readTextFile(filename, function(text){
      var gephijson = JSON.parse(text);
      var parseroptions = {
        edges: {
          inheritcolors: true
        },
        nodes: {
          fixed: false,
          parsecolor: false 
        }
      }
      var parsed = vis.network.convertGephi(gephijson, parseroptions);
      
      for(var i = 0; i < parsed.nodes.length; i++){
        parsed.nodes[i].group = parsed.nodes[i].attributes.Module_id;
        parsed.nodes[i].size = 32;
        delete parsed.nodes[i].color 
        console.log(parsed.nodes[i]);
      }

      var   data = {
        nodes: parsed.nodes,
        edges: parsed.edges
      };
      var container = document.getElementById(containter_name);
      network = new vis.Network(container, data, options);
    });
  },
  getRandomColor: function(){
    var hue = Math.random();
    var saturation = 1.0;
    var lightness = 0.5;
    return Color.hsl(hue, saturation, lightness).hexTriplet();
  }
}
