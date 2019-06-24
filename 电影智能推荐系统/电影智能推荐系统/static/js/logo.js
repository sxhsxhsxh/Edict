//获取姓名框,密码框的的输入内容
$(this).change(function(){
	var account = $(".account1").val();
	var password = $(".password").val()
})
//点击删除按钮,信息清零
$(document).ready(function(){ 
	$(".cancel-1").click(function(){
		$(".account1").val("");
		$(".password").val("")
	})
});

