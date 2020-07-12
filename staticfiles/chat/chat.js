const friend = document.querySelectorAll('.singularfriend');
console.log(friend);
for (let i = 0; i < friend.length; i++){
    friend[i].addEventListener('click', function () {
        for (let i = 0; i < friend.length; i++){
            friend[i].classList.remove('selected');
        }
        friend[i].classList.add('selected'); 
    })
}

  const button = document.querySelector('#emoji-button');
  const picker = new EmojiButton();

  picker.on('emoji', emoji => {
    document.querySelector('#chat-message-input').value += emoji;
  });

button.addEventListener('click', () => {
    picker.togglePicker(button);
});
