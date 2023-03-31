function search() {
  // Declare variables
  var input, filter, table, tr, th, i, txtValue;
  input = document.getElementById("search");
  filter = input.value.toUpperCase();
  table = document.getElementById("table");
  tr = table.getElementsByTagName("tr");
  console.log(tr);

  for (i = 0; i < tr.length; i++) {
    th = tr[i].getElementsByTagName("th");

    if (!th) { 
      break; 
    }

    if (th.scope == "col") { 
      continue; 
    }

    console.log(th)

    flag = false;

    for (k = 0; k < th.length; k++) {
      txtValue = th[k].textContent || th[k].innerText;
      if (th[k].scope == "col") {
        flag = true;
        break;
      }
      if (txtValue.toUpperCase().indexOf(filter) > -1) {
        flag = true;
      }
    }
    if (flag) {
      tr[i].style.display = "";
    } 
    else {
      tr[i].style.display = "none";
    }
  }
}

function inputCheckStock(id) {
  var value = parseInt($(`#input${id}`).val());
  var name = $(`#select${id}`).val();
  var total = 0;

  if (!value) {
    return;
  }
  for (key in parsed_item) {
    if (parsed_item[key]['name'] != name ) {
      continue;
    }

    total += value * parsed_item[key]["cost"];
    document.getElementById("total").innerHTML = `Total: ${total}`

    if (parseInt(parsed_item[key]['stock']) < value) {
      $('.alert').show();
      document.getElementById("alertDescription").innerHTML = `The quantity of the ${name} item in stock is ${parsed_item[key]['stock']}, but you tried to enter ${value}`;
    }
    else if (parseInt(parsed_item[key]['stock']) >= value) {
      $('.alert').hide();
    }
  }
}


function onOrderSave() {
  var clientName = $("#nameSelect").val();
  var paymentType = $("#paymentSelect").val();
  var items = [];
  var i = 0;
  while (true) {
    i++;
    if ($(`#select${i}`).val() === undefined) {
      break;
    }

    var itemName = $(`#select${i}`).val();
    var amount = $(`#input${i}`).val();

    if (amount === "") {
      $('.alert').show();
      document.getElementById("alertDescription").innerHTML = "Something went wrong";
      return;
    }

    items.push({"name": itemName, "amount": amount})
  }

  if (items.length === 0) {
    $('.alert').show();
    document.getElementById("alertDescription").innerHTML = "Something went wrong!";
    return;
  }
  else {
    $('#exampleModal').modal('hide');

    var data = JSON.stringify({"client": clientName, "payment": paymentType, "items":items});

    $.post( "/js_create_order", {
      javascript_data: data 
    });
  }
}


function changedClient() {
  var name = $("#nameSelect").val();
  for (key in parsed_client) {
    if (parsed_client[key]["name"] === name) {
      document.getElementById("amoney").innerHTML = `Money ${parsed_client[key]["money"]}`
      document.getElementById("alimit").innerHTML = `Limit ${parsed_client[key]["limit"]}`
      document.getElementById("acredit").innerHTML = `Credit ${parsed_client[key]["credit"]}`
    }
  }
}