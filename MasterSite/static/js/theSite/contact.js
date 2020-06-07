$(document).ready(function(){
  $(".nav").find(".active").removeClass("active");
  $(".link-7").addClass("active");

  $("#contact-form").on('submit', function() {
    $( "#name" ).removeClass('is-invalid');
    $( "#email" ).removeClass('is-invalid');
    $( "#phone_number" ).removeClass('is-invalid');
    $( "#content" ).removeClass('is-invalid');
    if ($("#contact-form")[0].checkValidity() === false) {
        $( "#name-div" ).empty();
        $( "#email-div" ).empty();
        $( "#phone_number-div" ).empty();
        $( "#content-div" ).empty();
        $( "#name-div" ).append( "Please provide a valid Name" );
        $( "#email-div" ).append( "Please provide a valid Email" );
        $( "#phone_number-div" ).append( "Please provide a valid Phone Number" );
        $( "#content-div" ).append( "Please provide a valid Message" );
        $("#contact-form")[0].classList.add('was-validated');
        return false;
        }
    else {
      $.ajax({
        url: '/contact/',
        type: 'POST',
        data: $("#contact-form").serialize(),
        dataType: 'json',
        })

      .done(function() {
        $("#contact-form").unbind('submit').submit();
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
