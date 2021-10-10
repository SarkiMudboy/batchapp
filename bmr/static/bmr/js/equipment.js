{
    $('#eq-form').submit(function(e) {
        // preventing from page reload and default actions
        e.preventDefault();
        // serialize the data for sending the form data.
        var serializedData = $(this).serialize();
        // make ajax POST call
        $.ajax({
            type: 'POST',
            url: $("#ajax-button").attr("data-ajax-target"),
            data: serializedData,
            success: function (response) {
                    // on successfull creating object
                    // 1. clear the form.
                    $("#eq-form").trigger('reset');
                    // 2. focus on the form
                    $("#eq-form").focus();

                    // display the newly added form to the list page
                    var instance = JSON.parse(response['instance']);
                    var fields = instance[0]["fields"];

                    $('#my-equipments').append(`
                    <li class="list-group-item">
                        <p>${fields['name']}
                            <button type="button" style="float: right;"  class="btn btn-outline-secondary" onclick=location.href='{{ equipment.get_absolute_url }}'>Details</button>
                        </p>
                    </li> 
                    `)
            },
            error: function (response) {
                // alert the error if any error occured
                alert(response["responseJSON"]["error"]);
            }
        })
    })
}