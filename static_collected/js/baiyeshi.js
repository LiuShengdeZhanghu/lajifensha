function baiyan() {
    $('#myBaiModal').modal('toggle');
    $("#Baimodal-body").html("sasa");
}

function anli() {
    $('#myKeyModal').modal('toggle');
    var txt = document.getElementById("anli-txt").value;
    // 去除上次可能剩余的节点
    var childNum = document.getElementById('table-body2').children.length;
    if(childNum>5){
        var parent = document.getElementById('table-body2');
        parent.removeChild(parent.lastChild);
    }
    $.ajax({
    url: "/baiyeshi/anli_Analysis/",
    type: "POST",
    async: true,
    data: { "txt":txt },
    success: function (org) {
        str="<tr>";
        var key_list=[];
        var value_list=[];
        for(var i=0;i<org.keywords.length;i++){
            for(var key in org.keywords[i]){
               str+='<td>'+key+'</td>';
                key_list.push(key)
            }
        }
        str+='</tr><tr>';
        for(var i=0;i<org.keywords.length;i++){
            for(var key in org.keywords[i]){
               str+='<td>'+org.keywords[i][key].toString().substring(0,5)+'</td>';
                value_list.push(org.keywords[i][key].toFixed(4));
            }
        }
        // 相似度计算表格
        str+='</tr>';
        $("#table-body").html(str);
        var myChart1 = echarts.init(document.getElementById('tf-idfdiv'));
        var option1={
            title : {
                text: '关键词南丁格尔图',
                subtext: 'tf-idf',
                x:'center'
            },
            tooltip : {
                trigger: 'item',
                formatter: "{a} <br/>{b} : {c} ({d}%)"
            },
            legend: {
                x : 'center',
                y : 'bottom',
                data:key_list
            },
            toolbox: {
                show : true,
                feature : {
                    mark : {show: true},
                    dataView : {show: true, readOnly: false},
                    magicType : {
                        show: true,
                        type: ['pie', 'funnel']
                    },
                    restore : {show: true},
                    saveAsImage : {show: true}
                }
            },
            calculable : true,
            series : [

                {
                    name:'面积模式',
                    type:'pie',
                    radius : [20, 120],
                    center : ['50%', '50%'],
                    roseType : 'area',
                    data:[
                        {value:value_list[0], name:key_list[0]},
                        {value:value_list[1], name:key_list[1]},
                        {value:value_list[2], name:key_list[2]},
                        {value:value_list[3], name:key_list[3]},
                        {value:value_list[4], name:key_list[4]},
                        {value:value_list[5], name:key_list[5]},
                        {value:value_list[6], name:key_list[6]},
                        {value:value_list[7], name:key_list[7]},
                        {value:value_list[8], name:key_list[8]},
                        {value:value_list[9], name:key_list[9]},
                        {value:value_list[10], name:key_list[10]},
                        {value:value_list[11], name:key_list[11]},
                        {value:value_list[12], name:key_list[12]},
                        {value:value_list[13], name:key_list[13]},
                        {value:value_list[14], name:key_list[14]}
                    ]
                }
            ]
        };
        myChart1.setOption(option1);
        // var keywords =['垃圾','项目','生活','建设','环保','城市','烟气','排放','发展','发电厂','设施','运营','工程','填埋','能力',
        //         '国家','系统','分类','居民','社会'
        //         ];
        // var valueA = [0.943,0.919,0.937,0.423,0.431,0.429,0.815,0.660
        //     ,0.402,0.202,0.271,0.261,0.116,0.149,0.163,0.122,0.188,0.224,0.194,0.110];
        // var valueB = [0.933,0.916,0.931,0.432,0.427,0.436,0.820,0.663,0.408,0.210,0.287,0.266,0.150,0.177,
        //     0.178,0.143,0.215,0.240,0.217,0.144];
        // var valueC = [1.202,1.149,1.177,0.921,0.875,0.838,1.056,0.985,0.864,0.736,0.799,0.787,0.744,0.719,0.749,0.671,0.735,
        //     0.740,0.728,0.707];
        // var valueD = [0.930,0.919,0.949,0.453,0.455,0.482,0.829,0.653,0.442,0.267,0.332,0.310,0.220,0.240,
        //     0.257,0.222,0.260,0.296,0.277,0.224];
        // // 构造相似度表
        // var str2 = '<tr>';
        // for(var i=0;i<20;i++){
        //     str2+='<td>'+keywords[i]+'</td>';
        // }
        // str2+='</tr><tr>';
        // for(var i=0;i<20;i++){
        //     str2+='<td>'+valueA[i]+'</td>';
        // }
        // str2+='</tr><tr>';
        // for(var i=0;i<20;i++){
        //     str2+='<td>'+valueB[i]+'</td>';
        // }
        // str2+='</tr><tr>';
        // for(var i=0;i<20;i++){
        //     str2+='<td>'+valueC[i]+'</td>';
        // }
        var str2 = '<tr><td>当前案例</td>';
        for(var i=0;i<org.textvalue.length;i++){
            str2+='<td>'+org.textvalue[i].toString().substring(0,5)+'</td>';
        }
        str2+='</tr>';
        // 往table中添加html代码
        var html = document.getElementById('table-body2').innerHTML;
        document.getElementById('table-body2').innerHTML=html+str2;
        // 取出type中的类型，绘图
        var type = org.type[org.type.length-1];
        var myChart3 = echarts.init(document.getElementById('chartTable'));
        var option3 = {
            title: {
                text: '案例对每个类型的相似度'
            },
            tooltip: {},
            legend: {
                data:['相似度值']
            },
            xAxis: {

                data: ["A类","B类","C类","D类"]
            },
            yAxis: {
                min: 0,
                max: 1.5
            },
            series: [{
                name: '相似度值',
                type: 'bar',
                data: [org.type[0].toFixed(7),org.type[1].toFixed(7),org.type[2].toFixed(7),org.type[3].toFixed(7)],
                itemStyle: {
							normal: {
								label: {
									show: true, //开启显示
									position: 'top', //在上方显示
									textStyle: { //数值样式
										color: 'black',
										fontSize: 16
									}
								}
							}
						}

            }]
        };
        myChart3.setOption(option3);
        },
    error: function () {
        alert("失败");
    }
    });
}