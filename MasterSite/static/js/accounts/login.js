$(document).ready(function(){
   $(".nav").find(".active").removeClass("active");
   $(".link-2").addClass("active");

   $("#login-form").on('submit', function() {
      $( "#email" ).removeClass('is-invalid');
      $( "#password" ).removeClass('is-invalid');
       if ($("#login-form")[0].checkValidity() === false) {
         $( "#email-div" ).empty();

         $( "#password-div" ).empty();

         $( "#email-div" ).append( "Please provide a valid email" )
         $( "#password-div" ).append( "Please provide a valid password" )
         $("#login-form")[0].classList.add('was-validated');
         return false;
       }
       else {
         $.ajax({
           url: '/accounts/login/',
           type: 'POST',
           data: $("#login-form").serialize(),
           dataType: 'json',
         })

         .done(function() {
           $("#login-form").unbind('submit').submit()
          })

         .fail(function(data) {
           if (data.responseJSON) {
             Object.entries(data.responseJSON).forEach(([key, value]) => {
               if (key === "email") {
                 $( "#email-div" ).empty();
                 value.forEach((error) => {
                   $( "#email-div" ).append(error + "<br>");
                 });

                 $("#email").addClass('is-invalid');
               }
               else if (key === "password") {
                 $( "#password-div" ).empty();
                 value.forEach((error) => {
                   $( "#password-div" ).append( error + "<br>" );
                 });
                 $("#password").addClass('is-invalid');
               }
               else if (key === "__all__") {
                $( "#password-div" ).empty();
                $( "#email-div" ).empty();
                value.forEach((error) => {
                  $( "#email-div" ).append( error + "<br>" );
                  $( "#password-div" ).append(error + "<br>");
                });
                $("#password").addClass('is-invalid');
                $("#email").addClass('is-invalid');
              }
             });
           }

           })
       }
       return false;
     });
});
