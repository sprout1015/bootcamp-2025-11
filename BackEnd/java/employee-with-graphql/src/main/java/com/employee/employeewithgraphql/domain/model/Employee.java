package com.employee.employeewithgraphql.domain.model;

import jakarta.persistence.*;
import lombok.*;

/**
 * Employee 엔티티는 DDD(도메인 주도 설계)의 도메인 모델 역할을 합니다.
 * Lombok의 @Getter, @Builder 등을 사용하여 JPA 엔티티로서의 안정성과 DDD 원칙(행위 캡슐화)을 유지합니다.
 * @Setter는 엔티티의 직접적인 외부 수정을 방지하고, 비즈니스 로직을 통해 상태 변경을 유도합니다.
 * JPA의 요구사항에 따라 protected 기본 생성자를 가집니다.
 */
@Entity
@Table(name = "employees")
@Getter
@Builder
@AllArgsConstructor
@NoArgsConstructor(access = AccessLevel.PROTECTED)
public class Employee {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private String name;
    @Column(nullable = false)
    private int age;
    @Column(nullable = false)
    private String job;
    @Column(nullable = false)
    private String language;
    @Column(nullable = false)
    private int pay;

    /**
     * 직원 정보를 업데이트하는 비즈니스 로직입니다.
     * 엔티티 스스로 자신의 상태를 변경하도록 캡슐화합니다.
     * @param name 이름
     * @param age 나이
     * @param job 직업
     * @param language 언어
     * @param pay 급여
     */
    public void update(String name, int age, String job, String language, int pay) {
        this.name = name;
        this.age = age;
        this.job = job;
        this.language = language;
        this.pay = pay;
    }
}