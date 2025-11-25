package com.bootcamp.employee.domain.model.customer;

import jakarta.persistence.*;
import lombok.*;

/**
 * Customer 엔티티는 DDD의 도메인 모델 역할을 합니다.
 * 시스템 내에서 고객의 정보를 캡슐화하며, 필요한 경우 고객과 관련된 비즈니스 로직을 포함할 수 있습니다.
 * Lombok의 @Getter, @Builder 등을 사용하여 JPA 엔티티로서의 요구사항과 코드의 간결성을 유지합니다.
 * JPA의 요구사항에 따라 protected 기본 생성자를 가집니다.
 */
@Entity
@Table(name="customers")
@Getter
@Builder
@AllArgsConstructor
@NoArgsConstructor(access = AccessLevel.PROTECTED)
public class Customer {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, length = 50)
    private String name;

    @Column(nullable = false, unique = true, length = 100)
    private String email;

    @Column(nullable = false)
    private String address;
}
