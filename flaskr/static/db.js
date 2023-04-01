var parsed_item;
var parsed_client;
var paymentType = "";
var totalCheck = 0;
var credit = 0;
var money = 0;
var limit = 0;

$.get("/js_db_data/Item", function(data) {
    parsed_item = $.parseJSON(data);
})

$.get("/js_db_data/Client", function(data) {
    parsed_client = $.parseJSON(data);
})

$(function () {

    var counter = 1;
    

    function createTemplate(data, id) {
        var tmp = `<td><select id='select${id}' class="form-select">`;
        for (key in data) {
            var name = data[key]['name'];
            tmp += `<option>${name}</option>`;
        }
        tmp += '</select></td>';
        return tmp;
    }

    // Start counting from the third row
    

    $("#insertRow").on("click", function (event) {
        event.preventDefault();

        var newRow = $("<tr>");
        var cols = '';

        // Table columns
        cols += '<th scope="row">' + counter + '</th>';
        cols += createTemplate(parsed_item, counter);
        cols += `<td><input onkeyup=inputCheckStock('${counter}') id=input${counter} class="form-control rounded-0" type="text"></td>`;
        cols += '<td><button class="btn btn-danger rounded-0" id ="deleteRow">🗑️</button</td>';

        // Insert the columns inside a row
        newRow.append(cols);

        // Insert the row inside a table
        $("#modalTable").append(newRow);

        // Increase counter after each row insertion
        counter++;
    });

    // Remove row when delete btn is clicked
    $("table").on("click", "#deleteRow", function (event) {
        $(this).closest("tr").remove();
        counter -= 1
    });

    function myAlertTop() {
        $(".myAlert-top").show();
        setTimeout(function(){
          $(".myAlert-top").hide(); 
        }, 2000);
    }
});