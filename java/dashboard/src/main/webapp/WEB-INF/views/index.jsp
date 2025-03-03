<%@ page contentType="text/html; charset=utf-8"%>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core"%>
<%@ taglib prefix="fmt" uri="http://java.sun.com/jsp/jstl/fmt"%>
<jsp:include page="includes/header.jsp" />

<!DOCTYPE html>
<html lang="en">

<style>
*{margin:0; padding:0;}
#modal{
  display:none;
  position:fixed; 
  width:100%; height:100%;
  top:0; left:0; 
  background:rgba(0,0,0,0.3);
  box-shadow: 0 25px 40px -20px #3c4a56;
}
.modal-con{
  display:none;
  position:fixed;
  top:50%; left:50%;
  transform: translate(-50%,-50%);
  max-width: 90%;
  min-width: 200px;
  min-height: 30%;
  background:#fff;
  border-radius: 5px;
}
.modal-con #title{
  font-size:20px; 
  padding: 10px; 
  background : #9ADCFF;
  border-top-left-radius : 5px;
  border-top-right-radius : 5px;
  text-align: center;
}
.modal-con .con{
  font-size:15px; line-height:1.3;
  padding: 30px;
}
.modal-con .close{
  display:block;
  position:absolute;
  border: 0;
  background: #9ADCFF;
  border-radius: 5px;
  padding: 0.5rem 1rem;
  font-size: 0.8rem;
  line-height: 1;
  right:10px;
  bottom:10px;
}
#con {
	margin-left:10px;
	margin-right:10px;
}
</style>

