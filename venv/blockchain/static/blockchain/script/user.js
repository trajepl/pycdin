$(document).ready(function() {
    $(".add-button").click(function() {
        $("#managers-addition").fadeIn(300);
        $("#managers-addition .dataTables_filter input[type='search']").focus();
    });

    $("table").on('click', '.is-root', function(){
        if(!confirm('Confirm modify?')) {
            return ;
        }

        var id = $(this).attr('user-id');
        var root = $(this).attr("is-root");
        if(root == 'false')
            root = 'true'
        else root = 'false'

        $.post(
            "/modifyauth",
            {
                root : root,
                id   : id,
            },
            function(data) {
                if(data.status==1) {
                    history.go(0);
                } else  alert("Modify failed! " + data.content);
            }
        );
    })

    $("table").on('click', '.delete-button', function() {
        if(!confirm('Confirm delete?')) {
            return;
        }
        
        var id = $(this).attr('user-id');

        $.ajax({
            url:"/userdelete",
            dataType:"json",
            data:{
                id:id,
            },
            success:function(data) {
                if(data.status == 1) {
                    history.go(0);
                } else {
                    alert("Delete failed！" + data.content);
                }
            }
        });   
    });

    $(".submit").click(function() {
        var id = $("#managers-add-td1 input[type='text']").val().trim();
        var password = $("#managers-add-td2 input[type='password']").val().trim();

        $.post(
            "/useradd",
            {
                id       : id,
                password : password,
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
