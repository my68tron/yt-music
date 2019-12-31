$(function() {
    $('.flash-message').delay(1000).fadeIn('normal', function() {
       $(this).delay(4000).fadeOut();
    });
 });