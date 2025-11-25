package com.bootcamp.employee.interfaces.order;

import com.bootcamp.employee.application.dto.book.BookWithCustomersDto;
import com.bootcamp.employee.application.dto.order.OrderRequestDto;
import com.bootcamp.employee.application.dto.order.OrderResponseDto;
import com.bootcamp.employee.application.service.order.OrderService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.net.URI;
import java.util.List;

/**
 * Order 도메인을 위한 인터페이스 계층의 REST 컨트롤러입니다.
 * 클라이언트의 HTTP 요청을 처리하고, 애플리케이션 서비스(OrderService)를 통해
 * 비즈니스 로직을 호출하며, DTO를 사용하여 응답을 구성합니다.
 * 특히, 주문 조회 시 고객 ID나 책 ID에 따라 다른 형태의 응답을 제공하는
 * 유연한 API 디자인을 보여줍니다.
 */
@RestController
@RequestMapping("/api/orders")
@RequiredArgsConstructor
public class OrderController {

    private final OrderService orderService;

    /**
     * 새로운 주문을 생성합니다.
     * @param requestDto 주문 생성에 필요한 고객 ID와 주문 항목들을 포함하는 DTO
     * @return 생성된 주문 정보를 담은 ResponseEntity (201 Created)
     */
    @PostMapping
    public ResponseEntity<OrderResponseDto> createOrder(@RequestBody OrderRequestDto requestDto) {
        try {
            var createdOrder = orderService.createOrder(requestDto);
            return ResponseEntity
                    .created(URI.create("/api/orders/" + createdOrder.orderId()))
                    .body(createdOrder);
        } catch (IllegalArgumentException e) {
            // 비즈니스 로직에서 발생한 예외(예: 고객 없음, 재고 부족) 처리
            return ResponseEntity.badRequest().body(null); // 더 적절한 에러 응답 본문을 고려할 수 있습니다.
        }
    }

    /**
     * 특정 주문 ID로 주문 상세 정보를 조회합니다.
     * @param id 조회할 주문의 ID
     * @return 주문 정보를 담은 ResponseEntity (200 OK) 또는 404 Not Found
     */
    @GetMapping("/{id}")
    public ResponseEntity<OrderResponseDto> getOrderById(@PathVariable("id") Long id) {
        return orderService.findOrderById(id)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }

    /**
     * 다양한 조건(고객 ID, 책 ID)에 따라 주문 목록을 조회하거나, 모든 주문을 조회합니다.
     * 고객 ID가 주어지면 해당 고객의 주문 목록을, 책 ID가 주어지면 해당 책을 주문한 고객 정보와 책 정보를 반환합니다.
     * 두 파라미터 모두 없으면 모든 주문 목록을 반환합니다.
     * 반환 타입이 파라미터에 따라 달라지므로 ResponseEntity<?>를 사용합니다.
     * @param customerId (Optional) 조회할 고객의 ID
     * @param bookId (Optional) 조회할 책의 ID
     * @return 조건에 맞는 주문 목록 (List<OrderResponseDto>) 또는 책-고객 정보 (BookWithCustomersDto)
     */
    @GetMapping
    public ResponseEntity<?> getOrders(
            @RequestParam(name = "customerId", required = false) Long customerId,
            @RequestParam(name = "bookId", required = false) Long bookId
    ) {
        if (customerId != null) {
            return ResponseEntity.ok(orderService.findOrdersByCustomerId(customerId));
        }
        if (bookId != null) {
            // 사용자 요청에 따라 책 ID로 조회 시 응답 형태를 변경
            return ResponseEntity.ok(orderService.findBookWithCustomersWhoOrdered(bookId));
        }
        return ResponseEntity.ok(orderService.findAllOrders());
    }
}
