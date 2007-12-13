// Browser-independent event handler attaching
function addEvent(element, event, handler)
{
	if (element.addEventListener) element.addEventListener(event, handler, false);
	else if (element.attachEvent) element.attachEvent('on' + event, handler);
	else throw "addEvent: Unable to attach the event handler";
}

function createTagsWidget(container, tag, values, width)
{
	// TODO: add support for readonly tags
	var table = document.createElement("TABLE");
	var body = document.createElement("TBODY");
	var row = document.createElement("TR");
	var cell = document.createElement("TD");

	var blank = document.createTextNode("");
	
	var img_add = document.createElement("IMG");
	img_add.src = "/site_media/images/add.gif"
	img_add.alt = "[+]";
	var cell_img_add = document.createElement("TD");
	cell_img_add.appendChild(img_add);
	
	var img_remove = document.createElement("IMG");
	img_remove.src = "/site_media/images/subtract.gif"
	img_remove.alt = "[-]";
	var cell_img_remove = document.createElement("TD");
	cell_img_remove.appendChild(img_remove);
	
	//document.body.appendChild(table);
	container.appendChild(table);

	// TODO: when adding or removing tags from the end of the list,
	// there is no need to redraw the whole table - just the last row would be enough
	function drawTable()
	{
		// Cleaning up
		if (table.hasChildNodes())
		{
			children = table.childNodes;
			for (i = 0; i < children.length; i++) if (children[i].nodeName == "TBODY") table.removeChild(children[i]);
		}
		
		// Building the table
		height = Math.ceil((values.length + 1) / width);
		new_body = body.cloneNode(false)
		table.appendChild(new_body);
		for (i = 0, n = 0; i < height; i++)
		{
			new_row = row.cloneNode(false);
			new_body.appendChild(new_row);
			for(j = 0; j < width; j++, n++)
			{
				if (n < values.length)
				{
					new_node = tag.cloneNode(false);
					new_node.value = values[n];
					new_node.onblur = new_node.onchange = changeTag;
					new_node.n = n;
					new_cell_img = cell_img_remove.cloneNode(true);
					new_cell_img.onclick = removeTag;
					new_cell_img.n = n;
				}
				else
				{
					new_node = blank.cloneNode(false);
					if (n == values.length)
					{
						new_cell_img = cell_img_add.cloneNode(true)
						new_cell_img.onclick = addTag;
					}
					else
					{
						new_cell_img = cell.cloneNode(false);
						new_cell_img.appendChild(blank.cloneNode(false));
					}
				}
				new_row.appendChild(new_cell_img);
				new_cell = cell.cloneNode(false);
				new_row.appendChild(new_cell);
				new_cell.appendChild(new_node);
			}
		}
	}
	
	// Event handlers
	function addTag(e)
	{
		//alert("Event: " + e.type + "\nAdding a new tag");
		values.push("");
		drawTable();
	}
	
	function removeTag(e)
	{
		//alert("Removing tag " + this.n);
		// Keep the only tag
		if (values.length > 1)
		{
			values.splice(this.n, 1);
			drawTable();
		}
	}
	
	function changeTag(e)
	{
		//alert("Changing tag " + this.n);
		values[this.n] = this.value;
	}
	
	drawTable();
}
