document.addEventListener('DOMContentLoaded', function() {
   //обработчик кнопки для рассылок
   document.getElementById('delete-employee').addEventListener('click', function() {
      openModal();
   });

   //закрытие модального окна
   document.querySelector('.close').addEventListener('click', closeModal);
   document.getElementById('cancelDeleting').addEventListener('click', closeModal);

 
   //обработчик удаления
   document.getElementById('deleteEmployee').addEventListener('click', function() {
      deleteEmployee();
   });

   //открытие модального окна
   function openModal() {
      document.getElementById('deletingModal').style.display = 'block';
   }

   //закрытие модалки
   function closeModal() {
      document.getElementById('deletingModal').style.display = 'none';
   }

   async function deleteEmployee() {
      const employeeId = document.getElementById('delete-employee').value;

      const deleteBtn = document.getElementById('delete-employee');
      deleteBtn.disabled = true;
      //подготавливаем данные: айди сотрудника
      const requestData = {
         employee_id: parseInt(employeeId),
      };

      const response = await fetch(DELETE_EMPLOYEE_URL, {
         method: 'POST',
         headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
         },
         body: JSON.stringify(requestData)
      });
      
      if (response.ok){
         alert(`Сотрудник удален!`);
      } else {
         alert(`Ошибка удаления. Попробуйте снова`);
      }
      
      closeModal();
      deleteBtn.disabled = false;
      window.location.href = '/report/';
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
