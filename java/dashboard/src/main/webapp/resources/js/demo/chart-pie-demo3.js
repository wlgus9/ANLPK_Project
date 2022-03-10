
// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#858796';

// Pie Chart Example
var ctx = document.getElementById("myPieChart3");

var labelData = document.getElementById("label3").value.split('[').join('').split(']').join('');
var labels = labelData.toString().split(",");

var countData = document.getElementById("count3").value.split('[').join('').split(']').join('');
var counts = countData.toString().split(",");


//var labels = JSON.parse(document.getElementById("label").value);
//var counts = JSON.parse(document.getElementById("count").value);

console.log(labels);
console.log(labels.length);

console.log(counts);
console.log(counts.length);

var myPieChart = new Chart(ctx, {
  type: 'doughnut',
  data: {	
    
    datasets: [{
      data: counts,
      backgroundColor: ['#9ADCFF', '#FFF89A', '#FFB2A6', '#FF8AAE','#EA99D5','#BFFFF0','#F0FFC2','#FFE4C0','#FFBBBB','#20c9a6'],
      hoverBackgroundColor: ['#2e59d9', '#17a673', '#2c9faf', '#ffb700'],
      hoverBorderColor: "rgba(234, 236, 244, 1)",
    }],
    labels: labels,
  },
  options: {
    maintainAspectRatio: false,
    tooltips: {
      backgroundColor: "rgb(255,255,255)",
      bodyFontColor: "#858796",
      borderColor: '#dddfeb',
      borderWidth: 1,
      xPadding: 15,
      yPadding: 15,
      displayColors: false,
      caretPadding: 10,
    },
    legend: {
      display: true,
      position : 'bottom'
    },
    cutoutPercentage: 50,
  },
});
