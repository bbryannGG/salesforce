$.fn.dataTable.ext.search.push(
  function(settings, data, dataIndex) {
    var min = $('#min').datepicker("getDate");
    var max = $('#max').datepicker("getDate");
    console.log(min);
    console.log(max);
    var startDate = new Date(data[7]);
    if (min == null && max == null) {
      return true;
    }
    if (min == null && startDate <= max) {
      return true;
    }
    if (max == null && startDate >= min) {
      return true;
    }
    if (startDate <= max && startDate >= min) {
      return true;
    }
    return false;
  }
);
