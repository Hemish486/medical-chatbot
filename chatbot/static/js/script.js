function escapeHtml(value) {
	return String(value)
		.replace(/&/g, "&amp;")
		.replace(/</g, "&lt;")
		.replace(/>/g, "&gt;")
		.replace(/\"/g, "&quot;")
		.replace(/'/g, "&#039;");
}

function formatMessage(value) {
	return escapeHtml(value).replace(/\n/g, "<br>");
}

function scrollToBottom() {
	var chatMessages = document.getElementById("chat-messages");
	if (chatMessages) {
		chatMessages.scrollTop = chatMessages.scrollHeight;
	}
}

var chatToggle = document.getElementById("chat-icon");
var chatWindow = document.getElementById("chat-window");

if (chatToggle && chatWindow) {
	chatToggle.addEventListener("click", function () {
		chatWindow.classList.toggle("is-open");
		if (chatWindow.classList.contains("is-open")) {
			scrollToBottom();
		}
	});
}

$(document).ready(function () {
	scrollToBottom();

	$("#chat-form").on("submit", function (event) {
		event.preventDefault();
		var userInput = ($("#chat-input").val() || "").trim();
		if (!userInput) {
			return;
		}

		$.ajax({
			type: "POST",
			url: "/",
			data: {
				user_input: userInput,
				csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
			},
			success: function (response) {
				$("#chat-messages").append(
					"<p class='user-question'>" + formatMessage(userInput) + "</p>"
				);
				$("#chat-messages").append(
					"<p class='chatbot-answer'>" + formatMessage(response.reply || "") + "</p>"
				);
				$("#chat-input").val("");
				scrollToBottom();
			},
			error: function (xhr) {
				var message = "Something went wrong. Please try again.";
				if (xhr.responseJSON && xhr.responseJSON.reply) {
					message = xhr.responseJSON.reply;
				}
				$("#chat-messages").append(
					"<p class='chatbot-answer'>" + formatMessage(message) + "</p>"
				);
				scrollToBottom();
			},
		});
	});
});
