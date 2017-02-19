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
      smooth: true,
      arrows: {
        to: {
          enabled: true
        }
      }
    },
    physics:{
      barnesHut:{gravitationalConstant:-30000},
      stabilization: {iterations:2500}
    },
    groups: {}
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
    var self = this;
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
      
      var maxModuleId = 0;
      for(var i = 0; i < parsed.nodes.length; i++){
        moduleId = parsed.nodes[i].attributes.Module_id;
        parsed.nodes[i].group = moduleId;
        parsed.nodes[i].size = 32;
        totalNumModule = parsed.nodes[i].attributes.Total_mod;
        if(maxModuleId < moduleId){
          self.options.groups[moduleId] = {
            shape: 'dot',
            color: self.getRandomColor(moduleId, totalNumModule)
          }
          maxModuleId = moduleId;
        }
        delete parsed.nodes[i].color 
      }

      for(var i = 0; i < parsed.edges.length; i++){
        weight = parsed.edges[i].attributes.Weight;
        parsed.edges[i].width = weight * 30;
      }

      console.log(parsed.edges);

      var   data = {
        nodes: parsed.nodes,
        edges: parsed.edges
      };
      var container = document.getElementById(containter_name);
      network = new vis.Network(container, data, self.options);
    });
  },
  getRandomColor: function(moduleId, totalNumModule){
    var hueIni = 0.1;
    var hueWid = 0.95;
    var hue = hueIni + (moduleId-1) * hueWid / (totalNumModule-1);
    var saturation = 1.0;
    var lightness = 0.5;
    return Color.hsl(hue, saturation, lightness).hexTriplet();
  }
}
