function barChart(cate, dateValue, modelKey, modelValue, wordValue) {
	document.getElementById("dateValue").innerHTML = "<b>" + cate[0] + " 분야의 " + cate[1] + " 기사 (총 " + modelValue[0] + "개)</b><br>" + "<b>" + dateValue[0] + " ~ " + dateValue[1] + "</b>";
	modelValue.shift();
	
	if(wordValue.length==0) {
		document.getElementById("wordValue").innerHTML = "<b>추출된 신조어가 없습니다.<b>";
	} else {
		document.getElementById("wordValue").innerHTML = "<b>입력된 기사에서의 최종 신조어<b><br>";
		for(i=0; i<wordValue.length; i++) {
			if(i==wordValue.length-1) {
				var a = "<b>" + wordValue[i] + "</b>";
				var b = document.getElementById("wordValue");
				b.innerHTML = b.innerHTML + a;
			} else {
				var a = "<b>" + wordValue[i] + "</b>" + ", ";
				var b = document.getElementById("wordValue");
				b.innerHTML = b.innerHTML + a;
			}		
		}
	}

	new Chart(document.getElementById("canvas"), {
    type: 'horizontalBar',
    data: {
        labels: modelKey,
        datasets: [{
            
            data: modelValue,
            backgroundColor: [
		      'rgba(255, 99, 132, 0.2)',
		      'rgba(255, 159, 64, 0.2)',
		      'rgba(255, 205, 86, 0.2)',
		      'rgba(75, 192, 192, 0.2)',
		      'rgba(54, 162, 235, 0.2)',
		      'rgba(153, 102, 255, 0.2)',
		      'rgba(201, 203, 207, 0.2)'],
		    borderColor: [
		      'rgb(255, 99, 132)',
		      'rgb(255, 159, 64)',
		      'rgb(255, 205, 86)',
		      'rgb(75, 192, 192)',
		      'rgb(54, 162, 235)',
		      'rgb(153, 102, 255)',
		      'rgb(201, 203, 207)']
        }]
    },
    options: {
       legend: {
           display: false
        }
    }
});	
}