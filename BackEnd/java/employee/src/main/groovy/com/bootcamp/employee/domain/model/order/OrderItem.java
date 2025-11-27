package com.bootcamp.employee.domain.model.order;

import com.bootcamp.employee.domain.model.book.Book;
import jakarta.persistence.*;
import lombok.*;

/**
 * Order aggregate 내의 엔티티로, 단일 주문 항목을 나타냅니다.
 * 주문(Order)에 포함된 특정 책(Book)의 수량과 주문 당시 가격을 캡슐화합니다.
 * Order와 Book 엔티티와의 연관관계를 가집니다. 성능 최적화를 위해 FetchType.LAZY를 사용합니다.
 */
@Entity
@Table(name="order_items")
@Getter
@Builder
@AllArgsConstructor
@NoArgsConstructor(access = AccessLevel.PROTECTED)
public class OrderItem {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    // Order (주문) 엔티티와의 다대일(N:1) 관계. 지연 로딩을 사용합니다.
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "order_id")
    private Order order;

    // Book (책) 엔티티와의 다대일(N:1) 관계. 지연 로딩을 사용합니다.
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "book_id")
    private Book book;

    @Column(nullable = false)
    private Integer orderPrice; // 주문 당시의 가격 (가격 변동에 대비)

    @Column(nullable = false)
    private Integer quantity; // 주문 수량

    //== 연관관계 편의 메서드 ==//
    /**
     * OrderItem이 특정 Order에 속하도록 연관관계를 설정하는 편의 메서드.
     * 양방향 연관관계에서 일관성을 유지하는 데 사용됩니다.
     */
    public void setOrder(Order order) {
        this.order = order;
    }
}
