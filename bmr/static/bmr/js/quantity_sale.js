{
	 $("#sale-form").on("submit", function (e) {
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

    $("#auto-qs").on("click", function(e) {
        console.log(e);
        e.preventDefault();
        var btn = $(this)
        $.ajax({
            url: btn.attr("target"),
            type: "GET",
            dataType: "json",
            success: function(data) {
                if (data.message) {
                    $("#messages").append(`<div class='text-center alert alert-danger'>${data.message}</div>`);
                } else {
                    $("#qs-form").html(data.form)
                }
                
            }
        })
    })
}