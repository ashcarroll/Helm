$(document).ready(function() {
    // Basic initialization
    $('.select2-multiple').select2({
        width: '100%',
        placeholder: 'Select team members',
        allowClear: true,
        closeOnSelect: false,
        // Tags-like visual style
        templateSelection: function(data) {
            if (!data.id) { return data.text; }
            return $('<span class="badge bg-primary me-1">' + data.text + '</span>');
        }
    });
});