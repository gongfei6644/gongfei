$(function (){
	//获取输入框，监听失去焦点状态
	$("[name=uname]").blur(function (){
		//判断长度为0或空字符串
		if ($(this).val().length == 0 || $(this).val() == ""){
			//给span提示文本
			$(this).siblings("span").html("username can't void!").css("color","red");
		}
	});
});