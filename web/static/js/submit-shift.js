/**
 * Created by Yuri on 5/20/2015.
 */
var caldate;
var behalf;

$(function() {  //this is jQuery's short notation for "fire all this when page is ready"
    $('#submit').on('click', submitShift);
	$('#emplist').on('change', modArgs);
	$('#cal').on('change', modArgs);
});

function modArgs(){
	behalf = $('#emplist').find('option:selected').attr('id');
	caldate = $('#cal').val();
	location.href = '/SubmissionShifts?behalf=' + behalf + "&date=" + caldate;
}

function submitShift() {
	var behalf = $('#emplist').find('option:selected').attr('id');
	var shifts = []
	var notes = $('textarea#notes').val();
	var numofshifts = $('#numofshifts').val();
	for(i = 1 ; i < 8 ; i++){
		for(j = 0 ; j < 3 ; j++){
			var shiftHour = j;
			var weekDay = i;
			if($('#'+i+j).is(':checked')){
				shifts.push({"shiftHour": shiftHour, "weekDay": weekDay})
			}
		}
	}
	$.ajax({
		url:'/submissionAtt',
		type:'GET',
		dataType:'json',
		data:{shifts:JSON.stringify(shifts), notes:notes, numofshifts:numofshifts, behalf:behalf},
		success:function(data, status, xhr) {
			location.reload();
		},
		error:function(xhr, status, error) {
			alert(xhr.responseText);
			console.error(xhr, status, error);
		}
	});
}
