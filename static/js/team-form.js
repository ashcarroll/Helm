$(document).ready(function() {
    // Basic initialization
    $('.select2-multiple').select2({
        width: '100%',
        placeholder: 'Select team members',
        allowClear: true,
        closeOnSelect: false,
        theme: 'classic',
        // Tags-like visual style
        templateSelection: function(data) {
            if (!data.id) { return data.text; }
            return $('<span class="select2-selection__choice__pill">' + data.text + '</span>');
        }, 
        selectionCssClass: 'select2-selection--clean'
    });
});