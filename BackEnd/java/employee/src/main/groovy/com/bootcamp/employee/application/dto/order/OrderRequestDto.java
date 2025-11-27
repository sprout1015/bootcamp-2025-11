package com.bootcamp.employee.application.dto.order;

import java.util.List;

/**
 * 주문 생성 요청 시 사용되는 DTO(Data Transfer Object) 레코드입니다.
 * 클라이언트로부터 주문을 생성하는 데 필요한 고객 ID와 주문할 항목들(OrderItemRequestDto 리스트)을 받습니다.
 * 애플리케이션 계층으로의 깨끗하고 타입-안전한 데이터 전달을 용이하게 합니다.
 */
public record OrderRequestDto(
    Long customerId, // 주문을 요청하는 고객의 ID
    List<OrderItemRequestDto> items // 주문에 포함될 상품 목록
) {}
