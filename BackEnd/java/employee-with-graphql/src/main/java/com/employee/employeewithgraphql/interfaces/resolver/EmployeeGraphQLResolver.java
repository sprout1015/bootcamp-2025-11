package com.employee.employeewithgraphql.interfaces.resolver;

import com.employee.employeewithgraphql.application.dto.EmployeeDto;
import com.employee.employeewithgraphql.application.service.EmployeeService;
import com.employee.employeewithgraphql.graphql.EmployeeInput;
import lombok.RequiredArgsConstructor;
import org.springframework.graphql.data.method.annotation.Argument;
import org.springframework.graphql.data.method.annotation.MutationMapping;
import org.springframework.graphql.data.method.annotation.QueryMapping;
import org.springframework.stereotype.Controller; // Use @Controller for GraphQL resolvers

import java.util.List;

@Controller
@RequiredArgsConstructor
public class EmployeeGraphQLResolver {
    private final EmployeeService employeeService; // Inject the application service

    @QueryMapping
    public List<EmployeeDto> getEmployeeList() { // Renamed from getEmployees to employees for schema consistency
        return employeeService.findAllEmployees();
    }

    @QueryMapping
    public EmployeeDto getEmployeeById(@Argument("id") Long id) { // Use @Argument for GraphQL ID
        return employeeService.findEmployeeById(id)
                .orElseThrow(() -> new RuntimeException("Employee not found with id: " + id));
    }

    @MutationMapping
    public EmployeeDto createEmployee(@Argument EmployeeInput input) {
        return employeeService.createEmployee(input);
    }

    @MutationMapping
    public EmployeeDto updateEmployee(@Argument Long id, @Argument EmployeeInput input) {
        return employeeService.updateEmployee(id, input);
    }

    @MutationMapping
    public boolean deleteEmployee(@Argument Long id) {
        return employeeService.deleteEmployee(id);
    }
}
