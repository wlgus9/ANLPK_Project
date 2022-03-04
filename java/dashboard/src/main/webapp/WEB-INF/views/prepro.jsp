<%@ page contentType="text/html; charset=utf-8"%>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core"%>
<jsp:include page="includes/header.jsp" />

<!DOCTYPE html>
<html lang="en">

<script
	src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js"></script>
<script>
	$(function() {
		$("button[type = button]").click(function() {
			req_url = "http://localhost:5000/url_test"
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

					var valueList = new Array();

					$.each(data, function(key, value) {
						$.each(value, function(key, value) {
							if (key == "count") {
								valueList.push(value);
							}
						});
					});

					for (i = 0; i < data.length; i++) {
						(function(x) {
							setTimeout(function() {
								console.log(valueList[x]);
								$("#result").append(valueList[x]);
								$("#result").append("<br>");
							}, 1000 * x);
						})(i);
					}

				},
				error : function(e) {
					alert();
				}
			})
		})
	})
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
			<h1 class="h3 mb-2 text-gray-800">Tables</h1>
			<p class="mb-4">
				DataTables is a third party plugin that is used to generate the demo
				table below. For more information about DataTables, please visit the
				<a target="_blank" href="https://datatables.net">official
					DataTables documentation</a>.
			</p>

			<!-- DataTales Example -->
			<div class="card shadow mb-4">
				<div class="card-header py-3">
					<h6 class="m-0 font-weight-bold text-primary">
						<form class="d-none d-sm-inline-block form-inline mr-auto ml-md-3 my-2 my-md-0 mw-100 navbar-search">
							<div class="input-group">
								<input type="text" class="form-control form-control-sm"
									placeholder="Search for..." aria-label="Search"
									aria-describedby="basic-addon2"
									style="height: 38px; width: 250px;">
								<div class="input-group-append">
									<button class="btn btn-primary" type="button">
										<i class="fas fa-search fa-sm"></i>
									</button>
								</div>
							</div>
						</form>
					</h6>
				</div>
				<div class="card-body">
					<div class="table-responsive">
						<table class="table table-bordered" id="dataTable" width="100%"
							cellspacing="0">
						</table>
						<div id="result"></div>
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

	<!-- toJSON -->

	<jsp:include page="includes/footer.jsp" />

</body>

</html>
