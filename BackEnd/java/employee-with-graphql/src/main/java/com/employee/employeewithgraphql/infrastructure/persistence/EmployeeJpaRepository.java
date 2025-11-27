package com.employee.employeewithgraphql.infrastructure.persistence;

import com.employee.employeewithgraphql.domain.model.Employee;
import com.employee.employeewithgraphql.domain.repository.EmployeeRepository;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface EmployeeJpaRepository extends JpaRepository<Employee, Long>, EmployeeRepository {
}
