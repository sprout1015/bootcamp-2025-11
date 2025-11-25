package com.bootcamp.employee.domain.model.order;

import com.bootcamp.employee.domain.model.customer.Customer;
import jakarta.persistence.*;
import lombok.AccessLevel;
import lombok.Getter;
import lombok.NoArgsConstructor;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;

/**
 * Order 엔티티는 DDD(도메인 주도 설계)의 Aggregate Root 역할을 합니다.
 * 주문(Order)은 고객(Customer)과 주문 항목(OrderItem)들을 포함하는 하나의 일관된 단위로 관리됩니다.
 * 주문의 생성, 상태 변경, 가격 계산과 같은 핵심 비즈니스 로직을 캡슐화합니다.
 * JPA의 요구사항에 따라 protected 기본 생성자를 가집니다.
 */
@Entity
@Table(name = "orders")
@Getter
@NoArgsConstructor(access = AccessLevel.PROTECTED) // JPA를 위한 protected 기본 생성자
public class Order {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "order_id")
    private Long id;

    // Customer와의 ManyToOne 관계. Order는 특정 Customer에 속합니다.
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "customer_id")
    private Customer customer;

    // OrderItem들과의 OneToMany 관계. Order가 OrderItem들을 관리하며,
    // Order가 영속화될 때 OrderItem들도 함께 영속화되도록 CascadeType.ALL을 설정합니다.
    @OneToMany(mappedBy = "order", cascade = CascadeType.ALL)
    private List<OrderItem> orderItems = new ArrayList<>();

    private LocalDateTime orderDate; // 주문 일시

    @Enumerated(EnumType.STRING) // Enum 타입을 DB에 문자열로 저장
    private OrderStatus status; // 주문 상태

    //== 연관관계 편의 메서드 ==//
    /**
     * Customer와의 연관관계를 설정하는 편의 메서드.
     * Order 생성 시 Customer를 할당하는 데 사용됩니다.
     */
    public void setCustomer(Customer customer) {
        this.customer = customer;
    }

    /**
     * OrderItem을 주문에 추가하고 양방향 연관관계를 설정하는 편의 메서드.
     * Order가 OrderItem의 생명 주기를 관리하도록 합니다.
     */
    public void addOrderItem(OrderItem orderItem) {
        orderItems.add(orderItem);
        orderItem.setOrder(this); // OrderItem에도 Order 참조 설정 (양방향 연관관계 편의)
    }

    //== 생성 메서드 ==//
    /**
     * 주문을 생성하는 정적 팩토리 메서드입니다.
     * 도메인 규칙에 따라 Order 객체를 올바른 상태로 초기화합니다.
     * (예: 초기 상태 PENDING, 현재 시간으로 orderDate 설정)
     */
    public static Order createOrder(Customer customer, List<OrderItem> orderItems) {
        Order order = new Order();
        order.setCustomer(customer);
        for (OrderItem orderItem : orderItems) {
            order.addOrderItem(orderItem);
        }
        order.status = OrderStatus.PENDING; // 초기 주문 상태
        order.orderDate = LocalDateTime.now(); // 주문 생성 시각
        return order;
    }

    //== 비즈니스 로직 ==//
    /**
     * 주문을 취소하는 비즈니스 로직입니다.
     * 이미 완료된 주문은 취소할 수 없다는 도메인 규칙을 강제합니다.
     * 재고 원복 로직은 트랜잭션 경계가 필요한 OrderService에서 처리하는 것이 더 적합할 수 있습니다.
     */
    public void cancel() {
        if (status == OrderStatus.COMPLETED) {
            throw new IllegalStateException("이미 배송완료된 상품은 취소가 불가능합니다.");
        }
        this.status = OrderStatus.CANCELLED;
        // 재고 원복 로직은 OrderService에서 처리하는 것이 더 적합할 수 있음 (트랜잭션)
        // for (OrderItem orderItem : orderItems) {
        //     orderItem.getBook().increaseStock(orderItem.getQuantity());
        // }
    }

    /**
     * 주문의 총 가격을 계산하여 반환합니다.
     * 주문 항목들의 가격과 수량을 합산하여 계산합니다.
     */
    public int getTotalPrice() {
        return orderItems.stream()
                .mapToInt(oi -> oi.getOrderPrice() * oi.getQuantity())
                .sum();
    }
}
