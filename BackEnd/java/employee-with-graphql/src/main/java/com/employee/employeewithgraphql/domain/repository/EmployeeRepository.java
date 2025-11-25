package com.employee.employeewithgraphql.domain.repository;

import com.employee.employeewithgraphql.domain.model.Employee;
import java.util.List;
import java.util.Optional;

public interface EmployeeRepository {
    Employee save(Employee employee);
    <S extends Employee> List<S> saveAll(Iterable<S> entities);
    Optional<Employee> findById(Long id);
    List<Employee> findAll();
    void deleteById(Long id);
    long count();
}
