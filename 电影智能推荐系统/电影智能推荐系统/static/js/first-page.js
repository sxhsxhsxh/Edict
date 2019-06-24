$(function (){
	//轮播图：
	//保存图片路径
	var baseUrl = "../static/images/";
	var arr = ["img2.jpg","img3.jpg","img4.jpg","img5.jpg"];
	var index = 0;
	var timer = setInterval(autoPlay,1000);
	function autoPlay(){
		$("#banner li").eq(index).css("background","#fff");
		index++;
		if(index == arr.length){
			index = 0;
		}
		var url = baseUrl + arr[index];
		$("#banner img").attr("src",url);
		//索引修改
		$("#banner li").eq(index).css("background","red");
	}
	//鼠标移入移出 #banner
	$("#banner").mouseover(function (){
		//停止定时器
		clearInterval(timer);
	}).mouseout(function (){
		//重启定时器
		timer = setInterval(autoPlay,5000);
	})
	$("#banner a.left").click(function(){
		$("#banner li").eq(index).css("background-color","#fff");
		index--;
		if(index == -1){
			index = arr.length-1
			}
		var url = baseUrl+arr[index];
		$('#banner img').attr("src",url);
		$("#banner li").eq(index).css("background-color","blue");});
	$("#banner a.right").click(function(){
		autoPlay()});
	for(var i=0;i<arr.length;i++){
		$('#banner li')[i].ind=i;
	}console.log($("#banner li").eq(2));
	$("#banner li").click(function(){
		console.log(this.ind);
	})
	});














