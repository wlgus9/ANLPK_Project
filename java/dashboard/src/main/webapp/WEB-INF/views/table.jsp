<%@ page contentType="text/html; charset=utf-8"%>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core"%>
<jsp:include page="includes/header.jsp" />
<%@ page import="java.util.List"%>
<%@ page import="java.util.ArrayList"%>
<%@ page import="org.json.simple.JSONArray"%>
<!DOCTYPE html>
<html lang="en">


<body id="page-top">
	<!-- Page Wrapper -->
	<div id="wrapper">

		<jsp:include page="includes/side-bar.jsp" />

		<!-- Content Wrapper -->
		<div id="content-wrapper" class="d-flex flex-column">

			<!-- Main Content -->
			<div id="content">

				<!-- Begin Page Content -->
				<div class="container-fluid">

					<!-- Page Heading -->
					<br>
					<p>
					<h1 class="h3 mb-2 text-gray-800">신조어 리스트</h1>
					<p class="mb-4">
						프로젝트 기간 동안 추출한 신조어입니다. 
					</p>

					<!-- DataTales Example -->
					<div class="card shadow mb-4">
						<div class="card-header py-3">
							<h6 class="m-0 font-weight-bold text-primary">신조어 리스트</h6>
						</div>
						<div class="card-body">
							<div class="table-responsive">
								<table class="table table-bordered" id="dataTable" width="100%"
									cellspacing="0">
									<thead>
										<tr>
											<th style="width:250px;">신조어</th>
											<th>빈도수</th>
											<th>카테고리</th>
											<th>단어가 등장한 주차</th>
											<th>해당 주차의 시작 날짜</th>
											<th>해당 주차의 끝 날짜</th>
										</tr>
									</thead>
									<tbody>
										<c:forEach var="item" items="${table}">
											<tr>
												<td>${item[0]}</td>
												<td>${item[1]}</td>
												<td>${item[2]}</td>
												<td>${item[3]}</td>
												<td>${item[4]}</td>
												<td>${item[5]}</td>
											</tr>
										</c:forEach>
									</tbody>
								</table>
							</div>
						</div>
					</div>

				</div>
				<!-- /.container-fluid -->

			</div>
			<!-- End of Main Content -->

		</div>
		<!-- End of Content Wrapper -->

	</div>
	<!-- End of Page Wrapper -->

	<!-- Scroll to Top Button-->
	<a class="scroll-to-top rounded" href="#page-top"> <i
		class="fas fa-angle-up"></i>
	</a>

	<!-- toJSON -->

	<jsp:include page="includes/footer.jsp" />

</body>

</html>
