package com.bootcamp.employee.application.service.customer;

import com.bootcamp.employee.application.dto.customer.CustomerDto;
import com.bootcamp.employee.domain.repository.customer.CustomerRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;

/**
 * Customer 도메인을 위한 애플리케이션 서비스입니다.
 * 유스케이스를 구현하고 도메인 리포지토리와의 상호작용을 조정하며, 트랜잭션을 관리합니다.
 * DTO와 도메인 모델 간의 변환을 담당하며, 고객 생성 시 이메일 중복 검사와 같은
 * 애플리케이션 수준의 비즈니스 규칙을 적용합니다.
 */
@Service
@RequiredArgsConstructor
@Transactional(readOnly = true) // 읽기 전용 트랜잭션 기본 적용
public class CustomerService {

    private final CustomerRepository customerRepository;

    public List<CustomerDto> findAllCustomers() {
        return customerRepository.findAll().stream()
                .map(CustomerDto::fromEntity)
                .collect(Collectors.toList());
    }

    public Optional<CustomerDto> findCustomerById(Long id) {
        return customerRepository.findById(id)
                .map(CustomerDto::fromEntity);
    }

    @Transactional // 쓰기 작업에 대한 트랜잭션 적용
    public CustomerDto createCustomer(CustomerDto customerDto) {
        if (customerDto.id() != null) {
            throw new IllegalArgumentException("Customer to create cannot have an ID.");
        }
        // 이메일 중복 검사
        if (customerRepository.findByEmail(customerDto.email()).isPresent()) {
            throw new IllegalArgumentException("Customer with email " + customerDto.email() + " already exists.");
        }
        var customer = customerDto.toEntity();
        var savedCustomer = customerRepository.save(customer);
        return CustomerDto.fromEntity(savedCustomer);
    }
}
