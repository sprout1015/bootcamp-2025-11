package com.bootcamp.employee;

import com.bootcamp.employee.domain.model.book.Book;
import com.bootcamp.employee.domain.model.customer.Customer;
import com.bootcamp.employee.domain.model.user.User;
import com.bootcamp.employee.domain.repository.book.BookRepository;
import com.bootcamp.employee.domain.repository.customer.CustomerRepository;
import com.bootcamp.employee.domain.repository.user.UserRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

/**
 * 애플리케이션 시작 시 데이터베이스를 초기 더미 데이터로 채우는 컴포넌트입니다.
 * 개발 및 테스트 환경에서 애플리케이션을 빠르게 시작하고 기능을 테스트할 수 있도록 돕습니다.
 * `CommandLineRunner` 인터페이스를 구현하여 Spring 컨텍스트 로드 완료 후 특정 코드를 실행합니다.
 */
@Component
@RequiredArgsConstructor
public class DataInitializer implements CommandLineRunner {

    private final UserRepository userRepository;
    private final CustomerRepository customerRepository;
    private final BookRepository bookRepository;

    @Override
    @Transactional // 데이터 변경 작업이므로 트랜잭션 내에서 실행
    public void run(String... args) throws Exception {
        // 데이터가 이미 존재하면 중복 삽입을 방지하기 위해 초기화를 건너뜁니다.
        // User는 일반적으로 기초 엔티티이므로, User 테이블이 비어있는지 확인합니다.
        if (userRepository.count() > 0) {
            return;
        }

        // 유저 더미 데이터 생성
        User user1 = User.builder().userName("admin").age(30).job("developer").language("java").pay(5000).build();
        User user2 = User.builder().userName("tester").age(25).job("qa").language("python").pay(4000).build();
        userRepository.saveAll(List.of(user1, user2));

        // 고객 더미 데이터 생성
        Customer customer1 = Customer.builder().name("John Doe").email("john.doe@example.com").address("123 Main St, Anytown").build();
        Customer customer2 = Customer.builder().name("Jane Smith").email("jane.smith@example.com").address("456 Oak Ave, Sometown").build();
        customerRepository.saveAll(List.of(customer1, customer2));

        // 책 더미 데이터 생성
        Book book1 = Book.builder().bookName("The Lord of the Rings").author("J.R.R. Tolkien").publisher("Allen & Unwin").genre("Fantasy").price(25).stock(100).build();
        Book book2 = Book.builder().bookName("Pride and Prejudice").author("Jane Austen").publisher("T. Egerton").genre("Romance").price(15).stock(50).build();
        Book book3 = Book.builder().bookName("1984").author("George Orwell").publisher("Secker & Warburg").genre("Dystopian").price(20).stock(75).build();
        Book book4 = Book.builder().bookName("To Kill a Mockingbird").author("Harper Lee").publisher("J. B. Lippincott & Co.").genre("Fiction").price(18).stock(60).build();
        Book book5 = Book.builder().bookName("The Great Gatsby").author("F. Scott Fitzgerald").publisher("Charles Scribner's Sons").genre("Fiction").price(17).stock(80).build();
        bookRepository.saveAll(List.of(book1, book2, book3, book4, book5));
    }
}
