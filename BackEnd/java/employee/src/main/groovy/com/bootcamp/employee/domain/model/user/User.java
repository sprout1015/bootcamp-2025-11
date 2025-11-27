package com.bootcamp.employee.domain.model.user;

import jakarta.persistence.*;
import lombok.*;

/**
 * User 엔티티는 DDD의 도메인 모델 역할을 합니다.
 * 시스템 사용자의 정보를 캡슐화하며, 계층 구조 리팩토링 과정에서 DDD 아키텍처에 맞게 재구성되었습니다.
 * Lombok의 @Getter, @Builder 등을 사용하여 JPA 엔티티로서의 요구사항과 코드의 간결성을 유지합니다.
 * JPA의 요구사항에 따라 protected 기본 생성자를 가집니다.
 * userName 필드는 고유(unique)해야 합니다.
 */
@Entity
@Table(name="users")
@Getter
@Builder
@AllArgsConstructor
@NoArgsConstructor(access = AccessLevel.PROTECTED)
public class User {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name="user_name", nullable = false, length = 50, unique=true)
    private String userName;

    @Column(nullable = false)
    private Integer age;

    @Column(name="job", nullable = true, length = 100)
    private String job;

    @Column(name="language", nullable = true, length = 100)
    private String language;

    @Column(name="pay", nullable = true)
    private Integer pay;
}
