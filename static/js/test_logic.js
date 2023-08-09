$(document).ready(function () {
    $("#personality-test-form").submit(function (event) {
        event.preventDefault();

        // Validate that all questions have been answered
        var allQuestionsAnswered = true;
        $(".question").each(function() {
            var radioName = $(this).find(".response-input").attr("name");
            if (!$("input[name='" + radioName + "']:checked").length) {
                allQuestionsAnswered = false;
                return false; // Exit the loop early
            }
        });

        if (!allQuestionsAnswered) {
            alert("Please answer all questions before submitting.");
            return;
        }

        // Collect form data
        var formData = $(this).serializeArray();

        // Send form data to the server using AJAX
        $.post("", formData, function (response) {
            alert(response.msg)
            window.location.href = '/job-list';
        }, "json");
    });
});
