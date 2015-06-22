$(function() {  //this is jQuery's short notation for "fire all this when page is ready"
	$('#emplist').on('change', function () {
		location.href = '/SwitchShifts?ce=' + $(this).find('option:selected').attr('id') + '&cms=' + $('#myshifts').find('option:selected').attr('id');
	});
	$('#submit').on('click', submitSwitch);
	$('.btn').on('click', function(){
		var actNum = $(this).attr('value');
		var actName;
		if (actNum == 1)
			actName = 'Approved'
		if (actNum == 0)
			actName = 'Declined'
		if (actNum == 2)
			actName = 'Remove'
			$.ajax({
				url:'/SwitchShifts/switch' + actName,
				type:'GET',
				dataType:'json',
				data: {req_id:$(this).attr('name')},
				success:function(data, status, xhr) {
					location.reload();
				},
				error:function(xhr, status, error) {
					alert(xhr.responseText);
					console.error(xhr, status, error);
				}
			});
	});
});

function submitSwitch(){
	var from_shift_id = $('#myshifts').find('option:selected').attr('id');
	var to_empno = $('#emplist').find('option:selected').attr('id');
	var to_shift_id = $('#othershifts').find('option:selected').attr('id');

	if(to_empno.isEmpty) {
		alert("Please choose employee to switch with");
		return
	}
	if(from_shift_id.isEmpty && to_shift_id.isEmpty) {
		alert("No shift selected");
		return
	}
	$.ajax({
		url:'/SwitchShifts/switchAtt',
		type:'GET',
		dataType:'json',
		data: {from_shift_id:from_shift_id, to_empno:to_empno, to_shift_id:to_shift_id},
		success:function(data, status, xhr) {
			location.reload();
		},
		error:function(xhr, status, error) {
			alert(xhr.responseText);
			console.error(xhr, status, error);
		}
	});
}