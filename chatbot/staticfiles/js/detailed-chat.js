document.querySelectorAll('.answer-form').forEach(form => {
   form.addEventListener('submit', function(e) {
      e.preventDefault();
      
      const formData = new FormData(this);
      const questionId = this.closest('.chat-container').id.split('-')[1];
      
      fetch(this.action, {
         method: 'POST',
         body: formData,
         headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': formData.get('csrfmiddlewaretoken')
         }
      })
      .then(response => response.json())
      .then(data => {
         if (data.success) {
            //создаем элемент с ответом
            const answerDiv = document.createElement('div');
            answerDiv.className = 'message sent';
            answerDiv.innerHTML = `
               <p><strong>Вы:</strong> ${formData.get('answer')}</p>
               <small>${new Date().toLocaleString()}</small>
            `;
            
            //вставляем ответ перед полем ввода
            this.closest('.chat__messages').insertBefore(
               answerDiv, 
               document.getElementById(`input-${questionId}`)
            );
            
            //скрываем поле ввода, больше куратор ответить не может
            document.getElementById(`input-${questionId}`).classList.add('hidden');
         }
      })
      .catch(error => console.error('Error:', error));
   });
});