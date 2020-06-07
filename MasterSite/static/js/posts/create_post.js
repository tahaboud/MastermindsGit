$(document).ready(function(){
  $(".nav").find(".active").removeClass("active");
  $(".link-5").addClass("active");
  $("#image").on("change", function(event){
    var filename = event.target.value.split("\\").pop();
    $("#label-form-image").text(filename);
  })
  $("#create_post-form").on('submit', function() {
    $( "#title" ).removeClass('is-invalid');
    $( "#image" ).removeClass('is-invalid');
    $( "#description" ).removeClass('is-invalid');
    $( "#content" ).removeClass('is-invalid');
    if ($("#create_post-form")[0].checkValidity() === false) {
        $( "#title-div" ).empty();
        $( "#image-div" ).empty();
        $( "#description-div" ).empty();
        $( "#content-div" ).empty();
        $( "#title-div" ).append( "Please provide a valid Title" );
        $( "#image-div" ).append( "Please provide a valid Image" );
        $( "#description-div" ).append( "Please provide a valid Description" );
        $( "#content-div" ).append( "Please provide a valid Content" );
        $("#create_post-form")[0].classList.add('was-validated');
        return false;
        }
    else {
      $.ajax({
        url: '/posts/create_post/',
        type: 'POST',
        data: $("#create_post-form").serialize(),
        dataType: 'json',
        })

      .done(function() {
        $("#create_post-form").unbind('submit').submit();
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
