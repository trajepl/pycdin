$(document).ready(function(){
	$(".content-body").on("mouseover",".portal-item:not('.inactive')",function(e) {

		var color = $(this).find(".icon-wrapper").css("background-color");
		$(this).css("border-color",color);
		$(this).find("h4,p").css("color",color);
	});

	$(".content-body").on("mouseout",".portal-item",function(e) {
		$(this).css("border-color","transparent");
		$(this).find("h4").css("color","#333");
		$(this).find("p").css("color","#777");
	});

	$("#add-file").click(function() {
		$("#add-file-input").trigger('click');
	});

	$("#add-file-input").on("change",function() {

		$("#add-file-input").next().trigger('click');
	});

	$("#test-result").click(function() {
		
	});
});
