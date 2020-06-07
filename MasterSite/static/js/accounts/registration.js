$(document).ready(function(){
   $(".nav").find(".active").removeClass("active");
   $(".link-4").addClass("active");
   $("#image").on("change", function(event){
     var filename = event.target.value.split("\\").pop();
     $("#label-form-image").text(filename);
   })
   $("#registration-form").on('submit', function() {
      $( "#first_name" ).removeClass('is-invalid');
      $( "#last_name" ).removeClass('is-invalid');
      $( "#email" ).removeClass('is-invalid');
      $( "#username" ).removeClass('is-invalid');
      $( "#profile_pic" ).removeClass('is-invalid');
      $( "#password1" ).removeClass('is-invalid');
      $( "#password2" ).removeClass('is-invalid');
       if ($("#registration-form")[0].checkValidity() === false) {
         $( "#first_name-div" ).empty();
         $( "#last_name-div" ).empty();
         $( "#email-div" ).empty();
         $( "#username-div" ).empty();
         $( "#profile_pic-div" ).empty();
         $( "#password1-div" ).empty();
         $( "#password2-div" ).empty();
         $( "#first_name-div" ).append( "Please provide a valid First Name" );
         $( "#last_name-div" ).append( "Please provide a valid Last Name" );
         $( "#email-div" ).append( "Please provide a valid Email" );
         $( "#username-div" ).append( "Please provide a valid Username" );
         $( "#profile_pic-div" ).append( "Please provide a valid Profile Picture" );
         $( "#password1-div" ).append( "Please provide a valid Password" );
         $( "#password2-div" ).append( "Please provide a valid Password" );
         $("#registration-form")[0].classList.add('was-validated');
         return false;
       }
       else {
         $.ajax({
           url: '/accounts/register/',
           type: 'POST',
           data: $("#registration-form").serialize(),
           // dataType: 'json',
         })

         .done(function() {
           $("#registration-form").unbind('submit').submit();
          })

         .fail(function(data) {
           console.log(data);
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
