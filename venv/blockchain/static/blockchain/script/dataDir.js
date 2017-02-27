$(document).ready(function() {
	$("table").on('click', '.in-use', function() {
		var state_pass = $(this).attr('state');
		var id = $(this).attr('data-id');
		var tableName = $(this).attr('table-name');

		var state_now = state_pass==0?1:0;

		$.ajax({
			url:"../../../Index/changeState",
			dataType:"json",
			data:{
				id:id,
				state:state_now,
				tableName:tableName
			},
			success:function(data){
	    		if(data.status == 1) {
	    			history.go(0);
	    		}
	    		else {
	    			alert("error!");
	    		}
	        },

		});

	});

	$(".submit").click(function() {
		
		var tableName = $("#add-item").attr('table-name');
		var dataField = $("#add-item").attr('data-field');
		var item = $("textarea").val().trim();

        $.post(
            "../../../Index/dataItemAdd",
            {
                tableName:tableName,
                dataField:dataField,
                item:item
            },
            function(data) {
                if(data.status==1) {
                    alert("Insert success!");
                    history.go(0);
                } else {
                    alert("Insert failed!");
                }
            }
        );

    });

    $(".reset").click(function() {
        $("#managers-addition").addClass('none');
    });


	$("table").on('click', '#add-item', function() {
		$("#managers-addition").removeClass('none');
	});

	$("table").on('click','.modify-cancel-button', function() {
		$(this).addClass("none");
		$(this).next().addClass("none");
		$(this).prev("a").removeClass("none");
		var len, tdList = $(this).parent().prevAll("td")[1];
		
		var text = $(tdList).children("input").val();
		$(tdList).empty().text(text);
	
		return;
	});

	$("table").on('click','.modify-button',function() {
	    $(this).addClass("none");
    	var len, tdList = $(this).parent().prevAll("td")[1];
    	$(this).nextAll().removeClass('none');

		var text = $(tdList).text();
		//每个td 清空 加上一个input 将原本的text填写进input中
		$(tdList).empty().append("<input class='modify-input' value='"+text+"''>");
	});


	$("table").on('click','.modify-submit-button',function() {
		$(this).addClass("none");
		$(this).prevAll(".modify-button").removeClass("none");
		$(this).prev(".modify-cancel-button").addClass("none");
		
		var len, $this = $(this)
			,id = $this.attr('data-id')
			,tableName=$this.attr('table-name')
			,tdList = $(this).parent().prevAll("td")[1]
			,data = new Object();

		
		data[$(tdList).attr('data-field')] = $(tdList).children("input").val().trim();
		data['id']=id;
		
		$.ajax({
		    url:"../../../Index/dataItemModify",
		    type:"POST",
		    dataType:"json",
		    data:{
		    	tableName:tableName,
				data:JSON.stringify(data)
			},
			success:function(data){
				if(data.status == 1) {
					var val = $(tdList).children('input').val();
					$(tdList).empty().text(val);
					$this.addClass("none");
				}
				else {
					alert("未作出修改");
					var val = $(tdList).children('input').val();
					$(tdList).empty().text(val);
					$this.addClass("none");
				}
		    },
		});    
	});

	$('table.info').DataTable({
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