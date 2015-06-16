
$(function() {  //this is jQuery's short notation for "fire all this when page is ready"
    $('#submit').on('click', submitSchedule);
});

function submitSchedule() {
	var schedule = new Array();
	for(dayCount = 1 ; dayCount < 8 ; dayCount++){
		for(hourCount = 0 ; hourCount < 3 ; hourCount++){
			var hfa = 4;
			if(hourCount == 0)
				hfa = 5;
			for(roleCount = 1 ; roleCount < hfa ; roleCount++) {
				var empno = document.getElementById("sel" + dayCount + hourCount + roleCount).value;
				schedule.push({"empno": empno, "day": dayCount, "hour": hourCount, "role": roleCount})
			}
		}
	}
	alert("lalalala");
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

function changeDate() {
    alert(document.getElementById("cal").value);
    $.ajax({
        url: '/Admin',
        type: 'GET',
        dataType: 'html',
        data: {date:document.getElementById("cal").value},
        success: function (data, status, xhr) {
            location.reload();
        },
        error: function (xhr, status, error) {
            alert(xhr.responseText);
            console.error(xhr, status, error);
        }
    });
}

