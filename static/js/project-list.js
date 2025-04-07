document.addEventListener('DOMContentLoaded', function() {
    
    // Project filtering
    var filterButtons = document.querySelectorAll('.filter-btn');
    var projectItems = document.querySelectorAll('.project-item');

    filterButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            filterButtons.forEach(function(btn) {
                btn.classList.remove('active');
            });

            // Add active class to clicked button
            this.classList.add('active');

            var filter = this.getAttribute('data-filter');

            // Show projects based on what has been filter selection
            projectItems.forEach(function(item) {
                if (filter === 'all') {
                    item.style.display = '';
                    
                } else {
                    var itemStatus = item.getAttribute('data-status');
                    var normalisedFilter = filter.toUpperCase().replace(/-/g, '_');
                    if (itemStatus === normalisedFilter) {
                        item.style.display = '';

                    } else {
                        item.style.display = 'none';
                    }
                }
            });
        });
    });
})