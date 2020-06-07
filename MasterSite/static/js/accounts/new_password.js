$(document).ready(function() {
  $(".nav").find(".active").removeClass("active");
  $("#reset_password-form").on('submit', function() {
     $( "#new_password1" ).removeClass('is-invalid');
     $( "#new_password2" ).removeClass('is-invalid');
      if ($("#reset_password-form")[0].checkValidity() === false) {
        $( "#new_password1-div" ).empty();
        $( "#new_password2-div" ).empty();
        $( "#new_password1-div" ).append( "Please provide a valid Password" );
        $( "#new_password2-div" ).append( "Please provide a valid Password" );
        $("#reset_password-form")[0].classList.add('was-validated');
        return false;
      }
      else {
        $.ajax({
          url: $("#reset_password-form").attr("data-url"),
          type: 'POST',
          data: $("#reset_password-form").serialize(),
        })

        .done(function() {
          $("#reset_password-form").unbind('submit').submit();
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
