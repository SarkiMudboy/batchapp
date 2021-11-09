$(function () {

    /* Functions */
  
    var loadForm = function () {
      var btn = $(this);
      $.ajax({
        url: btn.attr("data-form-url"),
        type: 'get',
        dataType: 'json',
        success: function (data) {
          $("#modal-tests").modal("show");
          if (data.delete) {
            $("#modal-tests .modal-content").html(data.html_delete);
          } else{
            $("#modal-tests .modal-content").html(data.html_form);
          }  
        }
      });
    };

    var saveForm = function () {
        var form = $(this);
        console.log(form)
        $.ajax({
          url: form.attr("action"),
          data: form.serialize(),
          type: 'POST',
          dataType: 'json',
          success: function (data) {
            if (data.form_is_valid) {
              $("#tests tbody").html(data.html_test_list);
              var message = data['messages'][0]
              if (!data.delete) {
                $("#test-messages").append(`<div class='text-center alert alert-${message.extra_tags}'>${message.message}</div>`);
              }
              else{
                $("#modal-tests").modal("hide")
                $("#test-delete-messages").append(`<div class='text-center alert alert-danger'>${message.message}</div>`)
              }
            }
            else if (data.created) {
              var message = data['messages'][0]
              $("#test-create-form").trigger("reset");
              $("#test-delete-messages").append(`<div class='text-center alert alert-${message.extra_tags}'>${message.message}</div>`);
              $("#tests tbody").html(data.html_test_list);
            }
            else {
              $("#modal-tests .modal-content").html(data.html_form);
            };
          }
        });
        return false;
      };

  // Create tests
  $("#test-create-form").on("submit", saveForm);

  // Update test
  $("#tests").on("click", ".test-rename", loadForm);
  $("#modal-tests").on("submit", ".js-test-update-form", saveForm);

  // Delete test
  $("#tests").on("click", ".test-delete", loadForm);
  $('#modal-tests').on("submit", ".test-delete-html", saveForm);
});

