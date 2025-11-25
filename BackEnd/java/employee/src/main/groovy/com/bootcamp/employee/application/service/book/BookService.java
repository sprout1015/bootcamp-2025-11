package com.bootcamp.employee.application.service.book;

import com.bootcamp.employee.application.dto.book.BookDto;
import com.bootcamp.employee.domain.repository.book.BookRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;

/**
 * Book 도메인을 위한 애플리케이션 서비스입니다.
 * 유스케이스를 구현하고 도메인 리포지토리와의 상호작용을 조정하며, 트랜잭션을 관리합니다.
 * DTO와 도메인 모델 간의 변환을 담당합니다.
 */
@Slf4j // 롬복을 사용한 SLF4J 로거 자동 생성
@Service
@RequiredArgsConstructor
@Transactional(readOnly = true) // 읽기 전용 트랜잭션 기본 적용
public class BookService {

    private final BookRepository bookRepository;

    public List<BookDto> findAllBooks() {
        return bookRepository.findAll().stream()
                .map(BookDto::fromEntity)
                .collect(Collectors.toList());
    }

    public Optional<BookDto> findBookById(Long id) {
        // 단일 책 조회 시 500 에러 트러블슈팅을 위해 임시로 추가된 로그 및 예외 처리입니다.
        // 문제 해결 후 제거해야 합니다.
        try {
            return bookRepository.findById(id)
                    .map(BookDto::fromEntity);
        } catch (Exception e) {
            log.error("Error finding book by id: {}", id, e);
            throw e; // 트랜잭션 롤백 및 500 에러 발생을 보장하기 위해 예외를 다시 던집니다.
        }
    }

    @Transactional // 쓰기 작업에 대한 트랜잭션 적용
    public BookDto createBook(BookDto bookDto) {
        if (bookDto.id() != null) {
            throw new IllegalArgumentException("Book to create cannot have an ID.");
        }
        var book = bookDto.toEntity();
        var savedBook = bookRepository.save(book);
        return BookDto.fromEntity(savedBook);
    }
}
