document.addEventListener('DOMContentLoaded', function(){
    current_user = document.querySelector("h1").dataset.user
    instructorBox = document.querySelectorAll('.instructor_box')
    past_messages = document.querySelector('#past_messages2')
    instructorBox.forEach(element => {
        element.addEventListener("click", () => {
            let url = `ws://${window.location.host}/ws/socket-server/`
            const chatSocket = new WebSocket(url)
            chatSocket.onmessage = function(e){
                let data = JSON.parse(e.data)
                console.log('Data:', data)

                if(data.type === 'chat'){
                    let message_box = document.createElement('div')
                    // message_box.innerText = ${message}
                    // message_box.setAttribute("class", "my_message")
                    console.log(data.message)
                    if(data.sender == current_user){
                        past_messages.insertAdjacentHTML('beforeend', `<div class="my_message">
                                    ${data.message}</div>`)
                    }
                    else{
                        past_messages.insertAdjacentHTML('beforeend', `<div class="other_message">
                                    ${data.message}</div>`)
                    }
                }
            }

            sendTo = document.querySelector('h4')  
            sendTo.innerHTML = ""
            allInstructorNameTags = document.querySelectorAll('.instructor_name')
            allInstructorNameTags.forEach(element => {
                element.style.color = "black";
            })
            allInstructorBoxes = document.querySelectorAll('.instructor_box')
            allInstructorBoxes.forEach(element => {
                element.style.backgroundColor = 'white'
            })
            instructorNameTag = element.firstElementChild.lastElementChild
            instructorNameTag.style.color = "green";
            element.style.backgroundColor = "rgb(229, 224   , 224)"
            chatMessage = document.querySelector('#chat_message')
            chatMessage.style.display = "none"
            document.querySelector('#send_strip').style.display = "flex"
            document.querySelector('#chat_template').style.display = "block"
            sendTo.append(instructorNameTag.innerHTML)
            populateMessages(instructorNameTag.innerText, current_user, past_messages)
            instructor = sendTo.innerText
            document.querySelector(".send_img").addEventListener("click", () => {

                message_input = document.querySelector(".message_content")
                new_message = message_input.value
                console.log(new_message)
                create_message(new_message, instructor, past_messages)

                chatSocket.send(JSON.stringify({
                    'message': new_message,
                    'sender': current_user
                }))

                message_input.value = ""
            })
        })
    });
})

function populateMessages(user, current_user, past_messages){
    past_messages.innerHTML = ""
    fetch('/get_messages/' + user)
    .then(response => response.json())
    .then(messages => {
        console.log(messages)
        messages.forEach(message => {
            const message_box = document.createElement('div')
            message_box.innerText = message.value
            if (message.sender == current_user){
                message_box.setAttribute("class", "my_message")
            }
            else{
                message_box.setAttribute("class", "other_message")
            }
            past_messages.append(message_box)
        })
    })
}

function create_message(new_message, instructor, past_messages){
    fetch('/create_message', {
        method: 'POST',
        body: JSON.stringify({
            user: instructor,
            value: new_message
        })
    })
}