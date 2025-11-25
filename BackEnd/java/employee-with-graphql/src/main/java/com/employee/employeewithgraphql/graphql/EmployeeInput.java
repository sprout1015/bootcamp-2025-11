package com.employee.employeewithgraphql.graphql;

public record EmployeeInput (
    String name,
    int age,
    String job,
    String language,
    int pay
) {}