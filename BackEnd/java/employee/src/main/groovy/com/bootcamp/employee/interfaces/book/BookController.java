package com.bootcamp.employee.interfaces.book;

import com.bootcamp.employee.application.dto.book.BookDto;
import com.bootcamp.employee.application.service.book.BookService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.net.URI;
import java.util.List;

/**
 * Book 도메인을 위한 인터페이스 계층의 REST 컨트롤러입니다.
 * 클라이언트의 HTTP 요청을 처리하고, 애플리케이션 서비스(BookService)를 통해
 * 비즈니스 로직을 호출하며, DTO를 사용하여 응답을 구성합니다.
 * 도메인 모델의 직접적인 노출을 방지하여 계층 간의 의존성을 분리합니다.
 */
@RestController
@RequestMapping("/api/books")
@RequiredArgsConstructor
public class BookController {

    private final BookService bookService;

    @GetMapping
    public ResponseEntity<List<BookDto>> getAllBooks() {
        return ResponseEntity.ok(bookService.findAllBooks());
    }

    @GetMapping("/{id}")
    public ResponseEntity<BookDto> getBookById(@PathVariable("id") Long id) {
        return bookService.findBookById(id)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }

    @PostMapping
    public ResponseEntity<BookDto> createBook(@RequestBody BookDto bookDto) {
        var createdBook = bookService.createBook(bookDto);
        return ResponseEntity
                .created(URI.create("/api/books/" + createdBook.id()))
                .body(createdBook);
    }
}
