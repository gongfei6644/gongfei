$(function (){
	//�ֲ�ͼ��
	//����ͼƬ·��
	var baseUrl = "../images/index/";
	var arr = ["index_banner3.jpg","index_banner1.jpg","index_banner2.jpg","index_banner4.jpg","index_banner5.jpg"];
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
		//�����޸�
		$("#banner li").eq(index).css("background","red");
	}
	//��������Ƴ� #banner
	$("#banner").mouseover(function (){
		//ֹͣ��ʱ��
		clearInterval(timer);
	}).mouseout(function (){
		//������ʱ��
		timer = setInterval(autoPlay,1000);
	})
	//ǰ�󷭣�ͼƬ
	$("#banner a.left").click(function (){
		$("#banner li").eq(index).css("background","#fff");
		index--;
		if(index == -1){
			index = arr.length-1;
		}
		var url = baseUrl + arr[index];
		$("#banner img").attr("src",url);
		//�����޸�
		$("#banner li").eq(index).css("background","red");
	})
	$("#banner a.right").click(function (){
		autoPlay();
	})
	//����li,�������ind
	//each()��jquery�ṩ�ı�������	
	for(var i = 0;i < arr.length;i++ ){
		//Ϊ�����������ind,��ʾ�±�
		$("#banner li")[i].ind = i;
	}
	console.log($("#banner li").eq(2));
	$("#banner li").click(function (){
		console.log(this.ind);
	});


	
	

	




})