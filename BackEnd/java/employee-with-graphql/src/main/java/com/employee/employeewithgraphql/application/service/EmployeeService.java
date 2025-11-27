package com.employee.employeewithgraphql.application.service;

import com.employee.employeewithgraphql.application.dto.EmployeeDto;
import com.employee.employeewithgraphql.domain.model.Employee;
import com.employee.employeewithgraphql.domain.repository.EmployeeRepository;
import com.employee.employeewithgraphql.graphql.EmployeeInput;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
@Transactional(readOnly = true)
public class EmployeeService {

    private final EmployeeRepository employeeRepository;

    public List<EmployeeDto> getEmployeeList() {
        return employeeRepository.findAll().stream()
                .map(EmployeeDto::fromEntity)
                .collect(Collectors.toList());
    }

    public Optional<EmployeeDto> getEmployeeById(Long id) {
        return employeeRepository.findById(id)
                .map(EmployeeDto::fromEntity);
    }

    @Transactional
    public EmployeeDto createEmployee(EmployeeInput input) {
        Employee employee = Employee.builder()
                .name(input.name())
                .age(input.age())
                .job(input.job())
                .language(input.language())
                .pay(input.pay())
                .build();
        Employee savedEmployee = employeeRepository.save(employee);
        return EmployeeDto.fromEntity(savedEmployee);
    }

    @Transactional
    public EmployeeDto updateEmployee(Long id, EmployeeInput input) {
        Employee employee = employeeRepository.findById(id)
                .orElseThrow(() -> new IllegalArgumentException("Employee not found with id: " + id));
        employee.update(input.name(), input.age(), input.job(), input.language(), input.pay());
        Employee updatedEmployee = employeeRepository.save(employee); // save for managed entity might not be strictly needed, but good practice
        return EmployeeDto.fromEntity(updatedEmployee);
    }

    @Transactional
    public Boolean deleteEmployee(Long id) {
        employeeRepository.findById(id)
                .orElseThrow(() -> new IllegalArgumentException("Employee not found with id: " + id));
        employeeRepository.deleteById(id);
        return true;
    }
}
