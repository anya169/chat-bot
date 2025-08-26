document.addEventListener('DOMContentLoaded', function() {
      const filterCheckbox = document.getElementById('filter_own_employees');
      const selectAllCheckbox = document.getElementById('select_all');
      //обработчик изменения состояния чекбокса
      filterCheckbox.addEventListener('change', filterRows);
      //галочка "только свои сотрудники"
      function filterRows() {
         //если была поставлена метка "только свои сотрудники"
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

      //сброс чекбоксов
      document.getElementById('reset-filters').addEventListener('click', function() {
            
            document.getElementById('filter_own_employees').checked = false;
            document.getElementById('select_all').checked = false;
            
            //сброс выпадающих списков
            document.querySelectorAll('.dropdown-menu input[type="checkbox"]').forEach(cb => {
               cb.checked = false;
            });
            
            //сброс дат
            document.querySelector('.hireDateFrom').value = '';
            document.querySelector('.hireDateTo').value = '';
            document.querySelector('.tgDateFrom').value = '';
            document.querySelector('.tgDateTo').value = '';
            
            //запрос без фильтров
            updateEmployees();
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
               var filter, items, i;
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

         //кнопка сброса для выпадающих списков
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
               if (e.target.closest('#pollDropdown-menu')) {
                  return; // не обновляем таблицу при выборе опросов
               }
               updateEmployees();
            });
         });

         //кнопка сброса для дат
         document.querySelectorAll('.reset-date').forEach(function(button) {
            button.addEventListener('click', function(e) {
               e.preventDefault();
               e.stopPropagation();
               
               //находим родительское меню
               const dropdownMenu = this.closest('.dropdown-menu');
               
               //сбрасываем поля
               dropdownMenu.querySelectorAll('.date').forEach(function(input) {
                  input.value = '';
               });
               updateEmployees();
            });
         });
         
                  
         // Работа с календарями
         function initDatePickers() {
            const hireDateFrom = $(".hireDateFrom");
            const hireDateTo = $(".hireDateTo");
            const tgDateFrom = $(".tgDateFrom");
            const tgDateTo = $(".tgDateTo");

            if (hireDateFrom.length) {
               new AirDatepicker(hireDateFrom[0], {
                     autoClose: true,
                     dateFormat: 'dd.MM.yyyy',
                     onSelect: function({formattedDate}) {
                        hireDateFrom.val(formattedDate);
                        updateEmployees();
                     }
               });
            }

            if (hireDateTo.length) {
               new AirDatepicker(hireDateTo[0], {
                     autoClose: true,
                     dateFormat: 'dd.MM.yyyy',
                     onSelect: function({formattedDate}) {
                        hireDateTo.val(formattedDate);
                        updateEmployees();
                     }
               });
            }

            if (tgDateFrom.length) {
               new AirDatepicker(tgDateFrom[0], {
                     autoClose: true,
                     dateFormat: 'dd.MM.yyyy',
                     onSelect: function({formattedDate}) {
                        tgDateFrom.val(formattedDate);
                        updateEmployees();
                     }
               });
            }

            if (tgDateTo.length) {
               new AirDatepicker(tgDateTo[0], {
                     autoClose: true,
                     dateFormat: 'dd.MM.yyyy',
                     onSelect: function({formattedDate}) {
                        tgDateTo.val(formattedDate);
                        updateEmployees();
                     }
               });
            }
         }
         $(document).ready(function() {
            initDatePickers();
         });
         
         
         //обработчики изменений фильтров
         document.addEventListener('change', function(e) {
            if (e.target.closest('#pollDropdown-menu')) {
               return; // не обновляем таблицу при выборе опросов
            } 
            if (  
               e.target.matches('.dropdown-menu input[type="checkbox"]') || //чекбоксы в выпадающем списке
               e.target.matches('.employee-controls input[type="checkbox"]')  //чекбоксы только свои и выбрать всех
             
               ) {
               updateEmployees();
            }
         }); 

         //обновление списка сотрудников
         async function updateEmployees(page = 1) {
            //собираем параметры фильтрации по всем категориям
               const filters = {
                  name: getSelectedValues('nameDropdown'),
                  filial: getSelectedValues('filialDropdown'),
                  struct: getSelectedValues('structDropdown'),
                  numtab: getSelectedValues('numtabDropdown'),
                  hire_date_from: document.querySelector('.hireDateFrom').value,
                  hire_date_to: document.querySelector('.hireDateTo').value,
                  tg_date_from: document.querySelector('.tgDateFrom').value,
                  tg_date_to: document.querySelector('.tgDateTo').value,
                  curator:  getSelectedValues('curatorDropdown'),
                  all: selectAllCheckbox.checked,
                  own: filterCheckbox.checked,
                  page: page
               };

            try {
               // Отправляем запрос на сервер
               const response = await fetch(FILTER_EMPLOYEES_URL, {
                     method: 'POST',
                     headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken')
                     },
                     body: JSON.stringify(filters)
               });

               if (!response.ok) throw new Error('Ошибка сервера');
               
               const data = await response.json();
               
               //обновляем таблицу
               updateEmployeeTable(data.employees, data.is_filter, data.page_obj, data.page_range);
               
            } catch (error) {
               console.error('Ошибка при фильтрации:', error);
            }
         }

         //функция для получения выбранных значений
         function getSelectedValues(dropdownId) {
            const dropdown = document.getElementById(dropdownId);
            const menu = dropdown.nextElementSibling;
            return Array.from(menu.querySelectorAll('input[type="checkbox"]:checked'))
               .map(checkbox => checkbox.value);
         }
   

         //функция обновления таблицы
         function updateEmployeeTable(employees, is_filter, page_obj, page_range) {
            const tbody = document.querySelector('.employee-table tbody');
            tbody.innerHTML = ''; //очищаем таблицу
            
            if (employees.length === 0) {
               tbody.innerHTML = '<tr><td colspan="8">Нет сотрудников для отображения</td></tr>';
               return;
            }
            
            //заполняем таблицу новыми данными
            employees.forEach(employee => {
               const row = document.createElement('tr');
               
               row.innerHTML = `
                     <td>
                        <input type="checkbox" id="employee_${employee.id}" 
                              name="selected_employees" value="${employee.id}" 
                              class="employee-checkbox" ${is_filter ? 'checked' : ''}>
                        <label for="employee_${employee.id}"></label>
                     </td>
                     <td>
                        <a href="/employee/${employee.id}" class="personal">
                           ${employee.name}
                        </a>
                     </td>
                     <td>${employee.filial || '-'}</td>
                     <td>${employee.struct || '-'}</td>
                     <td>${employee.num_tab || '-'}</td>
                     <td>${employee.curator || '-'}</td>
                     <td>${employee.hire_date || '-'}</td>
                     <td>${employee.telegram_registration_date || '-'}</td>
               `;
               
               tbody.appendChild(row);
            });

            const pagination = document.querySelector('.pagination');
            pagination.innerHTML = '';
            
            if (page_obj.paginator.num_pages > 1) {
               if (page_obj.has_previous) {
                     pagination.innerHTML += `<a href="#" class="page-link" data-page="1">&laquo; Первая</a>`;
                     pagination.innerHTML += `<a href="#" class="page-link" data-page="${page_obj.previous_page_number}">Предыдущая</a>`;
               }
               
               page_range.forEach(page => {
                     if (page == page_obj.number) {
                        pagination.innerHTML += `<span class="current">${page}</span>`;
                     } else {
                        pagination.innerHTML += `<a href="#" class="page-link" data-page="${page}">${page}</a>`;
                     }
               });
               
               if (page_obj.has_next) {
                  pagination.innerHTML += `
               <a href="#" data-page="${page_obj.next_page_number}" class="page-link">Следующая</a>
               <a href="#" data-page="${page_obj.paginator.num_pages}" class="page-link">Последняя &raquo;</a>
                `;
               }
            }
         setupPaginationHandlers();
      }
      function setupPaginationHandlers() {
         document.querySelectorAll('.page-link').forEach(link => {
            link.removeEventListener('click', handlePageClick); 
            link.addEventListener('click', handlePageClick); 
         });
      }

      function handlePageClick(e) {
         e.preventDefault();
         const page = this.getAttribute('data-page');
         updateEmployees(page);
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


      document.getElementById('report-button').addEventListener('click', generateReport);

      //сбор отмеченных сотрудников
      function getSelectedEmployees() {
         return Array.from(document.querySelectorAll('.employee-checkbox:checked'))
            .map(checkbox => {
                  const id = Number(checkbox.value);
                  
                  return { id: id }; 
            })
            .filter(emp => emp !== null);  //удаляем некорректные записи
      }

      //отправка данных для отчета
      async function generateReport() {
         const selectedEmployees = getSelectedEmployees();
         const selectedPolls = getSelectedValues('pollDropdown');
         
         if (selectedEmployees.length === 0) {
            alert('Пожалуйста, выберите хотя бы одного сотрудника');
            return;
         }

         if (selectedPolls.length === 0) {
            alert('Пожалуйста, выберите хотя бы один опрос');
            return;
         }

         try {

            // Отправка данных на сервер
            const response = await fetch(GENERATE_REPORT_URL, {
                  method: 'POST',
                  headers: {
                     'Content-Type': 'application/json',
                     'X-CSRFToken': getCookie('csrftoken'),
                  },
                  body: JSON.stringify({
                     employees: selectedEmployees,
                     polls: selectedPolls
                  })
            });

            if (!response.ok) throw new Error('Ошибка сервера');
        
            const contentDisposition = response.headers.get('Content-Disposition');
            let filename = 'report.xlsx'; // значение по умолчанию

            if (contentDisposition) {
               const filenameMatch = contentDisposition.match(/filename="(.+)"/);
               if (filenameMatch && filenameMatch[1]) {
                  filename = filenameMatch[1];
               }
            }

            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = filename; // Используем имя файла из заголовка
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            window.URL.revokeObjectURL(url);
        
         } catch (error) {
            alert(error);
         }
      }
      //обработчик кнопки для рассылок
      document.getElementById('mailing-button').addEventListener('click', function() {
         openMailingModal();
      });

      //закрытие модального окна
      document.querySelector('.close').addEventListener('click', closeModal);
      document.getElementById('cancelMailing').addEventListener('click', closeModal);

      //обработчик выбора рассылки
      document.getElementById('mailingSelect').addEventListener('change', function() {
         const mailingId = this.value;
         const sendButton = document.getElementById('sendSelectedMailing');
         
         if (mailingId) {
            sendButton.disabled = false;
         } else {
            sendButton.disabled = true;
         }
      });

      //обработчик отправки рассылки
      document.getElementById('sendSelectedMailing').addEventListener('click', function() {
         sendMailingToSelectedEmployees();
      });

      //открытие модального окна
      function openMailingModal() {
         const selectedEmployees = getSelectedEmployees();
         
         //если никто не выбран
         if (selectedEmployees.length === 0) {
            alert('Пожалуйста, выберите хотя бы одного сотрудника');
            return;
         }
         document.getElementById('mailingModal').style.display = 'block';
         const countElement = document.getElementById('selected-count');
         countElement.textContent = `Выбрано сотрудников: ${selectedEmployees.length}`;
         loadMailings(); //загружаем список рассылок
      }

      //закрытие модалки
      function closeModal() {
         document.getElementById('mailingModal').style.display = 'none';
      }

      //загрузка списка рассылок
      async function loadMailings() {
         try {
            const response = await fetch(GET_MAILINGS_URL, {
               headers: {
                  'X-CSRFToken': getCookie('csrftoken')
               }
            });
            
            if (response.ok) {
               const mailings = await response.json();
               const select = document.getElementById('mailingSelect');
               
               //заполняем поля выпадающего списка
               select.innerHTML = '<option value="">-- Выберите рассылку --</option>';
               mailings.forEach(mailing => {
                  const option = document.createElement('option');
                  option.value = mailing.id;
                  option.textContent = `${mailing.tag}`;
                  select.appendChild(option);
               });
            }
         } catch (error) {
            console.error('Ошибка загрузки рассылок:', error);
         }
      }

      //отправка рассылки выбранным сотрудникам
      async function sendMailingToSelectedEmployees() {
         const mailingId = document.getElementById('mailingSelect').value;
         const selectedEmployees = getSelectedEmployees();

         if (!mailingId) {
            alert('Пожалуйста, выберите рассылку');
            return;
         }

         if (selectedEmployees.length === 0) {
            alert('Пожалуйста, выберите хотя бы одного сотрудника');
            return;
         }

         
         const sendBtn = document.getElementById('sendSelectedMailing');
         sendBtn.disabled = true;
         //подготавливаем данные: айди рассылки и айди выбранных сотрудников
         const requestData = {
            mailing_id: parseInt(mailingId),
            employee_ids: selectedEmployees.map(emp => parseInt(emp.id))
         };

         const response = await fetch(SEND_MAILINGS_URL, {
            method: 'POST',
            headers: {
               'Content-Type': 'application/json',
               'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify(requestData)
         });
         
         //выводим результат рассылки
         const result = await response.json();
         alert(`Рассылка отправлена! Успешно: ${result.success_count}, Не отправлено: ${result.error_count}`);
         closeModal();
         sendBtn.disabled = false;
      
      }
});