<body id="page-top">

	<!-- Page Wrapper -->
	<div id="wrapper">

		<jsp:include page="includes/side-bar.jsp" />

			<!-- Main Content -->
			<div id="content">

				<!-- Begin Page Content -->
				<p>
				<div class="container-fluid">

					<!-- Page Heading -->
					<br>
					<div
						class="d-sm-flex align-items-center justify-content-between mb-4">
						<h1 class="h3 mb-0 text-gray-800">데이터 수집 현황</h1>
					</div>

					<!-- Content Row -->
					<div class="row">

						<!-- Earnings (Monthly) Card Example -->
						<div class="col-xl-3 col-md-6 mb-4">
							<div class="card border-left-primary shadow h-100 py-2">
								<div class="card-body">
									<div class="row no-gutters align-items-center">
										<div class="col mr-2">
											<div
												class="text-xs font-weight-bold text-primary text-uppercase mb-1">
												총 기사 개수</div>
											<div class="h5 mb-0 font-weight-bold text-gray-800">
												<fmt:formatNumber value="${totalData}" type="number" />
												개
											</div>
										</div>
										<div class="col-auto">
											<i class="fas fa-file fa-2x text-gray-300"></i>
										</div>
									</div>
								</div>
							</div>
						</div>

						<!-- Earnings (Monthly) Card Example -->
						<div class="col-xl-3 col-md-6 mb-4">
							<div class="card border-left-success shadow h-100 py-2">
								<div class="card-body">
									<div class="row no-gutters align-items-center">
										<div class="col mr-2">
											<div
												class="text-xs font-weight-bold text-success text-uppercase mb-1">
												데이터 수집 기간</div>
											<div class="h5 mb-0 font-weight-bold text-gray-800">
												<fmt:parseDate value="${min}" var="minDate" pattern="yyyyMMdd" />
												<fmt:parseDate value="${max}" var="maxDate" pattern="yyyyMMdd" />
												<fmt:formatDate value="${minDate}" pattern="yyyy.MM.dd" /> ~ 
												<fmt:formatDate value="${maxDate}" pattern="yyyy.MM.dd" />
											</div>
										</div>
										<div class="col-auto">
											<i class="fas fa-calendar fa-2x text-gray-300"></i>
										</div>
									</div>
								</div>
							</div>
						</div>

						<!-- Earnings (Monthly) Card Example -->
						<div class="col-xl-3 col-md-6 mb-4">
							<div class="card border-left-info shadow h-100 py-2">
								<div class="card-body">
									<div class="row no-gutters align-items-center">
										<div class="col mr-2">
											<div
												class="text-xs font-weight-bold text-info text-uppercase mb-1">빈도수
												TOP1 카테고리</div>
											<div class="row no-gutters align-items-center">
												<div class="col-auto">
													<div class="h5 mb-0 mr-3 font-weight-bold text-gray-800">${freq.cate}</div>
												</div>
											</div>
										</div>
										<div class="col-auto">
											<i class="fas fa-clipboard-list fa-2x text-gray-300"></i>
										</div>
									</div>
								</div>
							</div>
						</div>

						<!-- Pending Requests Card Example -->
						<div class="col-xl-3 col-md-6 mb-4">
							<div class="card border-left-warning shadow h-100 py-2">
								<div class="card-body">
									<div class="row no-gutters align-items-center">
										<div class="col mr-2">
											<div
												class="text-xs font-weight-bold text-warning text-uppercase mb-1">
												빈도수 TOP1 언론사</div>
											<div class="h5 mb-0 font-weight-bold text-gray-800">${freq.source}</div>
										</div>
										<div class="col-auto">
											<i class="fas fa-comments fa-2x text-gray-300"></i>
										</div>
									</div>
								</div>
							</div>
						</div>
					</div>

					<!-- Content Row -->

					<div class="row">

						<!-- Pareto Chart -->
						<div class="col-xl-8 col-lg-7">
							<div class="card shadow mb-4">
								<!-- Card Header - Dropdown -->
								<div
									class="card-header py-3 d-flex flex-row align-items-center justify-content-between">
									<h6 class="m-0 font-weight-bold text-primary">기사 수집 추이</h6>
									
								</div>
								<!-- Card Body -->
								<div class="card-body">
									<div class="chart-area">
										<div id="chartdiv"></div>
										<input type="hidden" value='${weekCount}' id="week">
									</div>
								</div>
							</div>
						</div>

						<!-- Pie Chart -->
						<div class="col-xl-4 col-lg-5">
							<div class="card shadow mb-4" style="height: 414.2px;">
								<!-- Card Header - Dropdown -->
								<div
									class="card-header py-3 d-flex flex-row align-items-center justify-content-between">
									<h6 class="m-0 font-weight-bold text-primary">카테고리별 분포</h6>
								</div>
								<!-- Card Body -->
								<div class="card-body">
									<div class="chart-pie pt-4 pb-2">
										<canvas id="myPieChart"></canvas>
										<input type="hidden" value='${map.label}' id="label">
										<input type="hidden" value='${map.count}' id="count">
									</div>
								</div>
							</div>
						</div>
					</div>
				</div>
				<p>
				<hr>

					<!-- Begin Page Content -->
				<div class="container-fluid">

					<!-- Page Heading -->
					<div
						class="d-sm-flex align-items-center justify-content-between mb-4">
						<h1 class="h3 mb-0 text-gray-800">전처리 현황</h1>
					</div>

					<!-- Content Row -->
					<div class="row">

						<!-- Earnings (Monthly) Card Example -->
						<div class="col-xl-3 col-md-6 mb-4">
							<div class="card border-left-primary shadow h-100 py-2">
								<div class="card-body">
									<div class="row no-gutters align-items-center">
										<div class="col mr-2">
											<div
												class="text-xs font-weight-bold text-primary text-uppercase mb-1">
												전처리 진행된 기사 수</div>
											<div class="h5 mb-0 font-weight-bold text-gray-800">
												<fmt:formatNumber value="${preData}" type="number" />개
											</div>
										</div>
										<div class="col-auto">
											<i class="fas fa-database fa-2x text-gray-300"></i>
										</div>
									</div>
								</div>
							</div>
						</div>

						<!-- Earnings (Monthly) Card Example -->
						<div class="col-xl-3 col-md-6 mb-4">
							<div class="card border-left-success shadow h-100 py-2">
								<div class="card-body">
									<div class="row no-gutters align-items-center">
										<div class="col mr-2">
											<div
												class="text-xs font-weight-bold text-success text-uppercase mb-1">
												전처리 진행된 기사 비율</div>
											<div class="h5 mb-0 font-weight-bold text-gray-800">${preRatio}%</div>
										</div>
										<div class="col-auto">
											<i class="fas fa-percent fa-2x text-gray-300"></i>
										</div>
									</div>
								</div>
							</div>
						</div>

						<!-- Earnings (Monthly) Card Example -->
						<div class="col-xl-3 col-md-6 mb-4">
							<div class="card border-left-info shadow h-100 py-2">
								<div class="card-body">
									<div class="row no-gutters align-items-center">
										<div class="col mr-2">
											<div
												class="text-xs font-weight-bold text-info text-uppercase mb-1">
												추출된 신조어 후보군 개수</div>
											<div class="row no-gutters align-items-center">
												<div class="col-auto">
													<div class="h5 mb-0 mr-3 font-weight-bold text-gray-800">
														<fmt:formatNumber value="${candidate}" type="number" />개
													</div>
												</div>
											</div>
										</div>
										<div class="col-auto">
											<i class="fas fa-clipboard-list fa-2x text-gray-300"></i>
										</div>
									</div>
								</div>
							</div>
						</div>
					</div>

					<!-- Content Row -->

					<div class="row">

						<!-- Area Chart -->
						<div class="col-xl-8 col-lg-7">
							<div class="card shadow mb-4">
								<!-- Card Header - Dropdown -->
								<div
									class="card-header py-3 d-flex flex-row align-items-center justify-content-between">
									<h6 class="m-0 font-weight-bold text-primary">전처리 후 가장 많이
										나온 신조어 후보군</h6>
								</div>
								<!-- Card Body -->
								<div class="card-body">
									<div class="chart-area">
										<div id=chartdiv2></div>
										<input type="hidden" value='${wordCloud}' id="wordCloud">
									</div>
								</div>
							</div>
						</div>

						<!-- Pie Chart -->
						<div class="col-xl-4 col-lg-5">
							<div class="card shadow mb-4" style="height: 414.2px;">
								<!-- Card Header - Dropdown -->
								<div
									class="card-header py-3 d-flex flex-row align-items-center justify-content-between">
									<h6 class="m-0 font-weight-bold text-primary">카테고리별 분포</h6>
									
								</div>
								<!-- Card Body -->
								<div class="card-body">
									<div class="chart-pie pt-4 pb-2">
										<canvas id="myPieChart2" width="277" height="245"
											style="display: block; width: 277px; height: 245px;"
											class="chartjs-render-monitor"></canvas>
										<input type="hidden" value='${map2.label}' id="label2">
										<input type="hidden" value='${map2.count}' id="count2">
									</div>
								</div>
							</div>
						</div>
					</div>



				</div>
				<!-- /.container-fluid -->
				<p>
				<hr>
					<!-- Begin Page Content -->
				<div class="container-fluid">

					<!-- Page Heading -->
					<div
						class="d-sm-flex align-items-center justify-content-between mb-4">
						<h1 class="h3 mb-0 text-gray-800">신조어 추출 현황</h1>
					</div>

					<!-- Content Row -->
					<div class="row">

						<!-- Earnings (Monthly) Card Example -->
						<div class="col-xl-3 col-md-6 mb-4">
							<div class="card border-left-success shadow h-100 py-2">
								<div class="card-body">
									<div class="row no-gutters align-items-center">
										<div class="col mr-2">
											<div
												class="text-xs font-weight-bold text-success text-uppercase mb-1">
												최종적으로 추출된 신조어 수</div>
											<div class="h5 mb-0 font-weight-bold text-gray-800">
												<fmt:formatNumber value="${newWordListCount}" type="number" />개
											</div>
										</div>
										<div class="col-auto">
											<i class="fas fa-eye fa-2x text-gray-300"></i>
										</div>
									</div>
								</div>
							</div>
						</div>
					</div>

					<!-- Content Row -->

					<div class="row">

						<!-- Pareto Chart -->
						<div class="col-xl-8 col-lg-7">
							<div class="card shadow mb-4">
								<!-- Card Header - Dropdown -->
								<div
									class="card-header py-3 d-flex flex-row align-items-center justify-content-between">
									<h6 class="m-0 font-weight-bold text-primary">신조어 추출 추이</h6>
									
								</div>
								<!-- Card Body -->
								<div class="card-body">
									<div class="chart-area">
										<div id="newWord"></div>
										<input type="hidden" value='${newWordListWeekCount}'
											id="newWordList">
									</div>
								</div>
							</div>
						</div>

						<!-- Pie Chart -->
						<div class="col-xl-4 col-lg-5">
							<div class="card shadow mb-4" style="height: 414.2px;">
								<!-- Card Header - Dropdown -->
								<div
									class="card-header py-3 d-flex flex-row align-items-center justify-content-between">
									<h6 class="m-0 font-weight-bold text-primary">카테고리별
										분포</h6>
									
								</div>
								<!-- Card Body -->
								<div class="card-body">
									<div class="chart-pie pt-4 pb-2">
										<canvas id="myPieChart3" width="277" height="245"
											style="display: block; width: 277px; height: 245px;"
											class="chartjs-render-monitor"></canvas>
										<input type="hidden" value='${map3.label}' id="label3">
										<input type="hidden" value='${map3.count}' id="count3">
									</div>
								</div>
							</div>
						</div>
						
						<!-- Area Chart -->
						<div class="col-xl-12 col-lg-12">
							<div class="card shadow mb-4">
								<!-- Card Header - Dropdown -->
								<div
									class="card-header py-3 d-flex flex-row align-items-center justify-content-between">
									<h6 class="m-0 font-weight-bold text-primary">기사에 20번 이상 나타난 신조어 (단어를 클릭하면 유사한 단어를 확인할 수 있습니다.)</h6>
								</div>
								<!-- Card Body -->
								<div class="card-body">
									<div class="chart-area">
										<div id=chartdiv3></div>
										<input type="hidden" value='${wordCloud2}' id="wordCloud2">
										<input type="hidden" value="javascript:openModal('modal1')" class="button modal-open">
										<div id="modal"></div>
										  <div class="modal-con modal1">
										    <p id="title"></p>
										    <div id="con"></div>
										    <a href="javascript:;" class="close">X</a>
										  </div>
									</div>
								</div>
							</div>
						</div>
					</div>
				</div>
				<!-- /.container-fluid -->
				<!-- End of Main Content -->

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
