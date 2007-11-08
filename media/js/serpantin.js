
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

	//alert("xhrGet");

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

			//alert("node:" + node);
			var tabpane = dijit.byId(model.toLowerCase() + 'TabPane');
			var tab = dijit.byId(node+"w");

			//alert("tabpane:" + tabpane + "\ntab:" + tab);
			tabpane.selectChild(tab);
			mainTabPane.selectChild(tabpane);

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

function loadForm(app_name, model_name, object_id, tab_title) {
	var server_url = '/async/' + app_name + '/' + model_name + '/';
	if (object_id) server_url += object_id + '/'; else server_url += 'new/';
	tab_id = dijit.getUniqueId("tab");
	win_id = tab_id.substring(4, tab_id.length);
	server_url += win_id + '/';
	if (arguments.length < 4) tab_title = 'New ' + model_name;
	var newTab = new dijit.layout.ContentPane({
		id: tab_id,
		title: tab_title,
		closable:true,
		parseOnLoad:true,
		refreshOnShow: false,
		href: server_url
	}, dojo.doc.createElement('div'));
	var parentTabPane = dijit.byId(model_name.toLowerCase() + 'TabPane');
	parentTabPane.addChild(newTab);
	newTab.startup();
	parentTabPane.selectChild(newTab);
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

function submitForm(app_name, model_name, object_id, win_id, action)
{
	var server_url = '/async/' + app_name + '/' + model_name + '/';
	if (object_id) server_url += object_id + '/'; else server_url += 'new/';
	server_url += win_id + '/'
	var node = dojo.byId("fpform_" + win_id);
	dojo.xhrPost({
		url: server_url,
		form: node,
		handleAs: "json-comment-filtered",
		timeout: 5000,
		load: function(response, ioArgs)
		{
			console.dir(response);
			switch (action) {
				case 'save_and_close':
					var tabpane = dijit.byId(model_name.toLowerCase() + "TabPane");
					//var listtab = dijit.byId(model_name.toLowerCase() + "listtabw");
					var tab = dijit.byId("tab_" + win_id);
					//tabpane.selectChild(listtab);
					loadListForm(app_name, model_name, model_name.toLowerCase() + 'listtab');
					tabpane.removeChild(tab);
					//FIXME: delete tab somehow from the memory
					//delete tab;
					break;
			}
			return response;
		},
		error: function(response, ioArgs)
		{
			node.innerHTML = response;
			return response;
		}
	});
}

function _submitForm(elem, app, model, win_id, id, cont) {
	defineURL = function(app, model, win_id, id, cont) {
		if (cont) {
			oper = "saveandgo";
		} 
		else {
			oper = "save";
		}
		if (id) {
			//alert("submit existent obj");
			//server_url = "/async/"+app+"/"+model+"/"+oper+"/"+id+"/form/"+win_id+"/";
			server_url = "/async/"+app+"/"+model+"/"+id+"/";
		}
		else {
			server_url = "/async/"+app+"/"+model+"/new/";
		}
		return server_url;
	}


	server_url = defineURL(app, model, win_id, id, cont);
	//alert("server_url "+ server_url);
	
	var node = document.getElementById("fpform_"+win_id);
	//node.method = "post";
	//node.enctype = "multipart/form-data";
	dojo.xhrPost({
		url: server_url,
		form: node,
		handleAs: "text",
		timeout: 5000,
		load: function(response, ioArgs)
		{
			return response;
		},
		error: function(response, ioArgs)
		{
			node.innerHTML = response;
			return response;
		}
		/*
		load:   function(type, data){
			var w = dojo.widget.byId("fp_"+win_id);
			
			refresh = function(){
				alert("Continue function...");			
			}
				
//			} else {	
			    resp = eval("("+data+")");
				if (resp.oper=="UPDATE") {
					if (cont) {
						//refresh();
						var cw = dojo.widget.byId("fpcontent_" + win_id);
						cw.cacheContent = false;
						cw.refresh();
					} else {
						if (Context.listform[app+"_"+model]) {
							//alert("Updated 1. app: "+app+" model: "+model);
							var node = Context.listform[app+"_"+model].node;
							var page = Context.listform[app+"_"+model].page;
							w.closeWindow();
							loadListForm(app,model,node,page);
						} else {
							//alert("Updated 2. app: "+app+" model: "+model);
							w.closeWindow();
							//loadListForm(app,model,node,page);
							relObj = dojo.widget.byId(""+model+"_rellist");
							if (relObj) {
								relObj.refresh();
							}
						}
					}
			    } else if (resp.oper=="ADDED"){
					var id = resp.id;
					var repr = resp.repr;
					if (cont) {
						//alert("Continue...");
						//refresh();
						server_url = defineURL(app, model, win_id, id, cont);
						//alert("server_url 2 "+ server_url);
						var cw = dojo.widget.byId("fpcontent_" + win_id);
						cw.cacheContent = false;
						cw.setUrl(server_url);
				  		//cw.loadContents();	  
						cw.refresh();
					} else {
						alert(""+resp.oper);
						//TODO: Update listform when regular object is added (parentid is not set)  
						if (Context.properties[win_id]) {
							var parentid = Context.properties[win_id].parentid
							var selectid = Context.properties[win_id].selectid
							//alert("Parentid "+parentid+" selectid "+selectid);
							//FIXME: find proper fp_id
							var listnode = findFloatingPaneChildNode(parentid, selectid);
							if (listnode) {
								updateList(listnode, id, repr);
							}
						} else {
							//TODO: Remove duplicate code
							//alert(data);
							var node = Context.listform[app+"_"+model].node;
							var page = Context.listform[app+"_"+model].page;
							loadListForm(app,model,node,page);
						}
						w.closeWindow();
						relObj = dojo.widget.byId(""+model+"_rellist");
						if (relObj) {
							relObj.refresh();
						}
					}
				} else {
		  			w.containerNode.innerHTML = data;	  
				}
//			}	 
		},
      	error: function(type, error, data) {alert(String(type) + "\n" + String(error.message) + "\n" + String(data) ); dojo.debug("Debig: " + data);},
	*/
    });  
}

