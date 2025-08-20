document.addEventListener('DOMContentLoaded', function() {
   const deleteButton = document.getElementById('delete-mailing');
      //обработчик нажатия кнопки удаления
      deleteButton.addEventListener('click', deleteMailing);
      async function deleteMailing() {
         const mailingId = document.querySelector('.employees-panel').id;
         //отправляем айди на сервер
            const response = await fetch(DELETE_URL, {
               method: 'POST',
               headers: {
                  'Content-Type': 'application/json',
                  'X-CSRFToken': getCookie('csrftoken')
               },
               body: JSON.stringify(mailingId)
            });
            if (response.ok) {
               const result = await response.json();
               if (result.success) {
                  alert('Рассылка успешно удалена!');
                  window.location.href = '/mailings/'; //перенаправляем на список рассылок
               } else {
                  alert('Ошибка при удалении');
               }
            } else {
               throw new Error('Ошибка сервера: ' + response.status);
            }
      }
      function getCookie(name) {
         let cookieValue = null;
         if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                  const cookie = cookies[i].trim();
                  if (cookie.substring(0, name.length + 1) === (name + '=')) {
                     cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                     break;
                  }
            }
         }
         return cookieValue;
      }   
});