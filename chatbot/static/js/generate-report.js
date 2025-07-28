document.addEventListener('DOMContentLoaded', function() {
      const currentUser = '{{ request.user.username }}';
      const filterCheckbox = document.getElementById('filter_own_employees');
      const selectAllCheckbox = document.getElementById('select_all');
      //получаем все строчки из таблицы
      const allRows = document.querySelectorAll('.employee-table tbody tr');
      //обработчик изменения состояния чекбокса
      filterCheckbox.addEventListener('change', filterRows);
      //галочка "только свои сотрудники"
      function filterRows() {
         //если была поставлена метка "только свои сотрудники"
         const showOnlyOwn = filterCheckbox.checked;
         allRows.forEach(row => {
            //если сотрудник в строке принадлежит куратору ставим true
            const isOwn = row.dataset.curator === currentUser;
            //если была поставлена метка и сотрудник не принадлежит куратору,
            // ставим display: none, если нет - ничего не меняем
            if (showOnlyOwn && !isOwn) {
               row.style.display = 'none';
               row.querySelector('.employee-checkbox').checked = false; //снимаем выделение
            } else {
               row.style.display = '';
            }
            if (showOnlyOwn && isOwn){
               row.querySelector('.employee-checkbox').checked = true; //выделяем 
            }
            if (!showOnlyOwn){
               row.querySelector('.employee-checkbox').checked = false; //снимаем выделение
            }
         });
         //отжимаем галочку 
         if (selectAllCheckbox.checked == true){
            selectAllCheckbox.checked = false;
            selectAll();
         }
         
      }

      selectAllCheckbox.addEventListener('change', selectAll);
      //галочка "выбрать все"
      function selectAll() {
         //если была поставлена метка "выбрать все"
         const showAll = selectAllCheckbox.checked;
         allRows.forEach(row => {
            //если была поставлена метка, выделяем все
            if (showAll) {
               row.querySelector('.employee-checkbox').checked = true; //выделяем 
            } else {
              row.querySelector('.employee-checkbox').checked = false; //иначе снимаем выделение везде   
            }
         });
         //отжимаем галочку 
         if (filterCheckbox.checked == true){
            filterCheckbox.checked = false;
            filterRows();
         }  
      }
      
      //обработка всех выпадающих списков с галочками
      document.querySelectorAll('.dropdown-toggle').forEach(function(toggle) {
         toggle.addEventListener('click', function(e) {
            e.stopPropagation(); //предотвращаем всплытие
            const menu = this.nextElementSibling;            
            //закрываем все другие открытые меню
            document.querySelectorAll('.dropdown-menu.show').forEach(function(openMenu) {
            if (openMenu !== menu) {
               openMenu.classList.remove('show');
            }
            });
            
            //переключаем текущее меню
            menu.classList.toggle('show');
            });
      });

         //закрытие при клике вне меню
         document.addEventListener('click', function() {
            document.querySelectorAll('.dropdown-menu.show').forEach(function(menu) {
               menu.classList.remove('show');
               //сбрасываем поиск
               const search = menu.querySelector('.search');
               if (search) {
                  search.value = '';
                  //триггерим событие input для обновления отображения
                  search.dispatchEvent(new Event('input'));
               }
            });
         });

         //предотвращаем закрытие при клике внутри меню
         document.querySelectorAll('.dropdown-menu').forEach(function(menu) {
            menu.addEventListener('click', function(e) {
               e.stopPropagation();
            });
         });
         const searches = document.querySelectorAll('input[class="search"], input[id$="-search"]');
         searches.forEach(input => {
         //функция поиска в выпадающем списке
            input.addEventListener('input', function() {
               var filter, items, i, txtValue;
               filter = input.value.toUpperCase();
               //получаем все элементы списка
               //находим родительское меню
               const dropdownMenu = this.closest('.dropdown-menu');
               // находим все элементы в текущем меню
               items = dropdownMenu.querySelectorAll('.dropdown-item');
               
               for (i = 0; i < items.length; i++) {
                  const filialNameElement = items[i].querySelector('.checkbox-container + span');
                  const filialName = filialNameElement ? filialNameElement.textContent.trim() : items[i].textContent.trim();
                  if (filialName.toUpperCase().includes(filter)) {
                        items[i].style.display = "";
                  } else {
                        items[i].style.display = "none";
                  }
               }
            });
         });
         //кнопка сброса
         document.querySelectorAll('.reset-button').forEach(function(button) {
            button.addEventListener('click', function(e) {
               e.preventDefault();
               e.stopPropagation();
               
               //находим родительское меню
               const dropdownMenu = this.closest('.dropdown-menu');
               
               //сбрасываем поиск
               const search = dropdownMenu.querySelector('.search');
               if (search) {
                  search.value = '';
                  //триггерим событие input для обновления отображения
                  search.dispatchEvent(new Event('input'));
               }
               
               //снимаем все галочки в этом меню
               dropdownMenu.querySelectorAll('input[type="checkbox"]').forEach(function(checkbox) {
                  checkbox.checked = false;
               });
            });
         });
         // Работа с календарями
         const hireDateFrom = $(".hireDateFrom");
         const hireDateTo = $(".hireDateTo");

         if (hireDateFrom.length) {
            new AirDatepicker(hireDateFrom[0], {
                  autoClose: true,
                  dateFormat: 'dd.MM.yyyy',
                  onSelect: function({formattedDate}) {
                     hireDateFrom.val(formattedDate);
                  }
            });
         }

         if (hireDateTo.length) {
            new AirDatepicker(hireDateTo[0], {
                  autoClose: true,
                  dateFormat: 'dd.MM.yyyy',
                  onSelect: function({formattedDate}) {
                     hireDateTo.val(formattedDate);
                  }
            });
         }
         const tgDateFrom = $(".tgDateFrom");
         const tgDateTo = $(".tgDateTo");

         if (tgDateFrom.length) {
            new AirDatepicker(tgDateFrom[0], {
                  autoClose: true,
                  dateFormat: 'dd.MM.yyyy',
                  onSelect: function({formattedDate}) {
                     tgDateFrom.val(formattedDate);
                  }
            });
         }

         if (tgDateTo.length) {
            new AirDatepicker(tgDateTo[0], {
                  autoClose: true,
                  dateFormat: 'dd.MM.yyyy',
                  onSelect: function({formattedDate}) {
                     tgDateTo.val(formattedDate);
                  }
            });
         }
});

