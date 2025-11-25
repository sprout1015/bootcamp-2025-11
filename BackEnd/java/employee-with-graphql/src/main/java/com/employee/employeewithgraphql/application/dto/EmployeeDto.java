package com.employee.employeewithgraphql.application.dto;

import com.employee.employeewithgraphql.domain.model.Employee;
import lombok.Builder;

@Builder
public record EmployeeDto(
    Long id,
    String name,
    int age,
    String job,
    String language,
    int pay
) {
    public static EmployeeDto fromEntity(Employee employee) {
        return EmployeeDto.builder()
                .id(employee.getId())
                .name(employee.getName())
                .age(employee.getAge())
                .job(employee.getJob())
                .language(employee.getLanguage())
                .pay(employee.getPay())
                .build();
    }

    // toEntity는 EmployeeInput에서 담당하므로 여기서는 필요하지 않습니다.
    // Employee 엔티티의 불변성을 유지하고, 생성은 EmployeeInput을 통해 담당하는 것이 GraphQL의 일반적인 접근 방식입니다.
}
