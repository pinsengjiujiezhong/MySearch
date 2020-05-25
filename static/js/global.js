
$(document).ready(function(){
	
// 去除虚线框（会影响效率）
$("a,input:checkbox,input:radio,button,input:button").live('focus',function(){$(this).blur();});

});


function hideElement(currentElement, targetElement) {
	if (!$.isArray(targetElement)) {
		targetElement = [ targetElement ];
	}
	$(document).on("click.hideElement", function(e) {
		var len = 0, $target = $(e.target);
		for (var i = 0, length = targetElement.length; i < length; i++) {
			$.each(targetElement[i], function(j, n) {
				if ($target.is($(n)) || $.contains($(n)[0], $target[0])) {
					len++;
				}
			});
		}
		if ($.contains(currentElement[0], $target[0])) {
			len = 1;
		}
		if (len == 0) {
			currentElement.hide();
		}
	});
};

function getStorage() {
	var my_search = localStorage.getItem('my_search') || []
	return my_search
};

function setStorage(value) {
	var my_search = getStorage()
	if (my_search.indexOf(value) != -1){
		my_search.splice(value, 1)
		my_search.unshift(value)
	} else{
		my_search.unshift(value)
	}
};

