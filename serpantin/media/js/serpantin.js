function loadListForm(app, model, page) {
	var server_url;
	//FIXME: add unique id for search panel in different tabs
	var sbar = dojo.byId(model + "_sbar");
	var q = "";
	if (sbar) q = sbar.value;
	var extraparam = new Array()
	if (page) extraparam.push("page=" + page);
	if (q) extraparam.push("q=" + q);
	server_url = "/async/" + app + "/" + model + "/";
	if (extraparam.length) server_url += "?" + extraparam.join("&");
	
	dojo.xhrGet({
		url:    server_url,
		handleAs: "text",
		timeout: 5000,
		load: function(response, ioArgs){
			var node = dojo.byId(model.toLowerCase() + 'listtab');
			
			node.innerHTML = response;
			dojo.connect(dojo.byId(model+"_sbut"), "onclick", function(e) { e.preventDefault(); loadListForm(app, model, page); });

			var tabpane = dijit.byId(model.toLowerCase() + 'TabPane');
			var tab = dijit.byId(model.toLowerCase() + 'listtabw');
			
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
