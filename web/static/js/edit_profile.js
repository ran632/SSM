
/**
 * Created by Elad on 6/4/2015.
 */

$(function() {  //this is jQuery's short notation for "fire all this when page is ready"
    $('#edit').on('click', editProfile);
    $('#save').on('click', saveProfile);
});

function editProfile() {

    var editable_elements = document.querySelectorAll("[contenteditable=false]");
    for(var i=0; i<editable_elements.length; i++) {
        editable_elements[i].setAttribute("contenteditable", true);
    }
    alert('Edit Available (Not Include Email)');
}

function saveProfile() {

    var arr = [];

    //gets table
    var oTable = document.getElementById('myTable');

    //gets rows of table
    var rowLength = oTable.rows.length;

    for (var i=0;i<rowLength;i++) {
        arr[i] = Array();
    }

    //loops through rows
    for (var i = 1; i < rowLength; i++) {

        //gets cells of current row
        var oCells = oTable.rows.item(i).cells;

        //gets amount of cells of current row
        var cellLength = oCells.length;

        //loops through each cell in current row
        for (var j = 1; j < cellLength; j++) {

            // get your cell info here
            var cellVal = oCells.item(j).innerHTML;
            arr[i][j] = cellVal;
        }
    }

    $.ajax({
        url:'/UserProfileAtt',
        type:'POST',
        dataType:'json',
        data:{editArr:JSON.stringify(arr), rowLength:rowLength},
        success:function(data, status, xhr) {
            document.location.href = '/Admin';
        },
        error:function(xhr, status, error) {
            alert(xhr.responseText);
            console.error(xhr, status, error);
        }
    });

}