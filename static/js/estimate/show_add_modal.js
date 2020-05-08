  $(function() {

    $(".create-product").each(function() {
      $(this).modalForm({
        formURL: $(this).data('id')
      });
    });

    $(".create-tax").each(function() {
      $(this).modalForm({
        formURL: $(this).data('id')
      });
    });

  });
