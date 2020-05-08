const formatter = new Intl.NumberFormat('en-US', {
  minimumFractionDigits: 2,
  maximumFractionDigits: 2,
});



function recalculateInvestment() {
  var overallInvestment = 0;
  $(".total-investment").each(function() {
    formattedInvestmentValue = this.value.replace(',', '')
    if (!isNaN(formattedInvestmentValue) && formattedInvestmentValue.length > 0) {
      overallInvestment = parseFloat(overallInvestment) + parseFloat(formattedInvestmentValue);
      $('id_overallInvestment').val(overallInvestment.toFixed(2));
    }
  });
  $('#id_overallInvestment').val(overallInvestment);
}

function recalculateNonTax() {
  var overallNonTax = 0;
  $(".total-nontax").each(function() {
    formattedNonTaxValue = this.value.replace(',', '')
    if (!isNaN(formattedNonTaxValue) && formattedNonTaxValue.length > 0) {
      overallNonTax = parseFloat(overallNonTax) + parseFloat(formattedNonTaxValue);
    }
  });
  $('#id_overallNonTax').val(overallNonTax.toFixed(2));
}

function recalculateTaxPerLot() {
  var overallTaxPerLot = 0;
  $(".totaltax-per-lot").each(function() {
    formattedTaxPerLot = this.value.replace(',', '')
    if (!isNaN(formattedTaxPerLot) && formattedTaxPerLot.length > 0) {
      overallTaxPerLot = parseFloat(overallTaxPerLot) + parseFloat(formattedTaxPerLot);
    }
  });
  $('#id_overallTaxPerLot').val(overallTaxPerLot.toFixed(2));
}

function recalculateWithTaxPerUnit() {
  var overallWithTaxPerUnit = 0;
  $(".totalwithtax-per-unit").each(function() {
    fomattedWithTaxPerUnit = this.value.replace(',', '')
    if (!isNaN(fomattedWithTaxPerUnit) && fomattedWithTaxPerUnit.length > 0) {
      overallWithTaxPerUnit = parseFloat(overallWithTaxPerUnit) + parseFloat(fomattedWithTaxPerUnit);
    }
  });

  $('#id_overallWithTaxPerUnit').val(overallWithTaxPerUnit.toFixed(2));
}

function recalculateWithTax() {
  var overallWithTax = 0;
  $(".totalWithTax").each(function() {
    formattedWithTax = this.value.replace(',', '')
    if (!isNaN(formattedWithTax) && formattedWithTax.length > 0) {
      overallWithTax = parseFloat(overallWithTax) + parseFloat(formattedWithTax);
    }
  });
  $('#id_overallWithTax').val(overallWithTax.toFixed(2));
}

function recalculateProfit() {
  var overallProfit = 0;
  $(".profits").each(function() {
    formattedProfit = this.value.replace(',', '')
    if (!isNaN(formattedProfit) && formattedProfit.length > 0) {
      overallProfit = parseFloat(overallProfit) + parseFloat(formattedProfit);
    }
  });
  $('#id_overallProfit').val(overallProfit.toFixed(2));
}

function recalculateOverall(){
  setTimeout(recalculateInvestment, 1);
  setTimeout(recalculateNonTax, 1);
  setTimeout(recalculateTaxPerLot, 1);
  setTimeout(recalculateWithTaxPerUnit, 1);
  setTimeout(recalculateWithTax, 1);
  setTimeout(recalculateProfit, 1);
}

function resetCalculatedValue(formNumber){
  $('#id_form-' + formNumber + '-qty').val("");
  $('#id_form-' + formNumber + '-markup').val("");
  $('#id_form-' + formNumber + '-totalInvestment').val("");
  $('#id_form-' + formNumber + '-newSRPPerUnit').val("");
  $('#id_form-' + formNumber + '-totalNonTax').val("");
  $('#id_form-' + formNumber + '-taxPerUnit').val("");
  $('#id_form-' + formNumber + '-totalTaxPerLot').val("");
  $('#id_form-' + formNumber + '-totalWithTaxPerUnit').val("");
  $('#id_form-' + formNumber + '-totalWithTax').val("");
  $('#id_form-' + formNumber + '-profit').val("");
}

function resetProductDetails(formNumber){
  $("#id_form-" + formNumber + "-description").val("");
  $("#id_form-" + formNumber + "-serialNo").val("");
  $("#id_form-" + formNumber + "-pricePerUnit").val("");
  $("#id_form-" + formNumber + "-srp").val("");
  $("#id_form-" + formNumber + "-distributor").val("");
}

function resetAllTotal(formNumber){
  $('#id_form-' + formNumber + '-totalInvestment').val("0.00");
  $('#id_form-' + formNumber + '-newSRPPerUnit').val("0.00");
  $('#id_form-' + formNumber + '-totalNonTax').val("0.00");
  $('#id_form-' + formNumber + '-taxPerUnit').val("0.00");
  $('#id_form-' + formNumber + '-totalTaxPerLot').val("0.00");
  $('#id_form-' + formNumber + '-totalWithTaxPerUnit').val("0.00");
  $('#id_form-' + formNumber + '-totalWithTax').val("0.00");
  $('#id_form-' + formNumber + '-profit').val("0.00");
}

function resetAllTotalxInvest(formNumber){
  $('#id_form-' + formNumber + '-newSRPPerUnit').val("0.00");
  $('#id_form-' + formNumber + '-totalNonTax').val("0.00");
  $('#id_form-' + formNumber + '-taxPerUnit').val("0.00");
  $('#id_form-' + formNumber + '-totalTaxPerLot').val("0.00");
  $('#id_form-' + formNumber + '-totalWithTaxPerUnit').val("0.00");
  $('#id_form-' + formNumber + '-totalWithTax').val("0.00");
  $('#id_form-' + formNumber + '-profit').val("0.00");
}

