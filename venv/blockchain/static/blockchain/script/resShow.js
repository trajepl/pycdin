$(document).ready(function() {
	$(".modify-cancel-button").click(function(){
		$(this).addClass("none");
		$(this).next().addClass("none");
		$(this).prev("a").removeClass("none");

		var tdList = $(this).parent().prevAll("td");
		for(var i = 0;i < 4;i++) {
			var text = $(tdList[i]).children("input").val();
			 $(tdList[i]).empty().text(text);
		}
		return;
	});

    $(".modify-button").click(function() {
    	var i,tdList;
    	$(this).addClass("none");
    	tdList = $(this).parent().prevAll("td");
    	$(this).nextAll().removeClass('none');
    	for(i = 0;i < 4;i++) {
    		var text = $(tdList[i]).text();
    		$(tdList[i]).empty().append($("<input class='modify-input' value='"+text+"''>"));
    	}
    });

    $(".modify-submit-button").click(function() {
    	$(this).addClass("none");
    	$(this).prevAll(".modify-button").removeClass("none");
    	$(this).prev(".modify-cancel-button").addClass("none");
    	
    	var i, $this = $(this), data = new Object();
    	var item = $(this).attr('item');
    	var tdList = $(this).parent().prevAll("td");

    	for(i = 0;i < 4;i++) {
    		data[$(tdList[i]).attr('data-field')] = $(tdList[i]).children("input").val();
    	}
    	
    	$.ajax({
    	    url:"../Index/resItemModify",
    	    type:"POST",
    	    dataType:"json",
    	    data:{
    	    	item: item,
    			data:JSON.stringify(data)
    		},
    		success:function(data){
    			if(data.status == 1) {
    				alert("修改成功");
    				for(var i = 3;i < 7;i++) {
    					var val = $(tdList[i]).children('input').val();
    					$(tdList[i]).empty().text(val);
    				}
    				$this.addClass("none");
    			}
    			else {
    				alert("修改失败");
    			}
    	    },
    	});    
    });

	$('table').DataTable({
		bLengthChange:false,
        bInfo:false,
        iDisplayLength: 20,
		language: {
	        "sProcessing": "处理中...",
	        "sLengthMenu": "显示 _MENU_ 项结果",
	        "sZeroRecords": "没有匹配结果",
	        "sInfo": "显示第 _START_ 至 _END_ 项结果，共 _TOTAL_ 项",
	        "sInfoEmpty": "显示第 0 至 0 项结果，共 0 项",
	        "sInfoFiltered": "(由 _MAX_ 项结果过滤)",
	        "sInfoPostFix": "",
	        "sSearch": "搜索:",
	        "sUrl": "",
	        "sEmptyTable": "表中数据为空",
	        "sLoadingRecords": "载入中...",
	        "sInfoThousands": ",",
	        "oPaginate": {
	            "sFirst": "首页",
	            "sPrevious": "上页",
	            "sNext": "下页",
	            "sLast": "末页"
	        },
	        "oAria": {
	            "sSortAscending": ": 以升序排列此列",
	            "sSortDescending": ": 以降序排列此列"
	        }
	    }
	});
});