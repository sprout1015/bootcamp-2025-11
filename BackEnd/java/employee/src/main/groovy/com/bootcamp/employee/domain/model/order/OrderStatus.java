package com.bootcamp.employee.domain.model.order;

/**
 * 주문의 상태를 나타내는 도메인 값 객체(Enum)입니다.
 * 주문의 생명 주기를 명확하게 표현하고, 각 상태에 따른 비즈니스 로직을 구현하는 데 사용됩니다.
 */
public enum OrderStatus {
    PENDING,        // 주문 대기 중
    PROCESSING,     // 처리 중
    COMPLETED,      // 완료됨
    CANCELLED       // 취소됨
}
