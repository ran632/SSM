$(function() {  //this is jQuery's short notation for "fire all this when page is ready"
	$('#emplist').on('change', function(){
		location.href = '/Statistics?behalf=' + $(this).find('option:selected').attr('id');
	});
});