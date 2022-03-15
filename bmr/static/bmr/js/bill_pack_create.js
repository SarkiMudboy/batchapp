{
    $('#packaging-bill-form').submit(function(e) {
        // preventing from page reload and default actions
        e.preventDefault();
        // serialize the data for sending the form data.
        var serializedData = $(this).serialize();
        // make ajax POST call
        $.ajax({
            type: 'POST',
            url: $("#ajax-packaging-button").attr("data-ajax-target"),
            data: serializedData,
            success: function (response) {
                    // on successfull creating object
                    // 1. clear the form.
                    $("#packaging-bill-form").trigger('reset');
                    // 2. focus on the form
                    $("#packaging-bill-form").focus();

                    // display the newly added form to the list page
                    var instance = JSON.parse(response['instance']);
                    
                    var resp_data = response['object_data']

                    let dataUrl = `/batches/${resp_data.product_pk}/${resp_data.batch_pk}/bill-of-packaging/${resp_data.bill_pk}/update`
                    
                    counter = document.getElementsByClassName("counter-bill")
                    
                    if (counter.length > 0) { 
                        var serial = counter[counter.length-1].innerHTML
                    } else {
                        var serial = "0"
                    }

                    $("#bill-list").append(`
                    <tr class="packaging-list" data-form-url="${dataUrl}">
                      <th scope="row" class="counter-bill">${(parseInt(serial) + 1).toString()}</th>
                      <td>${ instance["material"] }</td>
				      <td>${ instance["quantity_required"] }</td>
				      <td>${ instance["actual_quantity"] }</td>
			  	      <td>${ instance["action_by"] }</td>
				      <td>${ instance["checked_by"] }</td>
                    </tr>
                        `);

            },
            error: function (response) {
                // alert the error if any error occured
                error_message = response.responseJSON.errors;
                error_message.forEach(addError)
                function addError (err) {
                $("#messages").append(`<div class='text-center alert alert-danger'>${err}</div>`);
                };
                $("#control-form").trigger('reset');
            }
        })
    })

    $('#pack-process-form').submit(function(e) {
        // preventing from page reload and default actions
        e.preventDefault();
        // serialize the data for sending the form data.
        var serializedData = $(this).serialize();
        // make ajax POST call
        $.ajax({
            type: 'POST',
            url: $("#ajax-process-button").attr("data-ajax-target"),
            data: serializedData,
            success: function (response) {
                    // on successfull creating object
                    // 1. clear the form.
                    $("#pack-process-form").trigger('reset');
                    // 2. focus on the form
                    $("#pack-process-form").focus();

                    // display the newly added form to the list page
                    var instance = JSON.parse(response['instance']);
                    
                    var resp_data = response['object_data']

                    let dataUrl = `/batches/${resp_data.product_pk}/${resp_data.batch_pk}/bill-of-packaging/${resp_data.process_pk}/update`
                    
                    counter = document.getElementsByClassName("counter-process")
                    
                    if (counter.length > 0) { 
                        var serial = counter[counter.length-1].innerHTML
                    } else {
                        var serial = "0"
                    }

                    $("#process-list").append(`
                    <tr class="packaging-list" data-form-url="${dataUrl}">
                      <th scope="row" class="counter-bill">${(parseInt(serial) + 1).toString()}</th>
                      <td>${ instance["process"] }</td>
                      <td>${ instance["action_by"] }</td>
                      <td>${ instance["checked_by"] }</td>
                    </tr>
                        `);

            },
            error: function (response) {
                // alert the error if any error occured
                error_message = response.responseJSON.errors;
                error_message.forEach(addError)
                function addError (err) {
                $("#messages").append(`<div class='text-center alert alert-danger'>${err}</div>`);
                };
                $("#pack-process-form").trigger('reset');
            }
        })
    })
}