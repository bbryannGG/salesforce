$(".read-data").each(function() {
  $(this).modalForm({
    formURL: $(this).data('id')
  });
});
$(".add-data").each(function() {
  $(this).modalForm({
    formURL: $(this).data('id')
  });
});
