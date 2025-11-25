package com.bootcamp.employee.infrastructure.persistence.book;

import com.bootcamp.employee.domain.model.book.Book;
import com.bootcamp.employee.domain.repository.book.BookRepository;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

/**
 * Book 도메인 리포지토리의 인프라스트럭처 계층 구현체입니다.
 * Spring Data JPA의 JpaRepository를 상속받아 Book 엔티티에 대한 실제 DB 접근 기능을 제공합니다.
 * 도메인 계층의 BookRepository 인터페이스를 구현하여 인프라 구현이 도메인 계약을 따르도록 합니다.
 */
@Repository
public interface BookJpaRepository extends JpaRepository<Book, Long>, BookRepository {
}
