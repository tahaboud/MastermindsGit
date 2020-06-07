$(document).ready(function() {
  $(".nav").find(".active").removeClass("active");

  $("#reset-form").on('submit', function() {
     $( "#email" ).removeClass('is-invalid');
      if ($("#reset-form")[0].checkValidity() === false) {
        $( "#email-div" ).empty();
        $( "#email-div" ).append( "Please provide a valid email" )
        $("#reset-form")[0].classList.add('was-validated');
        return false;
      }
      else {
        $.ajax({
          url: $("#reset-form").attr("data-url"),
          type: 'POST',
          data: $("#reset-form").serialize(),
          })

        .done(function() {
          $("#reset-form").unbind('submit').submit();
          })

        .fail(function(data) {
          if (data.responseJSON) {
            Object.entries(data.responseJSON).forEach(([key, value]) => {
              var id = "#" + key;
              var div_id = "#" + key + "-div";
              $( div_id ).empty();
              value.forEach((error) => {
                $( div_id ).append(error + "<br>");
              });
              $( id ).addClass('is-invalid');
              });
            }
          })
        return false;
      }
    });
});
