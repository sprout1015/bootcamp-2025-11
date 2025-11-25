package com.bootcamp.employee.infrastructure.persistence.order;

import com.bootcamp.employee.domain.model.order.Order;
import com.bootcamp.employee.domain.repository.order.OrderRepository;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;

/**
 * Order 도메인 리포지토리의 인프라스트럭처 계층 구현체입니다.
 * Spring Data JPA의 JpaRepository를 상속받아 Order 엔티티에 대한 실제 DB 접근 기능을 제공합니다.
 * 도메인 계층의 OrderRepository 인터페이스를 구현하여 인프라 구현이 도메인 계약을 따르도록 합니다.
 */
@Repository
public interface OrderJpaRepository extends JpaRepository<Order, Long>, OrderRepository {

    // Spring Data JPA의 명명 규칙에 따라 findByCustomerId 메서드가 자동으로 구현됩니다.
    // Order 엔티티의 customer 필드와 그 ID를 기반으로 쿼리가 생성됩니다.
    List<Order> findByCustomerId(Long customerId);

    /**
     * 특정 책 ID를 포함하는 모든 주문을 조회하는 커스텀 쿼리입니다.
     * Order 엔티티와 OrderItem 엔티티를 JOIN하여, OrderItem에 연결된 Book의 ID를 기준으로 검색합니다.
     * 이는 Order가 Book에 대한 직접적인 참조를 가지지 않고, OrderItem을 통해 간접적으로 연결되기 때문에 필요합니다.
     */
    @Query("SELECT o FROM Order o JOIN o.orderItems oi WHERE oi.book.id = :bookId")
    List<Order> findOrdersByBookId(@Param("bookId") Long bookId);
}
