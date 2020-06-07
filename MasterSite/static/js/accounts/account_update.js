$(document).ready(function(){
   $("#image-div").mouseover(function(event) {
     $("#change-image").css("display", "inline-block");
   });
   $("#image-div").mouseout(function() {
     $("#change-image").hide();
   });
   $(".nav").find(".active").removeClass("active");
   $(".link-0").addClass("active");
   $("#profile_pic").on("change", function(event){
     var filename = event.target.value.split("\\").pop();
     $("#profile_pic-label").text(filename);
     var reader = new FileReader();
     reader.onload = function (e) {
         $('#image')
             .attr('src', e.target.result)
     };
     reader.readAsDataURL(this.files[0]);
   });
   $("#account_update-form").on('submit', function() {
      $( "#first_name" ).removeClass('is-invalid');
      $( "#last_name" ).removeClass('is-invalid');
      $( "#email" ).removeClass('is-invalid');
      $( "#username" ).removeClass('is-invalid');
      $( "#profile_pic" ).removeClass('is-invalid');
       if ($("#account_update-form")[0].checkValidity() === false) {
         $( "#first_name-div" ).empty();
         $( "#last_name-div" ).empty();
         $( "#email-div" ).empty();
         $( "#username-div" ).empty();
         $( "#profile_pic-div" ).empty();
         $( "#first_name-div" ).append( "Please provide a valid First Name" );
         $( "#last_name-div" ).append( "Please provide a valid Last Name" );
         $( "#email-div" ).append( "Please provide a valid Email" );
         $( "#username-div" ).append( "Please provide a valid Username" );
         $( "#profile_pic-div" ).append( "Please provide a valid Profile Picture" );
         $("#account_update-form")[0].classList.add('was-validated');
         return false;
       }
       else {
         $.ajax({
           url: $("#account_update-form").attr("data-url"),
           type: 'POST',
           data: $("#account_update-form").serialize(),
           // dataType: 'json',
         })

         .done(function() {
           $("#account_update-form").unbind('submit').submit();
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
