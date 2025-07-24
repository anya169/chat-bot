//создаем вебсокет
const employeeId = document.getElementById('employee-data').dataset.employeeId;
const chatSocket = new WebSocket(`ws://${window.location.host}/ws/chat/${employeeId}/`);
//при получении нового сообщения от сервера вызываем функцию
chatSocket.onmessage = function(e) {
   //преобразовываем объект json в строку
   const data = JSON.parse(e.data);
   //находим объект с сообщениями
   const messages = document.getElementById('chat-messages');
   
   //создаем объект и присваиваем ему класс в зависимости от того, кому принадлежит сообщение
   const messageDiv = document.createElement('div');
   messageDiv.className = data.sender_id === "{{ request.user.username }}" ? "message sent" : "message received";
   
   //создаем элемент
   messageDiv.innerHTML = `
      <p><strong>${data.sender_id === "{{ request.user.username }}" ? 'Вы:' : 'Сотрудник:'}</strong> ${data.message}</p>
      <small>${new Date().toLocaleString()}</small>
   `;
   
   //добавляем в структуру и прокручиваем экран
   messages.appendChild(messageDiv);
   messages.scrollTop = messages.scrollHeight;
};

//при нажатии кнопки 
document.getElementById('message-form').onsubmit = function(e) {
   e.preventDefault();
   const input = document.getElementById('message-input');
   //отправляем введенное сообщение и очищаем поле ввода
   chatSocket.send(JSON.stringify({
      'message': input.value,
      'sender_id': "{{ request.user.username }}"
   }));
   input.value = '';
};
