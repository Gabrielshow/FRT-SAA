$(document).ready(function() {
    $("#seatAssignmentForm").on("submit", function(event) {
        event.preventDefault();
        var formData = $(this).serialize();
        $.post("/run_saa", formData, function(data) {
            console.log(data);
            // Handle response here
            window.location.href = "/exam_hall";
        });
    });
});