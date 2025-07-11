import React, { useState, useEffect } from 'react';

function EmployeeList() {
  const [employees, setEmployees] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('http://localhost:8000/young_employees/') 
      .then(response => response.json())
      .then(data => {
        setEmployees(data);
        setLoading(false);
      })
      .catch(error => {
        console.error('Error:', error);
        setLoading(false);
      });
  }, []);

  if (loading) return <div>Loading...</div>;

  return (
    <div>
      <h1>Список молодых сотрудников</h1>
      <ul>
        {employees.map(employee => (
          <li key={employee.service_number}>
            {employee.surname} {employee.name} - {employee.department.name}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default EmployeeList;