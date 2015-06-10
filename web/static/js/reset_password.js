/**
 * Created by Elad on 6/10/2015.
 */

$(function() {  //this is jQuery's short notation for "fire all this when page is ready"
    $('#reset').on('click', resetPass);
});

function resetPass() {
    var email = $('#repeat_email').val();
    var password = $('#reset_password').val();
    $.ajax({
		url:'/ResetPasswordAtt',
		type:'GET',
		dataType:'json',
        data:{email:email, password:password},
		success:function(data, status, xhr) {
            document.location.href = '/Login';
		},
		error:function(xhr, status, error) {
            alert(xhr.responseText);
			console.error(xhr, status, error);
		}
	});
}