am5.ready(function() {

// Create root element
// https://www.amcharts.com/docs/v5/getting-started/#Root_element
var root = am5.Root.new("chartdiv10");

// Set themes
// https://www.amcharts.com/docs/v5/concepts/themes/

// Create chart
// https://www.amcharts.com/docs/v5/charts/percent-charts/sliced-chart/
var chart = root.container.children.push(am5percent.SlicedChart.new(root, {
  layout: root.verticalLayout
}));

// Create series
// https://www.amcharts.com/docs/v5/charts/percent-charts/sliced-chart/#Series
var series = chart.series.push(am5percent.FunnelSeries.new(root, {
  alignLabels: true,
  orientation: "vertical",
  valueField: "value",
  categoryField: "category",
  bottomRatio: 0.2,
  height: 300
}));

series.get("colors").set("colors", [
	  am5.color(0x9ADCFF),
	  am5.color(0xFFF89A),
	  am5.color(0xFFB2A6),
	  am5.color(0xFF8AAE),
	  am5.color(0xEA99D5),
	  am5.color(0xBFFFF0),
	  am5.color(0xF0FFC2),
	  am5.color(0xFFE4C0),
	  am5.color(0xFFBBBB)
	]);


// Set data
// https://www.amcharts.com/docs/v5/charts/percent-charts/sliced-chart/#Setting_data
series.data.setAll([
//  { value: 1415, category: "Soynlp로 추출한 명사" },
//  { value: 1282, category: "어미,조사,동사 등을 제거 후 추출한 명사" },
//  { value: 1282, category: "한글자 제거 후 명사" },
  { value: 72, category: "사전 비교 후 남은 명사" },
  { value: 19, category: "신조어 등장 기사 수 기준 상위 25% 명사" },
  { value: 20, category: "홑 따옴표 내의 명사를 추가 후 남은 명사" },
  { value: 9, category: "이전 추출 신조어와 비교 후 남은 신조어" },
  { value: 9, category: "불용어 처리 후 남은 신조어" },
  { value: 0, category: "입력 기사에서의 최종 신조어" }
]);


// Play initial series animation
// https://www.amcharts.com/docs/v5/concepts/animations/#Animation_of_series
series.appear();


// Create legend
// https://www.amcharts.com/docs/v5/charts/percent-charts/legend-percent-series/
//var legend = chart.children.push(am5.Legend.new(root, {
//  centerX: am5.p50,
//  x: am5.p50,
//  marginTop: 15,
//  marginBottom: 15
//}));

legend.data.setAll(series.dataItems);


// Make stuff animate on load
// https://www.amcharts.com/docs/v5/concepts/animations/
chart.appear(1000, 100);

}); // end am5.ready()