var empnoArr = [];
$(function() {  //this is jQuery's short notation for "fire all this when page is ready"
    $('#submit').on('click', submitSchedule);
	$('#cal').on('change', function(){
		location.href = '/Admin?date='+$('#cal').val();
	});
	$('.shiftselect').on('change', updateAll);

	$('.empno').each(function(){
		empnoArr.push($(this).text());
	});
	updateAll();
});

function updateAll(){
	$.each(empnoArr, function(index, value){
		updateNum(value);
	})
}

function updateNum(empno){
		numberOfSelected = $("select:has(option[value='" + empno + "']:selected)").length;
		document.getElementById("count" + empno).innerHTML = numberOfSelected;
	}

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
