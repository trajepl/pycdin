$(document).ready(function () {
	$(".add-dir").click(function() {
		/* 从属表项设置不显示 */
		$("#choose").css('display','none');
        $("#department").addClass('none');
        $("#major").addClass('none');

		/* 显示从属表项的数组字典表 */
		var belongTo = ["department", "major"];

		/* 获取点击点参数 即当前数据表名 */
		var key = $(this).attr('dir-table');

		$("#managers-addition").fadeIn(300);
		
		/* 显示当前表项 从属项视表而定 */
		$("#add-td1").text(key);
		if($.inArray(key, belongTo) != -1) {
			$("#choose").fadeIn(300);

            if(key == "department") $("#department").removeClass('none');
            else $("#major").removeClass('none');

            $("#managers-addition .dataTables_filter input[type='search']").focus();
		} else {
            $("#add-td2 input[type='text']").focus();
        }         
	});


	$(".submit").click(function() {
        var belong_id='';
        var key = $("#add-td1").text().trim();
        belong_id = $('#'+key).val();

        var label_dir = $("#add-td2 input[type='text']").val();

        if(label_dir.trim().length === 0) {
            alert("Please inpout label fristly!");
            return ;
        }

        $.post(
            "../Index/addDirItem",
            {
                key:key,
                id:belong_id,
                label_dir:label_dir
            },
            function(data) {
                if(data.status == 1) {
                    alert("Insert success!");
                    history.go(0);
                }
                else {
                    alert("Insert failed!");
                }
            }
        );


            
    });
	/* 隐藏添加表项 */
	$(".reset").click(function() {
		$("#managers-addition").css('display','none');
	});


    $(".dataTables_filter input[type='search']").on('input propertychange',function() {
    	if($(this).val().trim() != "") {
    		$("#userList").removeClass("none");
    	}
    	else {
    		$("#userList").addClass("none");
    	}
    });

    $('#belongList').DataTable({
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
            "sSearch": "",
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