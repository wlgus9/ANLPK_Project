<%@ page contentType="text/html; charset=utf-8"%>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core"%>
<jsp:include page="includes/header.jsp" />


<!DOCTYPE html>
<html lang="en">
<script src="//cdn.amcharts.com/lib/5/index.js"></script>
<script src="//cdn.amcharts.com/lib/5/percent.js"></script>
<script src="//cdn.amcharts.com/lib/5/themes/Animated.js"></script>
<script
	src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js"></script>

<script>
	$(function() {
		$("button[type = button]").click(
				function() {
					req_url = "http://localhost:5000/url_test";
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
							//var description = ["설명1", "설명2", "설명3", "설명4", "설명5", "설명6"];
							
							$.each(data, function(key, value) {
								prepro.push(value);
							});

							function preproPrint(prepro) {
								var y=1;
								for (i = 2; i <prepro.length+2; i++) {
									(function(x, y) {
										setTimeout(function() {
											$("#result").empty();
											$("#result").append(prepro[x-2]);
											$("#result").append("<hr>");
											
											if(x > prepro.length) {
												$("#modelButton").append("<input class='btn btn-primary' type='button' value='모델링' id='modeling' onclick=modeling()></input>");	
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
				})
	})
</script>

<script>

		/* function modeling() {
			req_url = "http://localhost:5000/url_test2";
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
			        $('#image').show();
			    },
			    complete: function(){
			        $('#image').hide();
			    },
				success : function(data) {
					
					console.log(data);
					
					// ----------------- 모델링 파트 JSON ----------------- 
					var valueList = new Array();
					var modelList = new Array();
					var wordList = new Array();

					$.each(data, function(key, value) {
						console.log("valueList :: " + key, value);
						valueList.push(value);
					});

					$.each(valueList[4], function(key, value) {
						console.log("modelList :: " + value);
						modelList.push(value);
					});

					for (i = 0; i < valueList[5].length; i++) {
						console.log("wordList :: " + valueList[5][i]);
						wordList.push(valueList[5][i]);
					} 

					valueList.splice(4, 2);
					
					var modeling = valueList.concat(modelList).concat(wordList);
					function modelingPrint(modeling) {
						$("#modelButton").empty();
						var y=1;
						for (i = 2; i <modeling.length+2; i++) {
							(function(x) {
								setTimeout(function() {
									
									if(x < 13) {
										$("#result").append(modeling[x-2]);
										$("#result").append("<hr>");										
									} else {
										$("#result").append(modeling[x-2] + "&nbsp;");
									}
									
								}, 1000 * x);
							})(i);
						}								
					}
					
					modelingPrint(modeling);
					
				},
				error : function(e) {
					alert();
				}
			})
		} */
		var test = new Array();
		function modeling() {
			req_url = "http://localhost:5000/url_test2";
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
					
					console.log(data);
					$("#modelButton").empty();
						
					$("#result").append(data);
					$("#result").append("<hr>");										
					modeling2();
						
					
					
				},
				error : function(e) {
					alert();
				}
			})
		}
		
		function modeling2() {
			req_url = "http://localhost:5000/url_test3";
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
					
					console.log(data);
					setTimeout(function() {
						
						$("#result").append(data);
						$("#result").append("<hr>");										
						modeling3();
						
					}, 1000);
					
				},
				error : function(e) {
					alert();
				}
			})
		}
		
		function modeling3() {
			req_url = "http://localhost:5000/url_test4";
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
					
					console.log(data);
					setTimeout(function() {
						
						$("#result").append(data);
						$("#result").append("<hr>");										
						
					}, 1500);
					
				},
				error : function(e) {
					alert();
				}
			})
		}
		
		function modelingPrint(test) {
			$("#modelButton").empty();
			var y=1;
			for (i = 2; i <modeling.length+2; i++) {
				(function(x) {
					setTimeout(function() {
						
						$("#result").append(test[x-2]);
						$("#result").append("<hr>");										
						
					}, 1000 * x);
				})(i);
			}								
		}
		console.log(test);
		//modelingPrint(test);
		
</script>


<body id="page-top">

	<!-- Page Wrapper -->
	<div id="wrapper">

		<jsp:include page="includes/side-bar.jsp" />

		<!-- Content Wrapper -->

		<!-- Begin Page Content -->
		<div class="container-fluid">

			<!-- Page Heading -->
			<p>
			<h1 class="h3 mb-2 text-gray-800">전처리 과정</h1>
			<p class="mb-4">
				DataTables is a third party plugin that is used to generate the demo
				table below. For more information about DataTables, please visit the
				<a target="_blank" href="https://datatables.net">official
					DataTables documentation</a>.
			</p>

			<!-- DataTales Example -->
			<div class="card shadow mb-4">
				<div class="card-header py-3">
					<div align="center">
						<h6 class="m-0 font-weight-bold text-primary">
							<form
								class="d-none d-sm-inline-block form-inline mr-auto ml-md-3 my-2 my-md-0 mw-100">
								<div class="input-group">
									<input type="text" class="form-control form-control-sm"
										placeholder="Search for..." aria-label="Search"
										aria-describedby="basic-addon2"
										style="height: 38px; width: 500px;">
									<div class="input-group-append">
										<button class="btn btn-primary" type="button">
											<i class="fas fa-search fa-sm"></i>
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
							<!-- <div class="loading-container">
    							<div class="loading"></div>
							    <div id="loading-text">loading</div>
							</div> -->
						</div>
						<div id="modelButton">
							<input class='btn btn-primary' type='button' value='모델링' id='modeling' onclick=modeling()></input>
						</div>
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

</html>