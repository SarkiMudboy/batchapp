
$( function() {
  function split(val){
    return val.split(" ");
  }
  function extractLast (term){
    return split(term).pop();
  }
    $( "#complete-id" ).autocomplete({
      source: function( request, response ) {
        var search = extractLast($('#complete-id').val())
        $.ajax( {
          url: $('#process-form').attr('data-ajax-target'),
          type: 'GET',
          dataType: "jsonp",
          data: {
            'search': search
          },
          success: function( data ) {
            response( data );
          }
        } );
      },
      search: function () {
        var term = extractLast(this.value);
        if (term.Length < 2) {
          return false;
        }
      },
      select: function (event, ui) {
        var input = split(this.value);
        input.pop();
        input.push(ui.item.value);
        input.push("")
        this.value = input.join(" ");
        console.log(this.value)
        return false;
      }, 

    } )
    .bind('keydown', function(event){
        if (event.keyCode === $.ui.keyCode.TAB && $(this).data("ui-autocomplete").menu.active){
            console.log('Hey')
            event.preventDefault();
        }
    })
    .data("autocomplete")._renderItem = function (ul, item) {
    return $("<li>")
        .data("item.autocomplete", item)
        .append("<a>" + item.label + "</a>")
        .appendTo(ul);
    };
  } );