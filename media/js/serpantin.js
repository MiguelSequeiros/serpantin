
    var town_type = [];
    town_type[1] = "г.  ";
    town_type[2] = "д.  ";
    town_type[3] = "пос.";
    town_type[4] = "с.  ";
    var town_type_ptr = 1;
	var changeTownType = function() {
		next = town_type_ptr + 1;
		//alert("length "+town_type.length);
		if (next == town_type.length) {
			idx = 1;
		} else {
			idx = town_type_ptr + 1;
		}
		town_type_ptr = idx;
		//alert("ptr " + town_type_ptr);
		obj = document.getElementById('town_type_lbl');
		obj.innerHTML = town_type[idx];	
		inp	= document.getElementById('town_type');
		inp.value = idx;
		//alert("value"+inp.value);
    }



var Context = {
    listform: [],
    org: "",
    person: "",
    win_id: 0,
    properties: []
};


function updateHistory(value) {
    //var value = dojo.byId("obj_id");
    //alert("Stub for updateHistory");

    dojo.io.bind({
        url:    "/common/update_history/"+value+"/",
        //content:{format: 'ahah'},
        load:   function(type, data){
                    var node = dojo.byId("todayhotlinks");
                    node.innerHTML = data;
        }
    })    
  }


function loadListForm(app, model, node, page) {
    Context.listform[app+"_"+model] = {"node":node, "page":page};
    var server_url;
    //FIXME: add unique id for search panel in different tabs
    var q = document.getElementById(model+"_sbar");
    var extraparam = "";
    if (page) {
		extraparam = "?page=" + page;
    }
    if ( q ) {  
		if (extraparam) {
	    	extraparam = extraparam + "&q=" + q.value;
		}
		else {
	    	extraparam = "?q=" + q.value;
		}
    }
    server_url = "/async/"+node+"/"+app+"/"+model+"/list/" + extraparam;
    
    dojo.xhrGet({
        url:    server_url,
        //content:{format: 'ahah'},
        handleAs: "text",
        timeout: 5000,
        load: function(response, ioArgs){
            //alert("node "+node);
            var n = dojo.byId(node);

            n.innerHTML = response;
            dojo.connect(dojo.byId(model+"_sbut"), "onclick", function(e) { e.preventDefault(); loadListForm(app, model, node, page); });

            var tab = dijit.byId(node+"w");
            var tabpane = dijit.byId("mainTabPane");

            //tabpane.selectChild(tab);
            mainTabPane.selectChild(peopletab);

            return response;
        },
	error: function(response, ioArgs) { // ?
    	    console.error("HTTP status code: ", ioArgs.xhr.status); // ?
	    return response; // ?
	}
    });
}


function loadContentForm(content_id, object_id) {
	var contentInfo = {};
	dojo.io.bind({
	url:   		"/async/call/getContentTypeOf/"+content_id+"/",
	mimetype:	"text/plain",
	load:   	function(type, data){
				resp = eval("("+data+")");
				loadForm(resp.app_label, resp.model, object_id);

			}
	});
}


var tabCounter = 1;

function loadForm(app, model, id, properties, values) {
	server_url = '/async/'+app+'/'+model+'/'+id+'/form/1/';
	var newTab = new dijit.layout.ContentPane({
		title: 'Tab ' +(++tabCounter),
		closable:true,
		refreshOnShow: false,
		href: server_url
	}, dojo.doc.createElement('div'));
	dijit.byId('peopleTabPane').addChild(newTab);
	newTab.startup();
}

/*
function loadForm(app,model,id,properties, values) {
    Context.win_id = Context.win_id + 1;
    var getparams = "";
    var win_id = Context.win_id;
    if (properties) {
        Context.properties[win_id] = properties;
		//alert(properties.model);
		//alert(properties.oid);
		if (properties.type=='boundform') {
	    	    getparams = "?type=boundform&app="+properties.app+"&model="+properties.model+"&oid="+properties.oid+"";
		}
    }
    var server_url;    
    if (id) {
    	//alert("id="+id);
      	server_url = "/async/"+app+"/"+model+"/"+id+"/form/"+win_id+"/";
    }
    else {
      	//alert("no id="+id);
      	server_url = "/async/"+app+"/"+model+"/form/"+win_id+"/" + getparams;
    }
    var props = {id:"fp_"+win_id, 
			//constrainToContainer:"true",
			//tagName:"MyPane", 
			//title:"Hello everybody", 
			displayCloseAction:"true",
			hasShadow:"true",
			//style:"height:380px;width:408px; padding:20 20 20 20;", 			
			style:"padding:40 40 40 40;" 			
    };
    var parentNode = document.createElement("div");
    var tmpWidget = dojo.widget.createWidget("FloatingPane", props);
    var cntProp =  { layoutAlign:"top",
		    id:"fpcontent_"+win_id, 
			style:"border: solid white; height:380px; width:408px; padding:20 20 20 20;", 
			href: server_url,
			executeScripts:"true",
			preload:"true",
	};
    dojo.html.body().appendChild(tmpWidget.domNode);		   
    tmpWidget.hide();
    tmpWidget.domNode.style.position = "absolite";
    // relative does not work
    //tmpWidget.domNode.style.position = "relative";
    tmpWidget.domNode.style.left = "100px";
    tmpWidget.domNode.style.top = "20px";
    if (Geometry[model]) {
	//alert("Geometry setting exist...");
        tmpWidget.domNode.style.height = Geometry[model].height;
	tmpWidget.domNode.style.width = Geometry[model].width;
    } else {
	//alert("Geometry setting does not exist...");
	tmpWidget.domNode.style.height = "500px";
	tmpWidget.domNode.style.width = "500px";
    }
    tmpWidget.domNode.style.padding = "60 60 60 60";
    tmpWidget.titleBarText.innerHTML = "Object of type "+model+"  win_id "+win_id;
    var content = dojo.widget.createWidget("ContentPane", cntProp);
    tmpWidget.addChild(content);
    tmpWidget.show();
    //fillComboBoxes();		   
}
*/

findNodeById = function(inRoot, inId) {
    var i=0;
    var children = inRoot.childNodes;
    var node;
    while (node = children[i++]) {
      	if (node.id == inId)
        	return node;
      	var subnode = findNodeById(node, inId);
      	if (subnode) 
        	return subnode;
    }
    return null;
}


findFloatingPaneChildNode = function(fpid, nodeid) {
    var fpnode = document.getElementById(fpid);
    if (fpnode) {
      	var childnode = findNodeById(fpnode, nodeid);
      	if (childnode) {
        	return childnode;
      	}
    }
    return null;
}


getParentByClass = function(fromNode, className) {
	//NOTE: code is grabbed from dojo/src/html.js dojo.html.getParentByType
	//var className = "parentdiv";
	//var parent = dojo.byId(node);
	var parent = fromNode;
	className = className.toLowerCase();
	while((parent)&&(parent.className.toLowerCase()!=className)){
		if(parent==(document["body"]||document["documentElement"])){
			return null;
		}
		parent = parent.parentNode;
	}
	//alert("Parent ID: "+parent.id+" Class name: "+parent.className);
	return parent;
}



function updateList(elem, newId, newRepr) {
    //var elem = document.getElementById(objid);
    if (elem) {
        if (elem.nodeName == 'SELECT') {
            var o = new Option(newRepr, newId);
            elem.options[elem.options.length] = o;
            elem.selectedIndex = elem.length - 1;
		}    
    } 
}




