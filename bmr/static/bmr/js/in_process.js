{   


    function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
            }
        }
        return cookieValue;
    }
    const csrftoken = getCookie('csrftoken');


    $('#process-form').submit(function(e) {
        // preventing from page reload and default actions
        e.preventDefault();
        // serialize the data for sending the form data.
        var serializedData = $(this).serialize();
        // make ajax POST call
        console.log(serializedData)
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

                    let dataUrl = `/batches/${resp_data.batch_data.product_pk}/${resp_data.batch_data.batch_pk}/process-control/${resp_data.batch_data.record_pk}/update`
                    counter = document.getElementsByClassName("counter")
                    let serial = counter[counter.length-1].innerHTML

                    $("#control-list").append(`
                    <tr class="rec-list" data-form-url="${dataUrl}">
                      <th scope="row" class="counter">${(parseInt(serial) + 1).toString()}</th>
                      <td>${fields['created'].split('T')[0]}</td>
                      <td>${resp_data.test.test_name}</td>
                      <td>${resp_data.test.specification}</td>
                      <td>${fields['result']}</td>
                      <td>${fields['remarks']}</td>
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

    $("body").on('click', ".rec-list", function(e) {
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
                    $('body').html(data.html_control_list);
                }
                else{
                    console.log('error')
                };
            }
        })
    })

    $("#weight-form").on("submit", function(e){
        e.preventDefault()
        var form = $(this)
        $.ajax({
            url: form.attr("action"),
            type: "POST",
            data: form.serialize(),
            dataType: "json",
            success: function(data) {
                console.log(data);
            }
        })
    })

    $('#cleaning-form').submit(function(e) {
        e.preventDefault();
        var serializedData = $(this).serialize();
        $.ajax({
            type: 'POST',
            url: $("#ajax-clean-button").attr("data-ajax-target"),
            data: serializedData,
            success: function (response) {
                    console.log(response)
                    $("#process-form").trigger('reset');
                    $("#process-form").focus();

                    var instance = JSON.parse(response['instance']);
                    var fields = instance[0]["fields"];
                    var ins = JSON.parse(response["batch_data"]["i"])

                    // $("#messages").append(`<div class='text-center alert alert-${resp_data.messages.type}'>${resp_data.messages.message}</div>`);

                    let dataUrl = `/batches/${response.batch_data.product_pk}/${response.batch_data.batch_pk}/cleaning-process/${response.batch_data.clean_pk}/update`
                    counter = document.getElementsByClassName("counter-clean")
                    let serial = counter[counter.length-1].innerHTML

                    $("#clean-list").append(`
                    <tr class="rec-list" data-form-url="${dataUrl}">
                      <th scope="row" class="counter">${(parseInt(serial) + 1).toString()}</th>
                      <td>${fields['process_description']}</td>
                      <td>${ins['action_by']}</td>
                      <td>${ins["checked_by"]}</td>
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
                $("#cleaning-form").trigger('reset');
            }
        })
    })

    $("body").on('click', ".cln-list", function(e) {
        e.preventDefault();
        var btn = $(this)
        $.ajax({
            url: btn.attr("data-form-url"),
            type: 'get',
            dataType: 'json',
            success: function (data) {
              $("#modal-clean").modal("show");
              $("#modal-clean .modal-content").html(data.form);  
            }
        })
    })

    $("#modal-clean").on("submit", "update-cleaning-js", function(e){
        e.preventDefault();
        var form = $(this)
        $.ajax({
            url: form.attr("action"),
            type:"POST",
            data: form.serialize(),
            dataType: "json",
            success: function (data) {
                if (data.form_is_valid){
                    $('body').html(data.html_cleaning_list);
                }
                else{
                    console.log('error')
                };
            }
        })
    })

}