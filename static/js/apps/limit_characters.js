var letnum = new RegExp("^[a-zA-Z ]+$");
var phonenum   = new RegExp('^[0-9()+-]');
var numonly   = new RegExp('^[0-9]');

$(document).on('keypress', '#id_contactPerson', function (event) {
    var key = String.fromCharCode(!event.charCode ? event.which : event.charCode);
    if (!letnum.test(key)) {
        event.preventDefault();
        return false;
    }
});

$(document).on('keypress', '#id_contactPerson2', function (event) {
    var key = String.fromCharCode(!event.charCode ? event.which : event.charCode);
    if (!letnum.test(key)) {
        event.preventDefault();
        return false;
    }
});

$(document).on('keypress', '#id_city', function (event) {
    var key = String.fromCharCode(!event.charCode ? event.which : event.charCode);
    if (!letnum.test(key)) {
        event.preventDefault();
        return false;
    }
});

$(document).on('keypress', '#id_country', function (event) {
    var key = String.fromCharCode(!event.charCode ? event.which : event.charCode);
    if (!letnum.test(key)) {
        event.preventDefault();
        return false;
    }
});

$(document).on('keypress', '#id_postalCode', function (event) {
    var key = String.fromCharCode(!event.charCode ? event.which : event.charCode);
    if (!numonly.test(key)) {
        event.preventDefault();
        return false;
    }
});

$(document).on('keypress', '#id_phone', function (event) {
    var key = String.fromCharCode(!event.charCode ? event.which : event.charCode);
    if (!phonenum.test(key)) {
        event.preventDefault();
        return false;
    }
});

$(document).on('keypress', '#id_phone', function (event) {
    var key = String.fromCharCode(!event.charCode ? event.which : event.charCode);
    if (!phonenum.test(key)) {
        event.preventDefault();
        return false;
    }
});
