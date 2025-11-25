package com.bootcamp.employee.interfaces.customer;

import com.bootcamp.employee.application.dto.customer.CustomerDto;
import com.bootcamp.employee.application.service.customer.CustomerService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.net.URI;
import java.util.List;

/**
 * Customer 도메인을 위한 인터페이스 계층의 REST 컨트롤러입니다.
 * 클라이언트의 HTTP 요청을 처리하고, 애플리케이션 서비스(CustomerService)를 통해
 * 비즈니스 로직을 호출하며, DTO를 사용하여 응답을 구성합니다.
 * 도메인 모델의 직접적인 노출을 방지하여 계층 간의 의존성을 분리합니다.
 */
@RestController
@RequestMapping("/api/customers")
@RequiredArgsConstructor
public class CustomerController {

    private final CustomerService customerService;

    @GetMapping
    public ResponseEntity<List<CustomerDto>> getAllCustomers() {
        return ResponseEntity.ok(customerService.findAllCustomers());
    }

    @GetMapping("/{id}")
    public ResponseEntity<CustomerDto> getCustomerById(@PathVariable("id") Long id) {
        return customerService.findCustomerById(id)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }

    @PostMapping
    public ResponseEntity<CustomerDto> createCustomer(@RequestBody CustomerDto customerDto) {
        try {
            var createdCustomer = customerService.createCustomer(customerDto);
            return ResponseEntity
                    .created(URI.create("/api/customers/" + createdCustomer.id()))
                    .body(createdCustomer);
        } catch (IllegalArgumentException e) {
            return ResponseEntity.badRequest().build(); // 이메일 중복 등의 비즈니스 예외 처리
        }
    }
}
