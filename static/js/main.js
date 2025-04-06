document.addEventListener('DOMContentLoaded', function() {
    // Tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.forEach(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.forEach(function(popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl)
    });

    // Auto-close alerts
    var alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            var bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
            // Close after 5 seconds
        }, 5000); 
    });

    // Project status colour indicators - automatically apply styling based on status, instead of hardcoding the classes into the html
    var projectStatusElements = document.querySelectorAll('.project-status');
    projectStatusElements.forEach(function(statusElement) {
        var status = statusElement.dataset.status;
        switch(status) {
            case 'NOT_STARTED':
                statusElement.classList.add('badge', 'badge-not-started');
                break;
            case 'ON_TRACK':
                statusElement.classList.add('badge', 'badge-on-track');
                break;
            case 'AT_RISK':
                statusElement.classList.add('badge', 'badge-at-risk');
                break;
            case 'BLOCKED':
                statusElement.classList.add('badge', 'badge-blocked');
                break;
            case 'COMPLETE':
                statusElement.classList.add('badge', 'badge-complete');
                break;
        }
    });

    // Task status colour indicators
    var taskStatusElements = document.querySelectorAll('.task-status');
    taskStatusElements.forEach(function(statusElement) {
        var status = statusElement.dataset.status;
        switch(status) {
            case 'TODO':
                statusElement.classList.add('badge', 'badge-todo');
                break;
            case 'IN_PROGRESS':
                statusElement.classList.add('badge', 'badge-in-progress');
                break;
            case 'BLOCKED':
                statusElement.classList.add('badge', 'badge-blocked-task');
                break;
            case 'DONE':
                statusElement.classList.add('badge', 'badge-done');
                break;
        }
    });

    // Form validation
    var forms = document.querySelectorAll('.needs-validation');
    forms.forEach(function(form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });
});