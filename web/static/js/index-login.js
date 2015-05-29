/**
 * Created by Yuri on 5/20/2015.
 */

$(function() {  //this is jQuery's short notation for "fire all this when page is ready"
    $('#login').on('click', submitLogin);
    $('#register').on('click', submitRegister);
});

function submitLogin() {
    var email = $('#login_email').val();
    var password = $('#login_password').val();
    $.ajax({
		url:'/loginAtt',
		type:'GET',
		dataType:'json',
        data:{email:email, password:password},
		success:function(data, status, xhr) {
            location.reload();
		},
		error:function(xhr, status, error) {
            alert(xhr.responseText);
			console.error(xhr, status, error);
		}
	});
}

function submitRegister() {
    var email = $('#reg_email').val();
    var password = $('#reg_password').val();
	var isAdmin = 0;
	if($('#isAdmin').is(':checked')){
            isAdmin = 1;
          }
    $.ajax({
		url:'/registerAtt',
		type:'GET',
		dataType:'json',
        data:{email:email, password:password, isAdmin:isAdmin},
		success:function(data, status, xhr) {
        document.location.href = '/';
			
		},
		error:function(xhr, status, error) {
            alert(xhr.responseText);
			console.error(xhr, status, error);
		}
	});
}