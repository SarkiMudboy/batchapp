{   


    $("#material-create-button").on("click", function(e){
        console.log("this was clicked")
        $.ajax({
        method:"GET",
        dataType: "html",
        url: $('#material-create-button').attr("href"),
        success: function (data) {
            console.log("success")
            $(".pack-material-form").html(data)
        }
    })
    })

    $('#create-bill-button').on('click', function(event){
        event.preventDefault();
        $.ajax({
            method:"GET",
            dataType: "html",
            url: $('#create-bill-button').attr("href"),
            success: function (data) {
                $(".bill-form").html(data)
            }
        })
    })

    $("body").on("click", ".packaging-list", function(e){
        console.log('clicked!')
        e.preventDefault()
        var btn = $(this)
        $.ajax({
            url: btn.attr("data-form-url"),
            type: 'GET',
            dataType: 'json',
            success: function (data) {
              $("#modal-packaging-bill").modal("show");
              $("#modal-packaging-bill .modal-content").html(data.form);  
            }
        })
    })

    
    $("#modal-packaging-bill").on("submit", ".update-bill-js", function(e){
        e.preventDefault();
        var form = $(this)
        $.ajax({
            url: form.attr("action"),
            type:"POST",
            data: form.serialize(),
            dataType: "json",
            success: function (data) {
                if (data.form_is_valid){
                    $('body').html(data.bill_template);
                }
                else{
                    console.log('error')
                };
            }
        })
    })

    $('#create-process-button').on('click', function(event){
        event.preventDefault();
        $.ajax({
            method:"GET",
            dataType: "html",
            url: $('#create-process-button').attr("href"),
            success: function (data) {
                $(".package-process-form").html(data)
            }
        })
    })


    $("body").on("click", ".pack-processes", function(e){
        console.log('clicked!')
        e.preventDefault()
        var btn = $(this)
        $.ajax({
            url: btn.attr("data-form-url"),
            type: 'GET',
            dataType: 'json',
            success: function (data) {
              $("#modal-packaging-process").modal("show");
              $("#modal-packaging-process .modal-content").html(data.form);  
            }
        })
    })

    $("#modal-packaging-process").on("submit", ".update-process-js", function(e){
        e.preventDefault();
        var form = $(this)
        $.ajax({
            url: form.attr("action"),
            type:"POST",
            data: form.serialize(),
            dataType: "json",
            success: function (data) {
                if (data.form_is_valid){
                    console.log("done")
                    $('body').html(data.process_template);
                }
                else{
                    console.log('error')
                };
            }
        })
    })

    $("#auth-form").on("submit", function (e) {
        e.preventDefault();
        var form = $(this)
        $.ajax({
            url: form.attr('target'),
            type:"POST",
            data: form.serialize(),
            dataType: "json",
            success: function(data){
                $("#messages").append(`<div class='text-center alert alert-success'>${data.message}</div>`);
            }
        })
    })

}