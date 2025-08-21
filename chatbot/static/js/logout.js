function clearForm() {
   // Очищаем форму входа при выходе
   if (window.opener && !window.opener.closed) {
      try {
         const form = window.opener.document.getElementById('login-form');
         if (form) form.reset();
      } catch (e) {
         console.log('Не удалось очистить форму входа');
      }
   }
   
   // Также очищаем localStorage/sessionStorage
   localStorage.removeItem('authData');
   sessionStorage.clear();
}