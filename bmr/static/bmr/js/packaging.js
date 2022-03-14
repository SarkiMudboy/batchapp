{   
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
}