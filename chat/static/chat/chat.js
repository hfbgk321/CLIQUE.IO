document.querySelector("#chat-message-submit").onclick = function (e) {
    const messageInputDom = document.querySelector("#chat-message-input");
    const message = "{{user.first_name}}: " + messageInputDom.value;
    // element.scrollIntoView(false);
    chatSocket.send(
      JSON.stringify({
        message: message,
      })
    );
    console.log(chatBox.scrollHeight + "new message");
    messageInputDom.value = "";
  };