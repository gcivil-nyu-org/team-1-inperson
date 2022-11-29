var text_max = 200;
$('#count_message').html('0 / ' + text_max );

$('#message-text').keyup(function() {
  var text_length = $('#message-text').val().length;
  var text_remaining = text_max - text_length;
  
  $('#count_message').html(text_length + ' / ' + text_max);
});