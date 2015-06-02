/**
 * Created by Yuri on 5/20/2015.
 */

$(function() {  //this is jQuery's short notation for "fire all this when page is ready"
    $('#submit').on('click', submitShift);

});

function submitShift() {
	for(i = 1 ; i < 8 ; i++){
		for(j = 0 ; j < 3 ; j++){
			var shiftHour = j;
			var weekDay = i;
			if($('#'+i+j).is(':checked')){
				$.ajax({
					url:'/submissionAtt',
					type:'GET',
					dataType:'json',
					data:{shiftHour:shiftHour, weekDay:weekDay},
					success:function(data, status, xhr) {
						location.reload();
					},
					error:function(xhr, status, error) {
						alert(xhr.responseText);
						console.error(xhr, status, error);
					}
				});
			}
		}
	}
	var notes = $('textarea#notes').val();
	$.ajax({
		url:'/submissionNoteAtt',
		type:'GET',
		dataType:'json',
		data:{notes:notes},
		success:function(data, status, xhr) {
			location.reload();
		},
		error:function(xhr, status, error) {
			alert(xhr.responseText);
			console.error(xhr, status, error);
		}
	});


}
