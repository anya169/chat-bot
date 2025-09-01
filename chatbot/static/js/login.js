// Функция для очистки формы при загрузке страницы
function clearFormOnLoad() {
   const urlParams = new URLSearchParams(window.location.search);
   if (urlParams.has('logout')) {
      document.getElementById('login-form').reset();
   }
}

// Функция для очистки формы при клике на кнопку выхода
function clearForm() {
   document.getElementById('login-form').reset();
}
