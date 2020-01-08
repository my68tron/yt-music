$(function() {
   $('.flash-message').delay(1000).fadeIn('normal', function() {
      $(this).delay(4000).fadeOut();
   });
});
function sendDownloadFlashMessage(s) {
   var selector = "." + s;
   $(selector).delay(1000).fadeIn('normal', function() {
      $(this).delay(4000).fadeOut();
   });
}

$('.download-url').click(function(e){
   e.preventDefault();
   if ($(".download-url-flash").length == 0) {
      $("body").append('<div class="flash-message download-url-flash alert alert-info alert-dismissable fade show" role="alert"><button type="button" class="close" data-dismiss="alert" aria-label="Close" aria-hidden="true">&times;</button>Processing Download...<br>Visit Archive Page to Download your Song</div>');
      $("body").append('<div class="flash-message download-url-ready-flash alert alert-success alert-dismissable fade show" role="alert"><button type="button" class="close" data-dismiss="alert" aria-label="Close" aria-hidden="true">&times;</button>Download Ready<br>Visit Archive Page to Download your Song</div>');
   }
   sendDownloadFlashMessage("download-url-flash");
   var dataUrl = $(this).attr("data-url");
   $.ajax({
      type:"GET",
      url: "/download/url/" + dataUrl,
      data: {
         url: dataUrl,
      },
      success: function( response, textStatus, xhr ) {
         sendDownloadFlashMessage("download-url-ready-flash");
      },
      error: function( xhr, ajaxOptions, thrownError ){
         alert("ERROR!\n\n" + "Your download ain't ready.\n\n" + "Maybe file is greter than 10 min.");
      }
   });
});

$('.download-page-form').submit(function(event) {
   event.preventDefault();
   var submitButton = $(this).find("button[type='submit']");
   submitButton.prop('disabled',true);
   submitButton.text('Processing');
   if ($(".download-url-flash").length == 0) {
      $("body").append('<div class="flash-message download-url-ready-flash alert alert-success alert-dismissable fade show" role="alert"><button type="button" class="close" data-dismiss="alert" aria-label="Close" aria-hidden="true">&times;</button>Download Ready<br>Visit Archive Page to Download your Song</div>');
   }
   var formData = {
      'download': $('input[name=download]').val(),
   };
   $.ajax({
      type        : 'GET',
      url         : '/download',
      data        : formData,
      // dataType    : 'json',
      encode      : true,
      success: function( response, textStatus, xhr ) {
         sendDownloadFlashMessage("download-url-ready-flash");
      },
      error       : function( xhr, ajaxOptions, thrownError ){
         alert("ERROR!\n\n" + "Your download ain't ready.\n\n" + "Maybe file is greter than 10 min.");
      },
      complete: function(data) {
         submitButton.prop('disabled', false);
         submitButton.text('Download');
      }
   });
   // .done(function(data) {
   //    sendDownloadFlashMessage("download-url-ready-flash");
   // });
});