$('#selectall').change(function () {
    if ($(this).prop('checked')) {
    $('input').prop('checked', true);
    }
    else {
        $('input').prop('checked', false);
    }
});
$('#selectall').trigger('change');