<%@ page contentType="text/html; charset=utf-8"%>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core"%>
<jsp:include page="includes/header.jsp" />


<!DOCTYPE html>
<html lang="en">
<script src="//cdn.amcharts.com/lib/5/index.js"></script>
<script src="//cdn.amcharts.com/lib/5/percent.js"></script>
<script src="//cdn.amcharts.com/lib/5/themes/Animated.js"></script>

<script src="https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js"></script>

<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js"></script>

<script>
				function prepro(newsUrl) {

					req_url = "http://localhost:5000/url_test/" + newsUrl;
					var form = $("form")[0];
					var form_data = new FormData(form);
					$.ajax({
						url : req_url,
						async : true,
						type : "POST",
						data : form_data,
						processData : false,
						contentType : false,
						success : function(data) {
							// ----------------- 전처리 파트 JSON ----------------- 
							
							console.log(data);	
							var prepro = new Array();
							
							$.each(data, function(key, value) {
								prepro.push(value);
							});
							
							$("#dateValue").empty();
							$("#wordValue").empty();
							var canvas = document.getElementById("canvas");
							canvas.getContext("2d").clearRect(0, 0, canvas.width, canvas.height);

							$("#result").empty();
							$("#result").append(prepro[0]);
							$("#result").append("<hr>");
							
							function preproPrint(prepro) {
								var y=1;
								for (i = 2; i <prepro.length+1; i++) {
									(function(x, y) {
										setTimeout(function() {
											$("#result").empty();
											$("#result").append(prepro[x-1]);
											$("#result").append("<hr>");
											
											if(x==prepro.length) {
												$("#modelButton").append("<input class='btn btn-primary' type='button' value='모델링' id='modeling' onclick=modeling(" + 'newsUrl' + ")>");
												$("#modelButton").append("<input type='hidden' id='newsUrl' value='" + newsUrl + "'>");
											}
											
										}, 3000 * (x-y));
									})(i, y);
								}
							}
							preproPrint(prepro);
						},
						error : function(e) {
							alert(e);
						}
					})
				}

</script>

<script>

		function modeling() {
			var newsUrl = document.getElementById('newsUrl').value;
			
			$("#result").empty();
			$("#modelButton").empty();
			
			req_url = "http://localhost:5000/url_test2/" + newsUrl;
			var form = $("form")[0];
			var form_data = new FormData(form);
			$.ajax({
				url : req_url,
				async : true,
				type : "POST",
				data : form_data,
				processData : false,
				contentType : false,
				beforeSend: function(){
			        $('#lottie').show();
			    },
			    complete: function(){
			        $('#lottie').hide();
			    },
				success : function(data) {
					
					console.log(data);
					
					// ----------------- 모델링 파트 JSON ----------------- 
					
					var cate = new Array();
					var dateValue = new Array();
					var modelKey = ["soynlp로 추출한 모든 명사 수",
								   "조사 및 동사 등의 단어 제거",
								   "사전 비교 후 사전에 있는 단어 제거 후 단어 수",
								   "신조어 등장 기사수 기준 상위 25% 단어 추출 후 단어 수",
								   "기사 본문의 홑따옴표 내 단어로 추출한 고유명사 추가 후 단어 수",
								   "이전 추출 신조어와 비교 후 해당 카테고리 및 기간의 총 신조어 수",
								   "불용어 처리 및 잘못 추출된 단어 적용 완료 후 단어 수"];
					var modelValue = new Array();
					var wordValue = new Array();
	
					$.each(data, function(key, value) {
						modelValue.push(value);
					});
					
					for(i=0; i<modelValue[13].length; i++) {
						wordValue.push(modelValue[13][i]);
					}
					
					cate.push(modelValue.shift());
					cate.push(modelValue.shift());
					dateValue.push(modelValue.shift());
					dateValue.push(modelValue.shift());
					modelValue.pop();
					modelValue.pop();
					
					console.log(cate)
					console.log(dateValue)
					console.log(modelKey)
					console.log(modelValue)
					console.log(wordValue)
					
					barChart(cate, dateValue, modelKey, modelValue, wordValue);
					
				},
				error : function(e) {
					alert(e);
				}
			})
		}
		
		
</script>


<body id="page-top">

	<!-- Page Wrapper -->
	<div id="wrapper">

		<jsp:include page="includes/side-bar.jsp" />

		<!-- Content Wrapper -->

		<!-- Begin Page Content -->
		<div class="container-fluid">

			<!-- Page Heading -->
			<br>
			<p>
			<h1 class="h3 mb-2 text-gray-800">전처리 과정</h1>
			<p class="mb-4">
				기사 원문이 전처리 되는 과정을 순차적으로 보여드리는 페이지입니다.<br>
				전처리가 완료된 후에는 모델링 버튼을 통해 신조어가 추출되는 과정을 차트로 확인할 수 있습니다.
			</p>

			<!-- DataTales Example -->
			<div class="card shadow mb-4">
				<div class="card-header py-3">
					<div align="center">
						<h6 class="m-0 font-weight-bold text-primary">
							<form
								class="d-none d-sm-inline-block form-inline mr-auto ml-md-3 my-2 my-md-0 mw-100">
								<div class="input-group">
									<div class="input-group-append">
										<button class="btn btn-primary" type="button" onclick="prepro('E8WGPEJgoh')">
										전처리 (1)
										</button>
									</div>
									<div class="input-group-append">
										<button class="btn btn-primary" type="button" onclick="prepro('EoKIeCpkAN')">
										전처리 (2)
										</button>
									</div>
									<div class="input-group-append">
										<button class="btn btn-primary" type="button" onclick="prepro('Ewt0HkkfhO')">
										전처리 (3)
										</button>
									</div>
									<div class="input-group-append">
										<button class="btn btn-primary" type="button" onclick="prepro('EHvxRyMXKN')">
										전처리 (4)
										</button>
									</div>
									<div class="input-group-append">
										<button class="btn btn-primary" type="button" onclick="prepro('ELgYKhPwjR')">
										전처리 (5)
										</button>
									</div>
								</div>
							</form>
						</h6>
					</div>
				</div>
				<div class="card-body">
					<div class="table-responsive">
						<table class="table table-bordered" id="dataTable" width="100%"
							cellspacing="0">
						</table>
						
						<div id="result">						

						</div>
						<div id="modelButton" name="modelButton">
							
						</div>
						<div style="width:100%;">
							<div id="lottie" align="center">
								<lottie-player src="https://assets2.lottiefiles.com/packages/lf20_mbrocy0r.json"  background="transparent"  speed="1"  style="width: 500px; height: 500px;"  loop  autoplay></lottie-player>							
							</div>
							<div id="dateValue" value="" style="text-align:center;"></div>
							<canvas id="canvas" height="150"></canvas>
						</div>
						<div id="wordValue" value="" style="text-align:center; color:red;"></div>
					</div>
				</div>
			</div>

		</div>
		<!-- /.container-fluid -->

	</div>
	<!-- End of Main Content -->

	<!-- Scroll to Top Button-->
	<a class="scroll-to-top rounded" href="#page-top"> <i
		class="fas fa-angle-up"></i>
	</a>

	<!— toJSON —>

	<jsp:include page="includes/footer.jsp" />

</body>
<script>
$('#lottie').hide();
</script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.7.2/Chart.min.js"></script>
</html>