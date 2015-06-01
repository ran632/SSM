/**
 * Created by Yuri on 5/20/2015.
 */

$(function() {  //this is jQuery's short notation for "fire all this when page is ready"
    $('#submit').on('click', submitShift);

});

function submitShift() {
    //var email = $('#login_email').val();
    //var password = $('#login_password').val();
    $.ajax({
		url:'/submissionAtt',
		type:'GET',
		dataType:'json',
        data:{},
		success:function(data, status, xhr) {
            location.reload();
		},
		error:function(xhr, status, error) {
            alert(xhr.responseText);
			console.error(xhr, status, error);
		}
	});
}
