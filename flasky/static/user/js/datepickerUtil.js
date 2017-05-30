define('datepickerUtil', ['jquery', 'datepicker', 'datepickerzhCN'], function ($) {
    return {
        initDatePicker: function () {
            initDatePicker($('#last-login-time .input-daterange'));
            initDatePicker($('#sign-up-time .input-daterange'));

            function initDatePicker(jqeuryElement) {
                jqeuryElement.datepicker({
                    format: 'yyyy-mm-dd',
                    clearBtn: true,
                    language: 'zh-CN',
                    todayHighlight: true
                })
            }
        },
        clearDateRanger: function () {
            $('.input-daterange input').each(function () {
                $(this).datepicker('clearDates');
            });
        }
    }
});