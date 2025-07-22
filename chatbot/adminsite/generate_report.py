from openpyxl import load_workbook
from datetime import datetime
from openpyxl.styles import Font
from .models import *
from pathlib import Path

def generate_report(cur_curator_login):
   try:
      curator = Employee.objects.filter(login = cur_curator_login).first()
      
      #загружаем шаблон
      current_dir = Path(__file__).parent
      template_path = current_dir / 'report_template.xlsx'     
      wb = load_workbook(template_path)
      ws = wb.active

      #получаем текущее время и форматируем его
      current_datetime = datetime.now().strftime("%d.%m.%Y %H:%M")

      #получаем всех сотрудников куратора
      curators_employees = Employee.objects.filter(curator_login = cur_curator_login)

      #заполняем шапку
      ws["A1"] = ws["A1"].value.replace("{{ date }}", current_datetime)
      ws["A2"] = ws["A2"].value.replace("{{ curator_name }}", curator.name)
      ws["A3"] = ws["A3"].value.replace("{{ count }}", str(curators_employees.count()))
      
      #начинаем выводить информацию с 5 строки
      current_row = 5
      
      for employee in curators_employees:
         #заголовок таблицы сотрудника
         ws.cell(row=current_row, column=1, value=f"Сотрудник: {employee.name}").font = Font(bold=True)
         ws.cell(row=current_row, column=2, value=f"Филиал: {employee.filial}")
         current_row += 1
         
         #получаем все пройденные опросы сотрудника
         employees_polls = Poll.objects.filter(question__answer__login = employee.id).distinct()
         for employee_poll in employees_polls:
            #шапка таблицы 
            ws.cell(row=current_row, column=1, value=f"Опрос: {employee_poll.name}").font = Font(bold=True)
            current_row += 1
            
            #получаем все вопросы из опроса
            employees_questions = Question.objects.filter(poll_id = employee_poll.id)
            
            #заголовки таблицы
            ws.cell(row=current_row, column=2, value="Вопрос")
            ws.cell(row=current_row, column=3, value="Ответ")
            current_row += 1
            for employees_question in employees_questions:
               #находим ответ на вопрос
               question_answer = Answer.objects.filter(question_id = employees_question.id, login_id = employee.id).first()   
               #заполняем строку       
               ws.cell(row=current_row, column=1, value=current_row)
               ws.cell(row=current_row, column=2, value=employees_question.name)
               ws.cell(row=current_row, column=3, value=question_answer)
               current_row += 1
            
         current_row += 2  
         
      #сохранение отчета
      report_filename = f"report_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx"
      wb.save(report_filename)
      return report_filename
   
   except Exception as e:
      print(f"Ошибка при формировании отчета: {str(e)}")
      return None
   
