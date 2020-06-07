$(document).ready(function(){
  function readURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {
            $('#post-image')
                .attr('src', e.target.result)
        };
        reader.readAsDataURL(input.files[0]);
    }
  }

  $("#image").on("change", function(event){
    var filename = event.target.value.split("\\").pop();
    $("#post-image-label").text(filename);
    readURL(this);
  });
  $("#post_update-form").on('submit', function() {
    $( "#title" ).removeClass('is-invalid');
    $( "#image" ).removeClass('is-invalid');
    $( "#description" ).removeClass('is-invalid');
    $( "#content" ).removeClass('is-invalid');
    if ($("#post_update-form")[0].checkValidity() === false) {
        $( "#title-div" ).empty();
        $( "#image-div" ).empty();
        $( "#description-div" ).empty();
        $( "#content-div" ).empty();
        $( "#title-div" ).append( "Please provide a valid Title" );
        $( "#image-div" ).append( "Please provide a valid Image" );
        $( "#description-div" ).append( "Please provide a valid Description" );
        $( "#content-div" ).append( "Please provide a valid Content" );
        $("#post_update-form")[0].classList.add('was-validated');
        return false;
        }
    else {
      $.ajax({
        url: $("#post_update-form").attr("data-url"),
        type: 'POST',
        data: $("#post_update-form").serialize(),
        dataType: 'json',
        })

      .done(function() {
        $("#post_update-form").unbind('submit').submit();
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
})
