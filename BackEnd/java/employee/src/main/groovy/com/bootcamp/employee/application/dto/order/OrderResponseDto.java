package com.bootcamp.employee.application.dto.order;

import com.bootcamp.employee.domain.model.order.Order;
import com.bootcamp.employee.domain.model.order.OrderStatus;
import lombok.Builder;

import java.time.LocalDateTime;
import java.util.List;
import java.util.stream.Collectors;

/**
 * 주문 응답 시 사용되는 메인 DTO(Data Transfer Object) 레코드입니다.
 * Order 도메인 엔티티의 모든 주요 정보를 클라이언트에 적합한 형태로 변환하여 제공합니다.
 * 주문 ID, 고객 정보, 주문 일시, 상태, 총 가격 및 포함된 모든 주문 항목을 포함합니다.
 */
@Builder
public record OrderResponseDto(
        Long orderId,           // 주문 ID
        Long customerId,        // 주문 고객 ID
        String customerName,    // 주문 고객 이름
        LocalDateTime orderDate,// 주문 일시
        OrderStatus status,     // 주문 상태
        int totalPrice,         // 총 주문 가격
        List<OrderItemResponseDto> items // 주문에 포함된 항목 리스트
) {
    /**
     * Order 엔티티로부터 OrderResponseDto를 생성하는 팩토리 메서드입니다.
     * Order 엔티티 및 연관된 Customer, OrderItem 정보를 DTO로 변환합니다.
     */
    public static OrderResponseDto fromEntity(Order order) {
        return OrderResponseDto.builder()
                .orderId(order.getId())
                .customerId(order.getCustomer().getId())
                .customerName(order.getCustomer().getName())
                .orderDate(order.getOrderDate())
                .status(order.getStatus())
                .totalPrice(order.getTotalPrice())
                .items(order.getOrderItems().stream()
                        .map(OrderItemResponseDto::fromEntity)
                        .collect(Collectors.toList()))
                .build();
    }
}
