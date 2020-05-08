var context = [];
$(document).ready(function() {

  // SELECTING HEADER CHECKBOX
  function check_uncheck(){
    $("input.mycheck-th").click(function() {
      if ($(this).prop("checked") === true) {
        context = []
        $("input.mycheck-td").each(function() {
          $(this).prop("checked", true);
          context.push($(this).val());
          $('#batch_action').show();
        });

      }
      else if ($(this).prop("checked") === false) {
        $("input.mycheck-td").each(function() {
          context = []
          $(this).prop("checked", false)
          $('#batch_action').hide();
        });
      }
    });
  }
  check_uncheck();

  // SELECTING INDIVIDUAL CHECKBOX
  var propertyCheck = [];
  $('input.mycheck-td').click(function() {
    if ($(this).prop("checked") == true) {
      context.push($(this).val());
      $('#batch_action').show();
      console.log("You clicked the TD")
      console.log(context);
      let checker = arr => arr.every(Boolean);

      propertyCheck = [];
      $("input.mycheck-td").each(function() {
        propertyCheck.push($(this).prop("checked"));
      });

      if(checker(propertyCheck)){
        $('input.mycheck-th').prop('checked', true);
      }
    }
    else if ($(this).prop("checked") == false) {
      console.log("You un clicked the TD")
      var index = context.indexOf($(this).val());

      if (index > -1) {
         context.splice(index, 1);
      }
      $('input.mycheck-th').prop("checked", false);
      if(context.length === 0){
        $('#batch_action').hide();
      }
      console.log(context);
    }
  });

  function resetCheck(){
    check_uncheck();
    context = []
    $('input.mycheck-th').prop("checked", false);

    $("input.mycheck-td").each(function() {
      $(this).prop("checked", false);
    });
    console.log(context);
    $('#batch_action').hide();

  }
  function alertme(){
    alert("awdawd");
  }

  $("input.mycheck-td").each(function() {
    console.log($(this).val());
  });
  $("select.custom-select").change(resetCheck);
  $("#myTable_paginate select").change(resetCheck);
  $('input[type="search"]').on('input', resetCheck);
  $('th.sort').click(resetCheck);
});
