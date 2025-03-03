
var weekData = JSON.parse(document.getElementById("week").value);

am5.ready(function() {

	// Create root element
	// https://www.amcharts.com/docs/v5/getting-started/#Root_element
	var root = am5.Root.new("chartdiv");


	// Create chart
	// https://www.amcharts.com/docs/v5/charts/xy-chart/
	var chart = root.container.children.push(am5xy.XYChart.new(root, {
		panX: false,
		panY: false,
		wheelX: "panX",
		wheelY: "zoomX",
		layout: root.verticalLayout
	}));

	var colors = chart.get("colors");

	var data = weekData;

	prepareParetoData();

	function prepareParetoData() {
		var total = 0;

		for (var i = 0; i < data.length; i++) {
			var value = data[i].count;
			total += value;
			data[i].pareto = total;
		}
	}


	// Create axes
	// https://www.amcharts.com/docs/v5/charts/xy-chart/axes/
	var xAxis = chart.xAxes.push(am5xy.CategoryAxis.new(root, {
		categoryField: "_id",
		renderer: am5xy.AxisRendererX.new(root, {
			minGridDistance: 30
		})
	}));

	xAxis.get("renderer").labels.template.setAll({
		paddingTop: 20
	});

	xAxis.data.setAll(data);

	var yAxis = chart.yAxes.push(am5xy.ValueAxis.new(root, {
		renderer: am5xy.AxisRendererY.new(root, {})
	}));



	var paretoAxisRenderer = am5xy.AxisRendererY.new(root, { opposite: true });
	var paretoAxis = chart.yAxes.push(am5xy.ValueAxis.new(root, {
		renderer: paretoAxisRenderer,
		extraTooltipPrecision: 1

	}));

	paretoAxisRenderer.grid.template.set("forceHidden", true);
	paretoAxis.set("numberFormat", "#");


	// Add series
	// https://www.amcharts.com/docs/v5/charts/xy-chart/series/
	var series = chart.series.push(am5xy.ColumnSeries.new(root, {
		xAxis: xAxis,
		yAxis: yAxis,
		valueYField: "pareto",
		categoryXField: "_id"
	}));
	
	chart.get("colors").set("colors", [
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
	
	series.columns.template.setAll({
		tooltipText: "{categoryX}: {count}" + "\n" + "누적합: {valueY}",
		tooltipY: 0,
		strokeOpacity: 0,
		cornerRadiusTL: 6,
		cornerRadiusTR: 6
	});

	series.columns.template.adapters.add("fill", function(fill, target) {
		return chart.get("colors").getIndex(series.dataItems.indexOf(target.dataItem));
	})


	// pareto series
	var paretoSeries = chart.series.push(am5xy.LineSeries.new(root, {
		xAxis: xAxis,
		yAxis: yAxis,
		valueYField: "count",
		categoryXField: "_id",
		stroke: root.interfaceColors.get("alternativeBackground"),
		maskBullets: false
	}));

	paretoSeries.bullets.push(function() {
		return am5.Bullet.new(root, {
			locationY: 1,
			sprite: am5.Circle.new(root, {
				radius: 5,
				fill: series.get("fill"),
				stroke: root.interfaceColors.get("alternativeBackground")
			})
		})
	})

	series.data.setAll(data);
	paretoSeries.data.setAll(data);

	// Make stuff animate on load
	// https://www.amcharts.com/docs/v5/concepts/animations/
	series.appear();
	chart.appear(1000, 100);

}); // end am5.ready()
