document.addEventListener('DOMContentLoaded', function() {
    // Initialise Select2 for multiple selection
    $('.select2-multiple').select({
        theme: 'bootstrap-5',
        width: '100%',
        placeholder: 'Select team members',
        allowClear: true,
        closeOnSelect: false,

        // Using Ajax for better performance with large datasets
        ajax: {
            url: 'api/users/search',
            dataType: 'json',
            delay: 250,
            data: function(params) {
                return {
                    q: params.term || '',
                    page: params.page || 1
                };
            },
            processResults: function(data, params) {
                params.page = params.page || 1;

                return {
                    results: data.results,
                    pagination: {
                        more: data.paginatino.more
                    }
                };
            },
            cache: true
        },
        // Display existing selections
        templateResult: formatUser,
        templateSelection: formatUserSelection
    });

    // Format the dropdown options
    function formatUser(user) {
        if(!user.id) {
            return user.text;
        }

        return $('<span><strong>' + user.text + '</strong>' + (user.email ? ' (' + user.email + ')' : '') + '</span');
    }

    // Format the selection options
    function formatUserSelection(user) {
        return user.text;
    }
})