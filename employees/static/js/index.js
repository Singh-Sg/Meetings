$(document).ready(function () {
    var date = new Date().toISOString().split('T')[0]
    $("#meeting-date").prop('min', date)
    $.ajax({
        url: "index_api/",
        type: 'GET',
        error: function (data) {
        },
        complete: function (data) {
            slot_text = ''
            emp_select = `<option disabled selected value> -- select an employee -- </option>`
            count = 0
            data.responseJSON.results.forEach((emp) => {
                count += 1
                slot_text = slot_text + 
                `
                    <tr>
                        <th scope="row"> ${count}</th>
                        <td>${emp.employeecode}</td>
                        <td>${emp.firstname}</td>
                        <td>${emp.lastname}</td>
                        <td>${emp.designation_name}</td>
                        <td>${emp.department_name}</td>
                        <td>
                            <button type="submit" class="btn btn-primary" id="book_slot" onclick="myfunction2.call(this)"
                                data-employeecode="${emp.employeecode}" data-firstname="${emp.firstname}"
                                data-lastname="${emp.lastname}"
                                data-target="#book-meeting-modal"
                                data-toggle="modal">Book
                                a meeting
                            </button>
                    </tr>
                 `
                emp_select += `
                        <option value=${emp.employeecode}> 
                            ${emp.employeecode}
                            ${emp.firstname}
                            ${emp.lastname}
                        </option>
                        `
            });
            $("#emp_body_list").html(slot_text);
            $("#emp_select").html(emp_select);
        },
    });
});


function myfunction2() {
    id = this.dataset.employeecode
    $('#selected-employee').val(this.dataset.firstname + ' ' + this.dataset.lastname)
    $('#book-meeting select').val("");
    $("#book-meeting input[id='book-message']").val("");
    $("#book-meeting input[name='emp_id_1']").val(id)
    let id2
    $("#emp_select option").each(function () {
        $(this).show();
        if (this.value == id) {
            $(this).hide();
        } else if (id2 == undefined) {
            id2 = this.value
        }
    });
}

function myfunction3() {
    id2 = $("#emp_select")[0].value;
    $("#slot_select").prop('required', false);
    if ($("#book-meeting")[0].checkValidity()) {
        $.ajax(
            {
                type: "GET",
                url: "tasks",
                data: $('#book-meeting').serialize(),

                success: function (data) {
                    console.log("working")
                    slot_text = '<option disabled selected value>  --Available  Slots--</option>'
                    data.available_slot.forEach((element) => {
                        slot_text = slot_text + '<option>' + element + '</option>'
                    });
                    $("#slot_select").html(slot_text)
                    $('#message').text(data);
                },
                error: function (data) {
                    alert(data.responseJSON.message)
                }
            })
    }
    else {
        $("#book-meeting")[0].reportValidity()
    }
}
