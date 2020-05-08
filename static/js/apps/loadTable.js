var table = $('#myTable').DataTable({
   'columnDefs': [{ 'targets': 0, 'checkboxes': { 'selectRow': true }}],
   'select': { 'style': 'multi' },
   'order': [[1, 'asc']]


});

$("#min").datepicker({ onSelect: function () { table.draw(); }, changeMonth: true, changeYear: true, maxDate: 0,
  onSelect: function(dateText, inst) {
    var actualDate = new Date(dateText);
    var newDate = new Date(actualDate.getFullYear(), actualDate.getMonth(), actualDate.getDate());
    $('#max').datepicker('option', 'minDate', newDate );
  }
});
$("#max").datepicker({ onSelect: function () { table.draw(); }, changeMonth: true, changeYear: true, maxDate: 0 });
            // Event listener to the two range filtering inputs to redraw on input
  $('#min, #max').change(function () {
    table.draw();
  });

// /////////////////////////////////////  /////////

$("#category_list").change(function(){
selected = $('#category_list option:selected').text();
table.columns(3).search(selected).draw();
});

$("#distributor_list").change(function(){
  selected = $('#distributor_list option:selected').text();
  table.columns(4).search(selected).draw();
});

$("#customer_list").change(function(){
  selected = $('#customer_list option:selected').text();
  table.columns(3).search(selected).draw();
});

$("#status_list").change(function(){
  selected = $('#status_list option:selected').text();
  table.columns(6).search(selected).draw();
});

function getSelectedItems(){
  var form = $('#frm-table');

  var rows_selected = table.column(0).checkboxes.selected();

  // Iterate over all selected checkboxes
  $.each(rows_selected, function(index, rowId){
     // Create a hidden element
     $(form).append($('<input>').attr('type', 'hidden').attr('name', 'id[]').val(rowId));
  });

  selected_items = rows_selected.join(",");

}
