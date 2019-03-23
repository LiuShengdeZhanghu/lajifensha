function ko(){
    var anli_title = document.getElementById("Title").value;
    var anli_address = document.getElementById("Address").value;
    var anli_datetime = document.getElementById("DateTime").value;
    var divtable = document.getElementById("tablediv");
    divtable.style.display="block";
    $("#tbody").html("");
    $.ajax({
    url: "/dataku/serch/",
    type: "GET",
    async: true,
    data: { title: anli_title,address:anli_address,datetime:anli_datetime },
    success: function (org) {
        var trStr ="";
        for(var i =0;i<org.length;i++){
            trStr += '<tr>';//拼接处规范的表格形式
            trStr += '<th><a onclick="ft(this)">' + org[i].id+ '</a></th>';//数据表的主键值
            trStr += '<td>' + org[i].city + '</td>';//对应数组表的字段值
            trStr += '<td>' + org[i].time + '</td>';
            trStr += '<td>' + org[i].title+ '</td>';
            trStr += '<td>' + org[i].result + '</td>';
            trStr += '<td>' + org[i].point+ '</td>';
            trStr += "</tr>";
        }
        $("#tbody").html(trStr);
        },
    error: function () {
        alert("失败");
    }
    });
}
function ft(e) {
    var id = e.innerText;
    $('#myModal').modal('toggle');
    $.ajax({
    url: "/dataku/detail/",
    type: "GET",
    async: true,
    data: { "id":id },
    success: function (org) {
        var str='<p>'+org.content+'</p>';
        $("#modal-body").html(str);
        },
    error: function () {
        alert("失败");
    }
    });

}
function fb() {
    var divtable = document.getElementById("tablediv");
    divtable.style.display="none";
}