package com.bootcamp.employee.application.dto.book;

import com.bootcamp.employee.domain.model.book.Book;
import lombok.Builder;

/**
 * Book 도메인을 위한 DTO (Data Transfer Object) 레코드입니다.
 * 애플리케이션 계층에서 데이터를 전달하는 역할을 하며, 도메인 모델의 내부 구조를
 * 외부 계층(예: Interfaces Layer)에 직접 노출하지 않도록 합니다.
 * 엔티티를 DTO로 변환하거나, DTO를 엔티티로 변환하는 헬퍼 메서드를 포함합니다.
 */
@Builder
public record BookDto(
    Long id,
    String bookName,
    String author,
    String publisher,
    String genre,
    Integer price,
    Integer stock
) {
    public static BookDto fromEntity(Book book) {
        return BookDto.builder()
                .id(book.getId())
                .bookName(book.getBookName())
                .author(book.getAuthor())
                .publisher(book.getPublisher())
                .genre(book.getGenre())
                .price(book.getPrice())
                .stock(book.getStock())
                .build();
    }

    public Book toEntity() {
        return Book.builder()
                .bookName(this.bookName)
                .author(this.author)
                .publisher(this.publisher)
                .genre(this.genre)
                .price(this.price)
                .stock(this.stock)
                .build();
    }
}
