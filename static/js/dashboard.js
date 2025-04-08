document.addEventListener('DOMContentLoaded', function() {
    // Only load charts if user is on the dashboard page
    if (document.getElementById('projectStatusChart')) {
        initProjectStatusChart();
    }

    if (document.getElementById('taskCompletionChart')) {
        initTaskCompletionChart();
    } 
});

// Project Status Pie Chart
function initProjectStatusChart() {
    var ctx = document.getElementById('projectStatusChart').getContext('2d');

    // Fetch real data from API endpoint
    fetch('/api/project-status-data/')
        .then(function(response) {
            return response.json();
        })
        .then(function(data) {
            new Chart(ctx, {
                type: 'pie',
                data: {
                    labels: ['Not Started', 'On Track', 'At Risk', 'Blocked', 'Complete'],
                    datasets: [{
                        data: data.counts,
                        backgroundColor: [
                            '#6C757D', 
                            '#28A745',
                            '#FFC107',
                            '#DC3545',
                            '#17A2B8'
                        ],
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'bottom'
                        },
                        title: {
                            display: true,
                            text: 'Project Status Distribution'
                        }
                    }
                }
            });
        })
        .catch(function(error) {
            console.error('Error fetching project status data:', error);
            // Fallback to dummy data if fetch fails
            new Chart(ctx, {
                type: 'pie',
                data: {
                    labels: ['Not Started', 'On Track', 'At Risk', 'Blocked', 'Complete'],
                    datasets: [{
                        data: [2, 5, 1, 0, 3],
                        backgroundColor: [
                            '#6C757D', 
                            '#28A745', 
                            '#FFC107', 
                            '#DC3545', 
                            '#17A2B8' 
                        ],
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'bottom'
                        },
                        title: {
                            display: true,
                            text: 'Project Status Distribution'
                        }
                    }
                }
            });
        }); 
}


// Task Completion Line Chart
function initTaskCompletionChart() {
    var ctx = document.getElementById('taskCompletionChart').getContext('2d');

    fetch('/api/task-completion-data/')
    .then(function(response) {
        return response.json();
    })
    .then(function(data) {
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: data.dates, 
                datasets: [{
                    label: 'Task Completed',
                    data: data.completedCounts,
                    borderColor: '#3A77FF',
                    backgroundColor: 'rgba(58, 119, 255, 0.1)',
                    tension: 0.4,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            precision: 0
                        }
                    }
                },
                plugins: {
                    legend: {
                        display: true,
                        position: 'top'
                    },
                    title: {
                        display: true,
                        text: 'Task Completion'
                    }
                }
            }
        });
    })
    .catch(function(error) {
        console.error('Error fetching task completion data', error);
        // Fallback to dummy data if fetch fails
        var dates = [];
        var dummyData = [];

        // Generate last 7 days
        for (var i = 6; i >= 0; i--) {
            var date = new Date();
            date.setDate(date.getDate() - i);
            dates.push(date.toLocaleDateString('en-IE', { day: 'numeric', month: 'short'}));

            dummyData.push(Math.floor(Math.random() * 8) + 1);
        }

        new Chart(ctx, {
            type: 'line',
            data: {
                labels: dates, 
                datasets: [{
                    label: 'Task Completed',
                    data: dummyData,
                    borderColor: '#3A77FF',
                    backgroundColor: 'rgba(58, 119, 255, 0.1)',
                    tension: 0.4,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            precision: 0
                        }
                    }
                },
                plugins: {
                    legend: {
                        display: true,
                        position: 'top'
                    },
                    title: {
                        display: true,
                        text: 'Task Completion'
                    }
                }
            }
        });
    });
}
