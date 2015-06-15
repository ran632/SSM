
$(function() {  //this is jQuery's short notation for "fire all this when page is ready"
    $('#submit').on('click', submitSchedule);
	$('#date').on('change', dateChanged);
});

function submitSchedule() {
	var schedule = new Array();
	for(dayCount = 1 ; dayCount < 8 ; dayCount++){
		for(hourCount = 0 ; hourCount < 3 ; hourCount++){
			for(roleCount = 1 ; roleCount < 4 ; roleCount++) {
				var empno = document.getElementById("sel" + dayCount + hourCount + roleCount).value;
				schedule.push({"empno": empno, "day": dayCount, "hour": hourCount, "role": roleCount})
			}
		}
	}
	$.ajax({
		url:'/Admin/schedulizeAtt',
		type:'GET',
		dataType:'json',
		data: {schedule:JSON.stringify(schedule)},
		success:function(data, status, xhr) {
			location.reload();
		},
		error:function(xhr, status, error) {
			alert(xhr.responseText);
			console.error(xhr, status, error);
		}
	});

}

function dateChanged(){
	$.ajax({
		url:'/Admin/schedulizeAtt',
		type:'GET',
		dataType:'json',
		data: {datepick:document.getElementById('date').value},
		success:function(data, status, xhr) {
			location.reload();
		},
		error:function(xhr, status, error) {
			alert(xhr.responseText);
			console.error(xhr, status, error);
		}
	});
}
