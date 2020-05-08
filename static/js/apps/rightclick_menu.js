  const formatter = new Intl.NumberFormat('en-US', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  });

  $('tr.mydata-row').bind("contextmenu", function(event) {
    // Avoid the real one
    event.preventDefault();
    // Show contextmenu
    $(".custom-menu").finish().toggle(100).
    // In the right position (the mouse)
    css({
      top: event.pageY + 5 + "px",
      left: event.pageX + 5 + "px"
    });
  });
  // If the document is clicked somewhere
  $('tr.mydata-row').bind("mousedown", function(e) {
    // If the clicked element is not the menu
    if (!$(e.target).parents(".custom-menu").length > 0) {
      $(".custom-menu").hide(100);
    }
  });

  var id;
  // If the menu element is clicked

  $("tr.mydata-row").contextmenu(function() {
    // This is the triggered action name
    id = $(this).find('td#customer-id').attr("value");

  });

  $("tr.mydata-row").click(function() {
    $(".custom-menu").hide(100);
  });

  $(document).mouseup(function(e){
    var container = $(".custom-menu");
    // If the target of the click isn't the container
    if(!container.is(e.target) && container.has(e.target).length === 0){
        container.hide(100);
    }
  });

  // $(document).mouseup(function(e){
  //   var container = $(".filter-group");
  //   // If the target of the click isn't the container
  //   if(!container.is(e.target) && container.has(e.target).length === 0){
  //       container.hide(80);
  //   }
  // });

  // PRICE FORMATTING
  $('td.price-per-unit').each(function(){
    $(this).html(formatter.format($(this).html()));
  });

  $('td.srp').each(function(){
    $(this).html(formatter.format($(this).html()));
  });

  $('td.profit').each(function(){
    $(this).html(formatter.format($(this).html()));
  });

  $('td.investment').each(function(){
    $(this).html(formatter.format($(this).html()));
  });
