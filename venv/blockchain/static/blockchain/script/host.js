$(document).ready(function() {
    $(".add-button").click(function() {
        $("#managers-addition").fadeIn(300);
        $("#managers-addition .dataTables_filter input[type='search']").focus();
    });

	$("table").on('click','.modify-cancel-button',function() {
		$(this).addClass("none");
		$(this).next().addClass("none");
		$(this).prev().removeClass("none");
		var len, tdList = $(this).parent().prevAll("td");
        history.go(0);
		return;
	});

	$("table").on('click','.modify-check-button',function() {
		$(this).addClass("none");
		$(this).prevAll(".modify-button").removeClass("none");
		$(this).prev(".modify-cancel-button").addClass("none");
		
		var len, $this = $(this)
			,origin_host = $this.attr('host-id')
			,tdList = $(this).parent().prevAll("td")
			,data = new Object();

		for(var i = 0,len = tdList.length;i < len;i++) {
			data[i] = $(tdList[i]).children("input").val();
		}
		
        console.log(data);
		$.ajax({
		    url:"hostmodify",
		    type:"POST",
		    dataType:"json",
		    data:{
                origin_host  : origin_host,
                modify_host  : data[0],
                
			},
			success:function(data){
				if(data.status == 1) {
					alert("Modify success.");
					for(var i = 0;i < len;i++) {
						var val = $(tdList[i]).children('input').val();
						$(tdList[i]).empty().text(val);
					}
					$this.addClass("none");
				}
				else {
					alert("Modify failed." + data.content);
                    history.go(0);
				}
		    },
		});    
	});

    $("table").on('click', '.modify-button', function(){
        var origin_host = $(this).attr('host-id');
        $(this).addClass("none");
    	var len, tdList = $(this).parent().prevAll("td");
        $(this).nextAll().removeClass('none');

    	for(var i = 0,len = tdList.length;i < len;i++) {
    		var text = $(tdList[i]).text();
    		$(tdList[i]).empty().append($("<input class='modify-input' value='"+text+"''>"));
        }
        /*
        $.post(
            "/hostmodify",
            {
                host : host,
            },
            function(data) {
                if(data.status==1) {
                    history.go(0);
                } else  alert("Modify failed! " + data.content);
            }
        );*/
    });

    $("table").on('click', '.delete-button', function() {
        if(!confirm('Confirm delete?')) {
            return;
        }
        
        var host = $(this).attr('host-id');

        $.post(
            "/hostdelete",
            {
                host:host,
            },
            function(data) {
                if(data.status == 1) {
                    history.go(0);
                } else {
                    alert("Delete failed！" + data.content);
                }
            }
        );   
    });

    $(".submit").click(function() {
        var host = $("#managers-add-td1 input[type='text']").val().trim();

        $.post(
            "/hostadd",
            {
                host       : host,
            },
            function(data) {
                if(data.status==1) {
                    alert("Insert success!");
                    history.go(0);
                } else {
                    alert("Insert failed! " + data.content);
                }
            }
        );

    });

    $(".reset").click(function() {
        $("#managers-addition").css('display', 'none');
    });

    $('#userList').DataTable({
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

    $(".dataTables_filter input[type='search']").on('input propertychange', function() {
        if($(this).val().trim() != "") {
            $("#userList").removeClass("none");
        } else {
            $("#userList").addClass("none");
        }
    });

})
