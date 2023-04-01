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
  var total = 0;
  var i = 0;
  while (true) {
    i++;
    if ($(`#select${i}`).val() === undefined) {
      break;
    }
    var value = parseInt($(`#input${i}`).val());
    var name = $(`#select${i}`).val();
    paymentType =  $("#paymentSelect").val();

    if (isNaN(value)) {
      value = 0;
    }
    for (key in parsed_item) {
      if (parsed_item[key]['name'] != name ) {
        continue;
      }

      total += value * parsed_item[key]["cost"];

      if (parseInt(parsed_item[key]['stock']) < value) {
        $('.alert').show();
        document.getElementById("alertDescription").innerHTML = `The quantity of the ${name} item in stock is ${parsed_item[key]['stock']}, but you tried to enter ${value}`;
      }
      else if (parseInt(parsed_item[key]['stock']) >= value) {
        $('.alert').hide();
      }

      break;
    }
  }

  totalCheck = total;
  document.getElementById("total").innerHTML = `Total: ${totalCheck}`

  if (paymentType === "Cash") {
    return;
  }
  else if (paymentType === "Online") {
    if (totalCheck > money) {
      $("#amoney").css("color", "red")
      $("#total").css("color", "red")
    }
    else if (totalCheck > money / 2) {
      $("#amoney").css("color", "orange")
      $("#total").css("color", "orange")
    }
    else if (totalCheck <= money) {
      $("#amoney").css("color", "#0d6efd")
      $("#total").css("color", "#0d6efd")
    }
  }
  else if (paymentType === "Credit") {
    if (totalCheck > (limit - credit)) {
      $("#acredit").css("color", "red")
      $("#alimit").css("color", "red")
      $("#total").css("color", "red")
    }
    else if (totalCheck > (limit - credit) / 2) {
      $("#acredit").css("color", "orange")
      $("#alimit").css("color", "orange")
      $("#total").css("color", "orange")
    }
    else if (totalCheck <= (limit - credit)) {
      $("#acredit").css("color", "#0d6efd")
      $("#alimit").css("color", "#0d6efd")
      $("#total").css("color", "#0d6efd")
    }
  }

}


function onOrderSave() {
  var clientName = $("#nameSelect").val();
  paymentType = $("#paymentSelect").val();
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
      money = parseInt(parsed_client[key]["money"]);
      credit = parseInt(parsed_client[key]["credit"]);
      limit = parseInt(parsed_client[key]["limit"]);
      document.getElementById("amoney").innerHTML = `Money ${money}`;
      document.getElementById("alimit").innerHTML = `Limit ${limit}`;
      document.getElementById("acredit").innerHTML = `Credit ${credit}`;
      break;
    }
  }
  $("#amoney").css("color", "#0d6efd")
  $("#acredit").css("color", "#0d6efd")
  $("#alimit").css("color", "#0d6efd")
  $("#total").css("color", "#0d6efd")
  inputCheckStock(0);
}


function update() {
  var name = $("#nameSelect").val();
  for (key in parsed_client) {
    if (parsed_client[key]["name"] === name) {
      money = parseInt(parsed_client[key]["money"]);
      credit = parseInt(parsed_client[key]["credit"]);
      limit = parseInt(parsed_client[key]["limit"]);
      document.getElementById("amoney").innerHTML = `Money ${money}`;
      document.getElementById("alimit").innerHTML = `Limit ${limit}`;
      document.getElementById("acredit").innerHTML = `Credit ${credit}`;
      break;
    }
  }
  paymentType = $("#paymentSelect").val();
}


function changePayement() {
  $("#amoney").css("color", "#0d6efd")
  $("#acredit").css("color", "#0d6efd")
  $("#alimit").css("color", "#0d6efd")
  $("#total").css("color", "#0d6efd")
  inputCheckStock(0);
}