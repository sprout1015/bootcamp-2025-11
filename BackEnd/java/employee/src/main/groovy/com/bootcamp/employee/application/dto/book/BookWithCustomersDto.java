package com.bootcamp.employee.application.dto.book;

import com.bootcamp.employee.application.dto.customer.CustomerDto;
import lombok.Builder;

import java.util.List;

/**
 * 특정 사용 사례(어떤 책을 주문한 고객 목록 조회)를 위해 설계된 특수 DTO입니다.
 * 책의 상세 정보와 해당 책을 주문한 고객들의 목록을 함께 캡슐화하여 반환합니다.
 * API 응답의 유연성을 보여주며, 도메인 주도 설계 내에서 특정 쿼리 요구사항을 충족시키기 위해 사용됩니다.
 */
@Builder
public record BookWithCustomersDto(
    Long id,
    String bookName,
    String author,
    String publisher,
    String genre,
    Integer price,
    List<CustomerDto> customersWhoOrdered
) {}
