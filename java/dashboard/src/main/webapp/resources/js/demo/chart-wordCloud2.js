// Create root element
// https://www.amcharts.com/docs/v5/getting-started/#Root_element

var root = am5.Root.new("chartdiv3");
var data = JSON.parse(document.getElementById("wordCloud2").value);
console.log(data);

// Set themes
// https://www.amcharts.com/docs/v5/concepts/themes/
root.setThemes([
	am5themes_Animated.new(root)
]);


// Add wrapper container
var container = root.container.children.push(am5.Container.new(root, {
	width: am5.percent(100),
	height: am5.percent(45),
	layout: root.verticalLayout
}));

// Add series
// https://www.amcharts.com/docs/v5/charts/word-cloud/
var series = container.children.push(am5wc.WordCloud.new(root, {
	categoryField: "new_word",
	valueField: "freq",
	calculateAggregates: true, // this is needed for heat rules to work
	colors: am5.ColorSet.new(root, {}),
	randomness: 0.2,
	maxFontSize: am5.percent(30),
	minFontSize: am5.percent(5)
}));

// Configure labels
series.labels.template.setAll({
	paddingTop: 5,
	paddingBottom: 5,
	paddingLeft: 5,
	paddingRight: 5,
	fontFamily: "Courier New",
	cursorOverStyle: "pointer"
});


series.labels.template.events.on("click", function(ev) {
	const category = ev.target.dataItem.get("category");
	$("#title").empty();
	$("#con").empty();
	var title = document.getElementById('title');
	title.insertAdjacentHTML('afterbegin', category);
	
	var req_url = "http://localhost:5000/get_similar_words/" + category;
	$.ajax({
		url: req_url,
		async: true,
		type: "POST",
		processData: false,
		contentType: false,
		success: function(data) {
			console.log(data);
			var json = new Array();
			
			$.each(data, function(key, value) {
				console.log(value);
				json.push(value);
			});

			function openModal(modalname) {
				
				document.get
				$("#modal").fadeIn(300);
				$("." + modalname).fadeIn(300);
				
				if(data.length == 0) {
					document.getElementById("con").innerHTML = "해당 신조어와 유사한 단어가 존재하지 않습니다.";					
				} else {
					for(i=0; i<json.length; i++) {
						var a = i+1 + ". " + json[i] + "<br>";
						var b = document.getElementById("con");
						b.innerHTML = b.innerHTML + a;
					}
				}
			}
			openModal("modal1");

			$("#modal, .close").on('click', function() {
				$("#modal").fadeOut(300);
				$(".modal-con").fadeOut(300);
				
			});

		},
		error: function(e) {
			alert("error!");
		}
	});
})

// Data from:
// https://insights.stackoverflow.com/survey/2021#section-most-popular-technologies-programming-scripting-and-markup-languages
series.data.setAll(data);