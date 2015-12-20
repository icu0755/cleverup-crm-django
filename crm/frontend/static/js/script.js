jQuery(function ($) {
    "use strict";
    $.fn.datepicker.defaults.format = "yyyy-mm-dd";
    $.fn.datepicker.defaults.autoclose = true;
    $('.cu-datepicker, #id_paid_at').datepicker();
});
