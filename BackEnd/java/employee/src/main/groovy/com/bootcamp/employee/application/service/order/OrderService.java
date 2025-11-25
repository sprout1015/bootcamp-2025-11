package com.bootcamp.employee.application.service.order;

import com.bootcamp.employee.application.dto.book.BookWithCustomersDto;
import com.bootcamp.employee.application.dto.customer.CustomerDto;
import com.bootcamp.employee.application.dto.order.OrderRequestDto;
import com.bootcamp.employee.application.dto.order.OrderResponseDto;
import com.bootcamp.employee.domain.model.book.Book;
import com.bootcamp.employee.domain.model.customer.Customer;
import com.bootcamp.employee.domain.model.order.Order;
import com.bootcamp.employee.domain.model.order.OrderItem;
import com.bootcamp.employee.domain.repository.book.BookRepository;
import com.bootcamp.employee.domain.repository.customer.CustomerRepository;
import com.bootcamp.employee.domain.repository.order.OrderRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Optional;
import java.util.Set;
import java.util.stream.Collectors;

/**
 * Order 도메인을 위한 애플리케이션 서비스입니다.
 * 주문 생성과 조회에 관련된 복잡한 비즈니스 로직을 오케스트레이션합니다.
 * 트랜잭션 경계 내에서 고객, 책 리포지토리와의 상호작용을 조정하며,
 * 도메인 모델의 비즈니스 규칙(예: 재고 감소)을 호출합니다.
 * DTO와 도메인 모델 간의 변환을 담당합니다.
 */
@Service
@RequiredArgsConstructor
@Transactional(readOnly = true) // 읽기 전용 트랜잭션 기본 적용
public class OrderService {

    private final OrderRepository orderRepository;
    private final CustomerRepository customerRepository;
    private final BookRepository bookRepository;

    /**
     * 새로운 주문을 생성하는 유스케이스를 처리합니다.
     * 고객 조회, 책 재고 확인 및 감소, 주문 항목 생성, 주문 엔티티 생성 및 저장을
     * 단일 트랜잭션으로 묶어 비즈니스 일관성을 보장합니다.
     */
    @Transactional // 쓰기 작업에 대한 트랜잭션 적용
    public OrderResponseDto createOrder(OrderRequestDto requestDto) {
        // 1. 고객 조회
        Customer customer = customerRepository.findById(requestDto.customerId())
                .orElseThrow(() -> new IllegalArgumentException("Customer not found with id: " + requestDto.customerId()));

        // 2. 주문 상품(OrderItem) 목록 생성
        List<OrderItem> orderItems = new ArrayList<>();
        for (var itemDto : requestDto.items()) {
            Book book = bookRepository.findById(itemDto.bookId())
                    .orElseThrow(() -> new IllegalArgumentException("Book not found with id: " + itemDto.bookId()));

            // 재고 감소: Book 도메인 엔티티 내의 비즈니스 로직 호출
            book.decreaseStock(itemDto.quantity());

            // 주문 상품 생성
            OrderItem orderItem = OrderItem.builder()
                    .book(book)
                    .orderPrice(book.getPrice()) // 주문 당시 가격으로 고정
                    .quantity(itemDto.quantity())
                    .build();
            orderItems.add(orderItem);
        }

        // 3. 주문 생성: Order 도메인 엔티티의 팩토리 메서드 호출
        Order order = Order.createOrder(customer, orderItems);

        // 4. 주문 저장
        Order savedOrder = orderRepository.save(order);

        // 5. DTO로 변환하여 반환
        return OrderResponseDto.fromEntity(savedOrder);
    }

    /**
     * ID를 통해 단일 주문을 조회합니다.
     */
    public Optional<OrderResponseDto> findOrderById(Long id) {
        return orderRepository.findById(id)
                .map(OrderResponseDto::fromEntity);
    }

    /**
     * 모든 주문 목록을 조회합니다.
     */
    public List<OrderResponseDto> findAllOrders() {
        return orderRepository.findAll().stream()
                .map(OrderResponseDto::fromEntity)
                .collect(Collectors.toList());
    }

    /**
     * 특정 고객 ID로 모든 주문 목록을 조회합니다.
     */
    public List<OrderResponseDto> findOrdersByCustomerId(Long customerId) {
        return orderRepository.findByCustomerId(customerId).stream()
                .map(OrderResponseDto::fromEntity)
                .collect(Collectors.toList());
    }

    /**
     * 특정 책을 주문한 고객 정보와 함께 책 정보를 조회합니다.
     * 이는 책 중심의 역방향 조회 요청에 대한 응답을 제공하기 위해 구현되었습니다.
     */
    public BookWithCustomersDto findBookWithCustomersWhoOrdered(Long bookId) {
        // 1. 책 정보 조회
        Book book = bookRepository.findById(bookId)
                .orElseThrow(() -> new IllegalArgumentException("Book not found with id: " + bookId));

        // 2. 해당 책이 포함된 모든 주문 조회
        List<Order> orders = orderRepository.findOrdersByBookId(bookId);

        // 3. 주문들로부터 유니크한 고객 정보 추출
        Set<Customer> uniqueCustomers = new HashSet<>();
        for (Order order : orders) {
            uniqueCustomers.add(order.getCustomer());
        }

        // 4. 고객 엔티티를 DTO로 변환
        List<CustomerDto> customerDtos = uniqueCustomers.stream()
                .map(CustomerDto::fromEntity)
                .collect(Collectors.toList());

        // 5. BookWithCustomersDto 빌드 및 반환
        return BookWithCustomersDto.builder()
                .id(book.getId())
                .bookName(book.getBookName())
                .author(book.getAuthor())
                .publisher(book.getPublisher())
                .genre(book.getGenre())
                .price(book.getPrice())
                .customersWhoOrdered(customerDtos)
                .build();
    }
}
