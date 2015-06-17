var empnoArr = [];
$(function() {  //this is jQuery's short notation for "fire all this when page is ready"
    $('#submit').on('click', submitSchedule);
	$('#cal').on('change', function(){
		location.href = '/Admin?date='+$('#cal').val();
	});
	$('.shiftselect').on('change', updateAll);
	$('.shiftselect').on('change', function(){
		numOfSelctedSame = $("select:has(option[value='"+this.value+"']:selected)").filter("[name='"+this.name+"']").length
		if(numOfSelctedSame >= 2){
			alert($(this).find("option:selected").text() + " is already selected for this shift!");
			this.selectedIndex = 0;
		}

		numOfSelectedBefore = $("select:has(option[value='"+this.value+"']:selected)").filter("[name='"+shiftNumBefore(this.name)+"']").length
		if(numOfSelectedBefore > 0){
			alert($(this).find("option:selected").text() + " is already selected for " + dayToString(parseInt(parseInt(shiftNumBefore(this.name)/10))) + " " + hourToString(parseInt(parseInt(shiftNumBefore(this.name)%10))));
		}

		numOfSelectedAfter = $("select:has(option[value='"+this.value+"']:selected)").filter("[name='"+shiftNumAfter(this.name)+"']").length
		if(numOfSelectedAfter > 0){
			alert($(this).find("option:selected").text() + " is already selected for " + dayToString(parseInt(parseInt(shiftNumBefore(this.name)/10))) + " " + hourToString(parseInt(parseInt(shiftNumAfter(this.name)%10))));

		}
	});

	$('.empno').each(function(){
		empnoArr.push($(this).text());
	});
	updateAll();

});

function shiftNumBefore(shiftnum){
	num = parseInt(shiftnum);
	day = parseInt(num/10);
	hour = num % 10;
	if(hour == 0) {
		day--;
		hour = 2;
	}
	else{
		hour--;
	}
	return "" + day + hour;
}

function shiftNumAfter(shiftnum){
	num = parseInt(shiftnum);
	day = parseInt(num/10);
	hour = num % 10;
	if(hour == 2) {
		day++;
		hour = 0;
	}
	else{
		hour++;
	}
	return "" + day + hour;
}

function dayToString(day){
	switch(day){
		case 1:
			return "Sunday";
			break;
		case 2:
			return "Monday";
			break;
		case 3:
			return "Tuesday";
			break;
		case 4:
			return "Wednesday";
			break;
		case 5:
			return "Thursday";
			break;
		case 6:
			return "Friday";
			break;
		case 7:
			return "Saturday";
			break;
	}
}

function hourToString(hour){
	switch(hour){
		case 0:
			return "morning";
			break;
		case 1:
			return "evening";
			break;
		case 2:
			return "night";
			break;
	}
}


function updateAll(){
	$.each(empnoArr, function(index, value){
		updateNum(value);
	})
}

function updateNum(empno){
		numberOfSelected = $("select:has(option[value='" + empno + "']:selected)").filter(".thisweek").length;
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
		data: {schedule:JSON.stringify(schedule), date:$("#cal").val()},
		success:function(data, status, xhr) {
			location.reload();
		},
		error:function(xhr, status, error) {
			alert(xhr.responseText);
			console.error(xhr, status, error);
		}
	});
}
