// Restricts input for the given textbox to the given inputFilter.


function setInputFilter(textbox, inputFilter) {
  ["input", "keydown", "keyup", "mousedown", "mouseup", "select", "contextmenu", "drop"].forEach(function(event) {
    textbox.addEventListener(event, function() {
      if (inputFilter(this.value)) {
        this.oldValue = this.value;
        this.oldSelectionStart = this.selectionStart;
        this.oldSelectionEnd = this.selectionEnd;
      } else if (this.hasOwnProperty("oldValue")) {
        this.value = this.oldValue;
        this.setSelectionRange(this.oldSelectionStart, this.oldSelectionEnd);
      } else {
        this.value = "";
      }
    });
  });
}

setInputFilter(document.getElementById("id_phone"), function(value) {
  return /^-?\d*$/.test(value); });

setInputFilter(document.getElementById("id_name"), function(value) {
  return /^[a-z-'.\s]*$/i.test(value); });

setInputFilter(document.getElementById("id_contactperson"), function(value) {
  return /^[a-z-'.\s]*$/i.test(value); });

setInputFilter(document.getElementById("id_addressline1"), function(value) {
  return /^[a-zA-Z0-9\s,.'-]*$/i.test(value); });

setInputFilter(document.getElementById("id_addressline2"), function(value) {
  return /^[a-zA-Z0-9\s,.'-]*$/i.test(value); });

setInputFilter(document.getElementById("id_city"), function(value) {
  return /^[a-z-'.\s]*$/i.test(value); });

setInputFilter(document.getElementById("id_postalcode"), function(value) {
  return /^-?\d*$/.test(value); });

setInputFilter(document.getElementById("id_country"), function(value) {
  return /^[a-z-.\s]*$/i.test(value); });
