function baiyan() {
    $('#myBaiModal').modal('toggle');
    $("#Baimodal-body").html("sasa");
}
var Gra=function(){
this.elem=arguments[0];
this.options=arguments[1];
this.width=this.elem.width;
this.height=this.elem.height;
this.context=this.elem.getContext('2d');
this.deName=false;
this.isSymmetric=false;
// 有向图
this.pointSize=15;
this.pointData=[];
this.init();
}
Gra.prototype.init=function()
{
var name=this.options.name;
 this.num=this.options.data.length;
if(name&&name.length!=0)
    {
        this.deName=true;
    }
    this.drawPoint();
    this.drawEdge();
    this.initaction();
}
//绘顶点
Gra.prototype.drawPoint=function()
{
    var ctx=this.context;
    var num=this.num;
    var dia=(this.width<this.height) ? this.width : this.height;
    var centerx=this.width/2;
    var centery=this.height/2;
    var rad=2*Math.PI/num;
    for(var i=0;i<num;i++) {
        var y = (dia / 2 - 30) * Math.sin(rad * i) + centery;
        var x = (dia / 2 - 30) * Math.cos(rad * i) + centerx;
        ctx.beginPath();
        ctx.strokeStyle='#000';
        ctx.lineWidth=1;
        ctx.arc(x, y, this.pointSize, 0, 2 * Math.PI, false);
        ctx.stroke();
        this.pointData.push({x:x,y:y})
    }
}
//绘边
Gra.prototype.drawEdge=function()
{
    //判断是无向图和有向图
    var gra=this;
    var ctx=this.context;
    var data=this.options.data;
    var mydata=this.pointData;
    for(var i=0;i<data.length;i++)
    {
        for(j=0;j<data.length;j++){
            if(data[i][j]!=data[j][i])
            {
                this.isSymmetric=false;
            }
        }
    }
    ctx.save();
    ctx.strokeStyle='#000';
    ctx.lineWidth=1;
    ctx.font='12px 微软雅黑';
    ctx.textAlign='left';
    if(this.isSymmetric)
    {
            ctx.fillText('无向图', 14, 14);
            for(var i=0;i<data.length;i++)
            {
                for(j=0;j<i;j++){
                    if(data[i][j]!=0&&data[i][j]!=Number.POSITIVE_INFINITY)
                    {
                        ctx.moveTo(mydata[i].x,mydata[i].y);
                        ctx.lineTo(mydata[j].x,mydata[j].y);
                        ctx.stroke();
                    }
                }
            }
        }
    else
        {
            ctx.fillText('有向图', 14, 14);
            for(var i=0;i<data.length;i++) {
                for (j = 0; j < data.length; j++) {
                    if (data[i][j] != 0 && data[i][j] != Number.POSITIVE_INFINITY && i != j) {
                        //比例
                        //console.log(i + '> ' + j)
                        var rat = Math.atan((mydata[j].y - mydata[i].y) / (mydata[j].x - mydata[i].x));
                        var dex = Math.cos(rat + (Math.PI / 6)) * this.pointSize;
                        var dey = Math.sin(rat + (Math.PI / 6)) * this.pointSize;
                        var dex1 = Math.cos(rat - (Math.PI / 6)) * this.pointSize;
                        var dey1 = Math.sin(rat - (Math.PI / 6)) * this.pointSize;
                        if (j < i) {
                            ctx.strokeStyle='	#2F4F4F';
                            ctx.moveTo(mydata[j].x - dex, mydata[j].y - dey);
                            ctx.lineTo(mydata[i].x + dex1, mydata[i].y + dey1);
                            ctx.stroke();
                            //箭头
                            this.drawArrow(mydata[i].x + dex1, mydata[i].y + dey1,mydata[j].x - dex, mydata[j].y - dey);
                        }
                        else {
                            ctx.strokeStyle='#800000 ';
                            ctx.moveTo(mydata[i].x - dex1, mydata[i].y - dey1);
                            ctx.lineTo(mydata[j].x + dex, mydata[j].y + dey);
                            ctx.stroke();
                            //箭头
                            this.drawArrow(mydata[i].x - dex1, mydata[i].y - dey1, mydata[j].x + dex, mydata[j].y + dey);
                        }

                    }
                }
            }

        }
    ctx.textAlign='center';
    ctx.textBaseline='middle';
    mydata.forEach(function (item, index) {
        //console.log(item.x);
        ctx.fillStyle='#fff';
        ctx.beginPath();
        ctx.arc(item.x, item.y, gra.pointSize-1, 0, 2 * Math.PI, true);
        ctx.closePath();
        ctx.fill();
        ctx.fillStyle='#000';
        if(gra.deName) {
            ctx.fillText(gra.options.name[index], item.x, item.y);
        }
        else
        {
            ctx.fillText(index.toString(), item.x, item.y);
        }
    });

    ctx.restore();
}

Gra.prototype.drawArrow=function(x,y,x1,y1)
{
    var ctx=this.context;
    ctx.save();
    ctx.translate(x/2+x1/2,y/2+y1/2)
    if(x1-x>0)
        ctx.rotate(Math.atan((y1-y)/(x1-x))+Math.PI);
    else
        ctx.rotate(Math.atan((y1-y)/(x1-x)));
    ctx.fillStyle='#000';
    ctx.beginPath();
    ctx.moveTo(0,0);
    ctx.lineTo(10,5);
    ctx.lineTo(10,-5);
    ctx.closePath();
    ctx.fill();
    ctx.restore();
}
//拖动事件
Gra.prototype.initaction=function() {
    var gra = this;
    var canvas = gra.elem;
    var ctx = gra.context;
    var mydata = gra.pointData;
    canvas.onmousedown = function (ev) {
        var moveIndex = -1;
        for (var i = 0; i < mydata.length; i++) {
            if (ev.x < (mydata[i].x + gra.pointSize) && ev.x > (mydata[i].x - gra.pointSize) && ev.y < (mydata[i].y + gra.pointSize) && ev.y > (mydata[i].y - gra.pointSize)) {
                moveIndex = i;
                break;
            }
        }
        document.onmousemove = function (event) {
            if (moveIndex != -1) {
                ctx.clearRect(0, 0, gra.width, gra.height);
                mydata[moveIndex].x = event.pageX;
                mydata[moveIndex].y = event.pageY;
                for (var i = 0; i < mydata.length; i++) {
                    ctx.beginPath();
                    ctx.strokeStyle = '#000';
                    ctx.lineWidth = 1;
                    ctx.arc(mydata[i].x, mydata[i].y, gra.pointSize, 0, 2 * Math.PI, false);
                    ctx.stroke();
                }
                gra.drawEdge();
            }
        }
        document.onmouseup = function () {
            document.onmousemove = null;
            document.onmouseup = null;
        }
    }
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
    var option={
        name:['v0','v1','v2','v3','v4','v5','v6','v7','v8','v9','v10'],
        data:[ [0,0,0,0,0,0,0,1,0,0],
 [1,0,0,0,0,0,0,0,1,0],
 [0,1,0,0,0,0,0,0,1,0],
 [0,0,0,0,1,1,0,0,0,1],
 [0,0,1,0,0,0,0,0,0,1],
 [0,0,0,0,0,0,1,0,0,0],
 [0,0,0,0,0,0,0,0,0,0],
 [0,0,0,0,0,0,0,0,0,0],
 [0,0,0,0,0,0,1,0,0,0],
 [0,0,0,0,0,0,0,1,1,0]]
    };
    var gra = new Gra(document.getElementById('gra'),option);
}
