$(function() {
  $("a").click(
    function() {
      var my_id = $(this).attr('data-name');

      $("#hide1").attr('value', my_id);
    })
});