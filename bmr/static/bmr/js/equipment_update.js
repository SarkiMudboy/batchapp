$(function () {

    /* Functions */
  
    var loadForm = function () {
      var btn = $(this);
      $.ajax({
        url: btn.attr("data-form-url"),
        type: 'get',
        dataType: 'json',
        success: function (data) {
          $("#modal-equipments").modal("show");
          if (data.delete) {
            $("#modal-equipments .modal-content").html(data.html_delete);
          } else {
            $("#modal-equipments .modal-content").html(data.html_form);
          }  
        }
      });
    };

    var saveForm = function () {
        var form = $(this);
        $.ajax({
          url: form.attr("action"),
          data: form.serialize(),
          type: 'POST',
          dataType: 'json',
          success: function (data) {
            if (data.form_is_valid) {
              $("#equipments").html(data.html_equipment_list);
              var message = data['messages'][0]
              if (!data.delete) {
                $("#eq-messages").append(`<div class='text-center alert alert-${message.extra_tags}'>${message.message}</div>`);
              }
              else{
                $("#modal-equipments").modal("hide")
                $("#eq-delete-messages").append(`<div class='text-center alert alert-danger'>${message.message}</div>`)
              }
            }
            else {
              $("#modal-equipments .modal-content").html(data.html_form);
            };
          }
        });
        return false;
      };

  // Update equipment
  $("#equipments").on("click", ".js-update-equipment", loadForm);
  $("#modal-equipments").on("submit", ".js-equipment-update-form", saveForm);

  // Delete equipment
  $("#equipments").on("click", ".js-delete-equipment", loadForm);
  $('#modal-equipments').on("submit", ".js-delete-html", saveForm);

});