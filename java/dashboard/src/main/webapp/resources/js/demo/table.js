function table() {
	var new_word = JSON.parse(document.getElementById("new_word").value);
	console.log(new_word);
	$("#new_word").append(new_word);	
}
