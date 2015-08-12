$(function() {  //this is jQuery's short notation for "fire all this when page is ready"
	$('#cal').on('change', function () {
		location.href = '/History?date=' + $('#cal').val();
	});
	$('#prnt').on('click', function () {
		$('body > :not(.printversion)').hide(); //hide all nodes directly under the body
		$('.printversion').appendTo('body');

		$('.success').removeClass( 'success' );
		$('.info').removeClass( 'info' );
		$('.warning').removeClass( 'warning' );
		$('.danger').removeClass( 'danger' );
	});
});