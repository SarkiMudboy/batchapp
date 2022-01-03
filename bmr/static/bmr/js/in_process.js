{
    $('#process-form').submit(function(e) {
        // preventing from page reload and default actions
        e.preventDefault();
        // serialize the data for sending the form data.
        var serializedData = $(this).serialize();
        // make ajax POST call
        $.ajax({
            type: 'POST',
            url: $("#ajax-control-button").attr("data-ajax-target"),
            data: serializedData,
            success: function (response) {
                    // on successfull creating object
                    // 1. clear the form.
                    $("#process-form").trigger('reset');
                    // 2. focus on the form
                    $("#process-form").focus();

                    // display the newly added form to the list page
                    var instance = JSON.parse(response['instance']);
                    var fields = instance[0]["fields"];
                    
                    var resp_data = response['data']
                    console.log(resp_data.record);

                    $("#messages").append(`<div class='text-center alert alert-${resp_data.messages.type}'>${resp_data.messages.message}</div>`);

                    $('#control-list').append(`
                    <tr class="rec-list" 
                    data-form-url="">
                      <th scope="row">1</th>
                      <td>${fields['created'].split('T')[0]}</td>
                      <td>${resp_data.test.test_name}</td>
                      <td>${resp_data.test.specification}</td>
                      <td>${fields['result']}</td>
                      <td>${fields['remarks']}</td>
                    </tr>
                    `)

                    $('#control-list tr').last().attr('data-form-url', 
                        `/batches/${resp_data.batch_data.product_pk}/${resp_data.batch_data.batch_pk}/process-control/${resp_data.batch_data.record_pk}/update`)

            },
            error: function (response) {
                // alert the error if any error occured
                error_message = response.responseJSON.errors;
                error_message.forEach(addError)
                function addError (err) {
                $("#messages").append(`<div class='text-center alert alert-danger'>${err}</div>`);
                };
                $("#eq-form").trigger('reset');
            }
        })
    })

    $(".rec-list").on('click', function(e) {
        console.log("clicked")
        e.preventDefault();
        var btn = $(this)
        $.ajax({
            url: btn.attr("data-form-url"),
            type: 'get',
            dataType: 'json',
            success: function (data) {
              $("#modal-controls").modal("show");
              $("#modal-controls .modal-content").html(data.form);  
            }
        })
    })

    $("#modal-controls").on("submit", ".update-control-js", function(e){
        e.preventDefault();
        var form = $(this)
        $.ajax({
            url: form.attr("action"),
            type:"POST",
            data: form.serialize(),
            dataType: "json",
            success: function (data) {
                if (data.form_is_valid){
                    $('#control-list').html(data.html_control_list);
                };
            }
        })
    })
}