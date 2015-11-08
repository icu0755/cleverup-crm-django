jQuery(function ($) {
    "use strict";
    $.fn.datepicker.defaults.format = "yyyy-mm-dd";
    $.fn.datepicker.defaults.autoclose = true;
    $('.cu-datepicker').datepicker();
});
