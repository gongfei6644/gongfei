$(function (){
	//1.全选和取消全选
	var isChecked = false;
	$(".checkAll").click(function (){
		isChecked = !isChecked;
		if(isChecked){
			//切换选中样式
			$(this)
				.attr("src","../images/cart/product_true.png");
			$(".checkImg")
				.attr("src","../images/cart/product_true.png")
				.attr("checked","true");//修改状态标记
		}else{
			$(this)
				.attr("src","../images/cart/product_normal.png")
			$(".checkImg")
				.attr("src","../images/cart/product_normal.png")
				.removeAttr("checked");
		}
		total();
	})
	//2.反选
	$(".checkImg").click(function (){
		//如果当前元素存在checked属性值，
		//说明原本是选中状态，需要改为取消选中
		if($(this).attr("checked")){
			$(this)
				.attr("src","../images/cart/product_normal.png")
				.removeAttr("checked");
		}else{
			$(this).attr("checked","true")
				.attr("src","../images/cart/product_true.png");

		}
		//反选：被选中的图片数量与列表中图片数量一致，
		//视为全选
		if($("img[checked]").length == $(".checkImg").length){
			$(".checkAll")
				.attr("src","../images/cart/product_true.png");
			//修改全选按钮的状态标记
			isChecked = true;
		}else{
			$(".checkAll")
				.attr("src","../images/cart/product_normal.png");
			//修改全选按钮的状态标记
			isChecked = false;
		}
		total()

	})
	//3.数量加减
	$(".add").click(function (){
		//获取输入框的值
		var value = $(this).prev().val();
		//值+1
		$(this).prev().val(++value);
		//修改总金额
		changePrice($(this),value);
		total()
	})
	$(".minus").click(function (){
		var value = $(this).next().val();
		value--;
		if(value < 1){
			value = 1;
		}
		$(this).next().val(value);
		//修改总金额
		changePrice($(this),value);
		total();
	})
	//监听输入框数量变化
	$(".gcount input").blur(function (){
		//输入框的值是正整数
		//出现小数，负数，非数字字符串，一律显示为1
		var value = $(this).val();
		var r1 = Number(value);//是否数字字符串
		var r2 = value >= 1;//是否是>=1的正数
		//使用小数点分割字符串，
		//如果不存在小数点，数组长度为1，存在，>1
		var r3 = value.split('.').length == 1;
		if(r1 && r2 && r3){
			//value合法
	
		}else{
			value = 1;
			$(this).val(value);
		}
		changePrice($(this),value)
		total();
	})
	//移除操作
	$(".item .action").click(function (){
		$(this).parent().remove();
		total();
	})
	
	//计算总数量和总价格
	function total(){
		var num = 0;//总数量
		var sum = 0;//总价格
		//获取被选中商品的总数量和总价格进行累加
		//each()遍历列表，
		//每取到一个元素就自动调用相关函数
		$("img[checked]").each(function (){
			//当前获取的元素
			var n = Number($(this).parents(".item")
				.find(".gcount input").val());
			var pstr = $(this).parents(".item")
				.find(".gsum b").html();
			var price = Number(pstr.substring(1));
			num += n;
			sum += price;
		})
		//显示
		$(".total-num").html(num);
		$(".total-price").html(sum+"元");
	}



	
	//价格联动
	function changePrice(that,n){//元素对象，数量
		//获取单价"￥288"
		var pstr = that.parents(".item")
				.find(".gprice span").html();
		var price = pstr.substring(1);//"288"
		//获取总价
		//总价保留两位小数
		var sum = (n*price).toFixed(2);
		that.parents(".item")
				.find(".gsum b").html("￥"+sum);

	}

	

	/*
	var s = "5.3";
	var s2 = "53";
	console.log(s.split("."),s2.split("."));
	*/



})