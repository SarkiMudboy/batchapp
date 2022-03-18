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
}