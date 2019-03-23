var Gra=function(){
this.elem=arguments[0];
this.options=arguments[1];
this.width=this.elem.width;
this.height=this.elem.height;
this.context=this.elem.getContext('2d');
this.deName=false;
this.isSymmetric=true;
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