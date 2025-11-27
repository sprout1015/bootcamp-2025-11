package com.bootcamp.employee.application.dto.order;

import com.bootcamp.employee.domain.model.order.OrderItem;
import lombok.Builder;

/**
 * 주문 응답 시 사용되는 단일 주문 항목 DTO(Data Transfer Object) 레코드입니다.
 * 클라이언트에게 주문된 책의 상세 정보(ID, 이름)와 주문 당시 가격, 수량을 제공합니다.
 * 도메인 모델의 OrderItem 엔티티를 클라이언트에 적합한 형태로 변환하여 전달합니다.
 */
@Builder
public record OrderItemResponseDto(
        Long bookId,        // 주문된 책의 ID
        String bookName,    // 주문된 책의 이름
        int orderPrice,     // 주문 당시의 책 가격
        int quantity        // 주문 수량
) {
    /**
     * OrderItem 엔티티로부터 OrderItemResponseDto를 생성하는 팩토리 메서드입니다.
     * OrderItem 엔티티의 정보를 DTO로 변환하여 클라이언트에게 제공합니다.
     */
    public static OrderItemResponseDto fromEntity(OrderItem orderItem) {
        return OrderItemResponseDto.builder()
                .bookId(orderItem.getBook().getId())
                .bookName(orderItem.getBook().getBookName())
                .orderPrice(orderItem.getOrderPrice())
                .quantity(orderItem.getQuantity())
                .build();
    }
}
