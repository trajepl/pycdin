$(document).ready(function() {
	$("table").on('click','.modify-cancel-button',function() {
		$(this).addClass("none");
		$(this).next().addClass("none");
		$(this).prev("a").removeClass("none");
		var len, tdList = $(this).parent().prevAll("td");
		for(var i = 0,len = tdList.length - 1;i < len;i++) {
			var text = $(tdList[i]).children("input").val();
			 $(tdList[i]).empty().text(text);
		}
		return;
	});

	$("table").on('click','.modify-button',function() {
	    $(this).addClass("none");
    	var len, tdList = $(this).parent().prevAll("td");
    	$(this).nextAll().removeClass('none');

    	for(var i = 0,len = tdList.length - 1;i < len;i++) {
    		var text = $(tdList[i]).text();
    		//每个td 清空 加上一个input 将原本的text填写进input中
    		$(tdList[i]).empty().append($("<input class='modify-input' value='"+text+"''>"));
    	}
	});


	$("table").on('click','.delete-button',function() {
		if(!confirm('确认删除？')) {
			return;
		}
	    var $this = $(this),id = $this.attr('data-id');

	    $.ajax({
	        url:"../Index/teacherDelete",
	        dataType:"json",
	        data:{
	        	id: id
	    	},
	    	success:function(data){
	    		if(data.status == 1) {
	    			alert("删除成功");
	    			$this.parents('tr').remove();
	    		}
	    		else {
	    			alert("删除失败");
	    		}
	        },
	    });    
	});

	$("table").on('click','.modify-submit-button',function() {
		$(this).addClass("none");
		$(this).prevAll(".modify-button").removeClass("none");
		$(this).prev(".modify-cancel-button").addClass("none");
		
		var len, $this = $(this)
			,id = $this.attr('data-id')
			,tdList = $(this).parent().prevAll("td")
			,data = new Object();

		for(var i = 0,len = tdList.length - 1;i < len;i++) {
			data[$(tdList[i]).attr('data-field')] = $(tdList[i]).children("input").val();
		}
		
		$.ajax({
		    url:"../Index/teacherModify",
		    type:"POST",
		    dataType:"json",
		    data:{
		    	id: id,
				data:JSON.stringify(data)
			},
			success:function(data){
				if(data.status == 1) {
					alert("修改成功");
					for(var i = 0;i < len;i++) {
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