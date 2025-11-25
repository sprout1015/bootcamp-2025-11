package com.bootcamp.employee.domain.model.book;

import jakarta.persistence.*;
import lombok.*;

/**
 * Book 엔티티는 DDD(도메인 주도 설계)의 도메인 모델 역할을 합니다.
 * 단순히 데이터를 저장하는 것을 넘어, 재고 관리와 같은 핵심 비즈니스 로직을 스스로 캡슐화합니다.
 * Lombok의 @Data 대신 @Getter, @Builder 등을 사용하여 JPA 엔티티로서의 안정성과 DDD 원칙(행위 캡슐화)을 유지합니다.
 * JPA의 요구사항에 따라 protected 기본 생성자를 가집니다.
 */
@Entity
@Table(name="books")
@Getter
@Builder
@AllArgsConstructor
@NoArgsConstructor(access = AccessLevel.PROTECTED)
public class Book {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name="book_name", nullable = false, length = 100)
    private String bookName;

    @Column(name="author", nullable = false, length = 50)
    private String author;

    @Column(name="publisher", nullable = false, length = 30)
    private String publisher;

    @Column(name="genre", nullable = false, length = 30)
    private Integer price;

    @Column(nullable = false)
    private Integer stock;

    /**
     * 책의 재고를 감소시키는 비즈니스 로직입니다.
     * 재고 부족 시 예외를 발생시켜 도메인 규칙을 강제합니다.
     */
    public void decreaseStock(int quantity) {
        if (this.stock < quantity) {
            throw new IllegalArgumentException("Not enough stock available.");
        }
        this.stock -= quantity;
    }
}
