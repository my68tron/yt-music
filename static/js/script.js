$(function() {
    $('.flash-message').delay(1000).fadeIn('normal', function() {
       $(this).delay(4000).fadeOut();
    });
 });

 $('.download-url').click(function(e){
   e.preventDefault();
   // catid = $(this).attr("data-catid");
   var dataUrl = $(this).attr("data-url");
   console.log(dataUrl)
   $.ajax({
      type:"GET",
      url: "/download/" + dataUrl,
      data:{
         url: dataUrl,
      },
      success: function( response, textStatus, xhr ) {
         alert("Your download is ready.\n\nGo to Downloads Page to download your song" + textStatus);
      },
      error: function( xhr, ajaxOptions, thrownError ){
         alert("ERROR!\n" + thrownError +"\nYour download ain't ready.\n\n" + xhr.responseJSON['flash_message']);
      }
      
   })
});