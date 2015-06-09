/**
 * Created by Elad on 6/8/2015.
 */


$(function() {  //this is jQuery's short notation for "fire all this when page is ready"
    $('#delete').on('click', deleteProfile);
});

function deleteProfile() {

    var oTable = document.getElementById('deleteTable');
    var oCells = null;
    var email = null;
    var non_email = null;
    var checkedValue = null;
    var inputElements = document.getElementsByName("active");
    var non_activation = [];
    var activation = [];

    for(var i=0;i < inputElements.length; i++){

        oCells = oTable.rows.item(i+1).cells;
        if(!inputElements[i].checked){

            checkedValue = inputElements[i].value;
            non_email = oCells.item(4).innerHTML;

            non_activation.push({"non_email": non_email});

        }
        else {
            email = oCells.item(4).innerHTML;
            activation.push({"email": email});
        }
    }
    $.ajax({
        url:'/DeleteEmployeeAtt',
        type:'GET',
        dataType:'json',
        data:{'activation':JSON.stringify(activation),'non_activation':JSON.stringify(non_activation)},
        success:function(data, status, xhr) {
            document.location.href = '/Admin';
        },
        error:function(xhr, status, error) {
            alert(xhr.responseText);
            console.error(xhr, status, error);
        }
    });
}
