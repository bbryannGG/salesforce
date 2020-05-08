$(document).ready(function() {
  $('#myTable').DataTable({
    stateSave: true,
    "pagingType": "full_numbers",
    "language": {
      "decimal": ",",
      "thousands": ".",
    },
    "dom": '<"top"i>rt<"bottom"flp><"clear">',
  });
});

window.onload = function() {
  $("#batch_action").hide();
};

var context = [];
$(document).ready(function() {

  $('tr').on('contextmenu', function(e) {
    // alert($(this).attr('id'));
    return false;
  });

  $("input.mycheck-th").click(function() {
    if ($(this).prop("checked") == true) {
      context = []
      $("input.mycheck-td").each(function() {
        context.push($(this).val());
        $(this).prop("checked", true)
        $('#batch_action').show();
        alert("This is the context: " + context);

      });
    } else if ($(this).prop("checked") == false) {
      $("input.mycheck-td").each(function() {
        context = []
        $(this).prop("checked", false)
        $('#batch_action').hide();
        alert("This is the context: " + context);
      });
    }
    console.log(context);
  });

  $('input.mycheck-td').click(function() {
    if ($(this).prop("checked") == true) {
      context.push($(this).val());
      console.log(context);
    } else if ($(this).prop("checked") == false) {
      const index = context.indexOf($(this).val());
      if (index > -1) {
        context.splice(index, 1);
      }
      if (context.length === 0) {
        $('input.mycheck-th').prop("checked", false);
      }
      alert($(this).val());
    }

    console.log(context);
    if (context.length === 0) {
      $('#batch_action').hide();
      $('input.mycheck-td').prop("checked", false);
    } else {
      $('#batch_action').show();
    }
  });
});

$("a.batch_export").on("click", function() {
  context = context.toString();
  var url = "{% url 'customer-export_batch' 'test' %}";
  url = url.replace('test', context);
  $(this).attr("href", url);
});

$("a.batch_delete").on("click", function() {
  context = context.toString();
  var url = "{% url 'customer-delete-batch' 'test' %}";
  url = url.replace('test', context);
  $(this).attr("href", url);
});

if (context.length === 0) {
  $('#batch_action').hide();
} else {
  $('#batch_action').show();
}
