$(function() {  //this is jQuery's short notation for "fire all this when page is ready"
	$('#cal').on('change', function () {
		location.href = '/History?date=' + $('#cal').val();
	});
});