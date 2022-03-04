// Create root element
// https://www.amcharts.com/docs/v5/getting-started/#Root_element

var root = am5.Root.new("chartdiv2");
var data = JSON.parse(document.getElementById("wordCloud").value);
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
  randomness:0.2,
  maxFontSize:am5.percent(30),
  minFontSize:am5.percent(5)
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
  //window.open("https://stackoverflow.com/questions/tagged/" + encodeURIComponent(category));
  //window.open("http://naver.com");
  alert("hi");
});

// Data from:
// https://insights.stackoverflow.com/survey/2021#section-most-popular-technologies-programming-scripting-and-markup-languages
series.data.setAll(data);