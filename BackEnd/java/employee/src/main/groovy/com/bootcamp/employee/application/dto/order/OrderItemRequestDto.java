package com.bootcamp.employee.application.dto.order;

/**
 * 주문 생성 요청 시 사용되는 단일 주문 항목 DTO(Data Transfer Object) 레코드입니다.
 * 클라이언트로부터 어떤 책(bookId)을 몇 개(quantity) 주문할 것인지에 대한 정보를 받습니다.
 * 애플리케이션 계층으로의 깨끗하고 타입-안전한 데이터 전달을 용이하게 합니다.
 */
public record OrderItemRequestDto(
    Long bookId,    // 주문할 책의 ID
    Integer quantity // 주문 수량
) {}