function returnFormNumber(selectID){
  if ($.isNumeric(selectID.slice(8, 10))) {
    return selectID.slice(8, 10);
  } else {
    return selectID.slice(8, 9);
  }
}

function setCalculatedValues(formNumber, markupValue, priceperunit){
  var markup = parseFloat(markupValue / 100);
  var qty = parseFloat($('#id_form-' + formNumber + '-qty').val());
  var totalInvestment = $('#id_form-' + formNumber + '-totalInvestment').val();
  var newSRPPerUnit = priceperunit / (1 - markup);
  var totalNonTax = newSRPPerUnit * qty;
  var taxPerUnit = newSRPPerUnit * 0.035;
  var totalTaxPerLot = (taxPerUnit * qty);
  var totalWithTaxPerUnit = newSRPPerUnit + taxPerUnit;
  var totalWithTax = totalWithTaxPerUnit * qty;
  var profit = totalNonTax - totalInvestment;

  $('#id_form-' + formNumber + '-newSRPPerUnit').val(newSRPPerUnit.toFixed(2));
  $('#id_form-' + formNumber + '-totalNonTax').val(totalNonTax.toFixed(2));
  $('#id_form-' + formNumber + '-taxPerUnit').val(taxPerUnit.toFixed(2));
  $('#id_form-' + formNumber + '-totalTaxPerLot').val(totalTaxPerLot.toFixed(2));
  $('#id_form-' + formNumber + '-totalWithTaxPerUnit').val(totalWithTaxPerUnit.toFixed(2));
  $('#id_form-' + formNumber + '-totalWithTax').val(totalWithTax.toFixed(2));
  $('#id_form-' + formNumber + '-profit').val(profit.toFixed(2));
  recalculateProfit();
  recalculateNonTax();
  recalculateTaxPerLot();
  recalculateWithTaxPerUnit();
  recalculateWithTax();
}

// //////////////QUANTITY COMPUTATION
$(".price-per-unit").on("input", function() {

  // GET THE ID OF SELECTED ITEM
  var formNumber = returnFormNumber($(this).attr("id"));

  var qty = parseFloat($("#id_form-" + formNumber + '-qty').val());
  var priceperunit = parseFloat($("#id_form-" + formNumber + '-pricePerUnit').val());
  var markupValue = $("#id_form-" + formNumber + '-markup').val();

  if($.isNumeric(qty)){

    if($.isNumeric(priceperunit)){

      var totalinvestment = qty * priceperunit;
      $('#id_form-' + formNumber + '-totalInvestment').val(totalinvestment.toFixed(2));
      recalculateInvestment();

      if($.isNumeric(markupValue)){
        setCalculatedValues(formNumber, markupValue, priceperunit);
      }

    }
    else{
      resetAllTotal(formNumber);
      recalculateInvestment();
    }
  }
});


$(".quantity").on("input", function() {
  // Get the id of selected item
  var formNumber = returnFormNumber($(this).attr("id"));

  var qty = parseFloat($("#id_form-" + formNumber + '-qty').val());
  var priceperunit = parseFloat($('#id_form-' + formNumber + '-pricePerUnit').val());
  var markupValue = $('#id_form-' + formNumber + '-markup').val()

  if($.isNumeric(qty)){

    if($.isNumeric(priceperunit)){

      var totalinvestment = qty * priceperunit;
      $('#id_form-' + formNumber + '-totalInvestment').val(totalinvestment.toFixed(2));
      recalculateInvestment();

      if($.isNumeric(markupValue)){
        setCalculatedValues(formNumber, markupValue, priceperunit);
      }
      else{
        resetAllTotalxInvest(formNumber);
      }

    }
    else{
      alert("Item has an invalid price.")
      $('#id_form-' + formNumber + '-pricePerUnit').focus();
    }
  }
  else{
    resetAllTotal(formNumber);
    recalculateInvestment();
  }

});

// /////////////////    RECALCULATE MARKUP       /////////////////
$(".markup").on("input", function() {

  var formNumber = returnFormNumber($(this).attr("id"));

  var markupValue = $("#id_form-" + formNumber + '-markup').val();
  var markup = parseFloat(markupValue / 100);
  var priceperunit = parseFloat($('#id_form-' + formNumber + '-pricePerUnit').val());
  var qty = parseFloat($('#id_form-' + formNumber + '-qty').val());
  var totalInvestment = $('#id_form-' + formNumber + '-totalInvestment').val();

  if($.isNumeric(markupValue)){
    if($.isNumeric(priceperunit)){
      if($.isNumeric(qty)){
        setCalculatedValues(formNumber, markupValue, priceperunit);
      }
      else{
        alert("Please insert a valid quantity.");
        $('#id_form-' + formNumber + '-qty').focus();
      }
    }
    else{
      alert("Please insert a valid price.");
      $('#id_form-' + formNumber + '-pricePerUnit').focus();
    }
  }
  else{
    resetAllTotalxInvest(formNumber);
    recalculateProfit();
    recalculateNonTax();
    recalculateTaxPerLot();
    recalculateWithTaxPerUnit();
    recalculateWithTax();
  }
});


// RECALCULATE INVESTMENT UPON DELETING A PRODUCT
$("button.remove-form-row").on("click", recalculateOverall);


// ///////////////////////////////////////////////////////
