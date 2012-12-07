var labelType, useGradients, nativeTextSupport, animate;

(function() {
  var ua = navigator.userAgent,
      iStuff = ua.match(/iPhone/i) || ua.match(/iPad/i),
      typeOfCanvas = typeof HTMLCanvasElement,
      nativeCanvasSupport = (typeOfCanvas == 'object' || typeOfCanvas == 'function'),
      textSupport = nativeCanvasSupport 
        && (typeof document.createElement('canvas').getContext('2d').fillText == 'function');
  //I'm setting this based on the fact that ExCanvas provides text support for IE
  //and that as of today iPhone/iPad current text support is lame
  labelType = (!nativeCanvasSupport || (textSupport && !iStuff))? 'Native' : 'HTML';
  nativeTextSupport = labelType == 'Native';
  useGradients = nativeCanvasSupport;
  animate = !(iStuff || !nativeCanvasSupport);
})();

var Log = {
  elem: false,
  write: function(text){
    if (!this.elem) 
      this.elem = document.getElementById('log');
    this.elem.innerHTML = text;
    this.elem.style.left = (500 - this.elem.offsetWidth / 2) + 'px';
  }
};

function init(data){
    //init data
    var json = JSON.parse(data);
    //end
    //init Spacetree
    //Create a new ST instance
    var st = new $jit.ST({
        orientation: 'top',
        //id of viz container element
        injectInto: 'arbol',
        //set duration for the animation
        duration: 800,
        //set animation transition type
        transition: $jit.Trans.Quart.easeInOut,
        //set distance between node and its children
        levelDistance: 50,
        //enable panning
        Navigation: {
          enable:true,
          panning:true
        },
        //set node and edge styles
        //set overridable=true for styling individual
        //nodes or edges
        Node: {
            height: 60,
            width: 120,
            type: 'rectangle',
            color: '#aaa',
            overridable: true
        },
        
        Edge: {
            type: 'bezier',
            color: "#000",
            overridable: true
        },
        
        onBeforeCompute: function(node){
            Log.write("Cargando ...");
        },
        
        onAfterCompute: function(){
            Log.write("Listo");
        },
        
        //This method is called on DOM label creation.
        //Use this method to add event handlers and styles to
        //your node.
        onCreateLabel: function(label, node){
            var array = infoNodo(node.name),
                string = "";
            string += "<table>";
            for (var i = 0; i<array.length; ++i){
                string += "<tr>";
                string += "<td>";
                string += array[i];
                if (i == 2)
                  string += "%";
                string += "</td>";
                string += "</tr>";
                
            }
            string += "</table>";
            label.id = node.id;            
            //label.innerHTML = node.name
            label.innerHTML = string; 
            label.onclick = function(){
              st.onClick(node.id);
            };
            label.ondblclick = function(){
              var form = document.getElementById("visualizarActividad");
              var input = form.getElementsByTagName("input");
              for (var i = 0; i < input.length; ++i){
                if (input[i].id == "inputAct"){
                  input[i].value = label.id;
                  form.submit();
                }
              }
            }
            //set label styles
            var style = label.style;
            style.width = 120 + 'px';
            style.height = 60 + 'px';            
            style.cursor = 'pointer';
            style.textAlign= 'center';
            style.color = "#000"


        },
        
        //This method is called right before plotting
        //an edge. It's useful for changing an individual edge
        //style properties before plotting it.
        //Edge data proprties prefixed with a dollar sign will
        //override the Edge global style properties.
        onBeforePlotLine: function(adj){
            if (adj.nodeFrom.selected && adj.nodeTo.selected) {
                adj.data.$color = "#a0a0a0";
                adj.data.$lineWidth = 3;
            }
            else {
                delete adj.data.$color;
                delete adj.data.$lineWidth;
            }
        },

        offsetY: 150,
    });
    //load json data
    st.loadJSON(json);
    //compute node positions and layout
    st.compute();
    //optional: make a translation of the tree
    st.geom.translate(new $jit.Complex(-200, 0), "current");
    //emulate a click on the root node.
    st.onClick(st.root);
    //end
}

function infoNodo(id){
  var array = id.split(" ");
  if (array.length == 3){
    return array;
  }
  else{
    var newArray = new Array(),
        string = "",
        count = array.length,
        i = 0;
    while (count-i >= 3 && i<count){
      string += array[i];
      string += " ";
      i++;
    }
    newArray[0] = string;
    for (var j = 1; j<3; ++j){
      newArray[j] = array[i];
      i++;
    }
    return newArray;
  }
}
