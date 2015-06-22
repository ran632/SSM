
$(function() {  //this is jQuery's short notation for "fire all this when page is ready"
    $('#submit').on('click', submitSchedule);
	$('#date').on('change', dateChanged);
});

function submitSchedule() {
	var schedule = new Array();
	for(var dayCount = 1 ; dayCount < 8 ; dayCount++){
		for(var hourCount = 0 ; hourCount < 3 ; hourCount++){
			for(var roleCount = 1 ; roleCount < 4 ; roleCount++) {
				var empno = document.getElementById("sel" + dayCount + hourCount + roleCount).value;
                var i = dayCount;
                var j = hourCount;
                var k = roleCount;
				schedule.push({"empno": empno, "day": i, "hour": j, "role": k});
                //schedule.push({"day": i});
                //schedule.push({"hour": j});
                //schedule.push({"role": k});
			}
		}
	}
	$.ajax({
		url:'/Admin/schedulizeAtt',
		type:'POST',
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
