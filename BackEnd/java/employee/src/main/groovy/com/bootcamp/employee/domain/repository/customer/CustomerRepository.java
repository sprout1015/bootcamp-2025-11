package com.bootcamp.employee.domain.repository.customer;

import com.bootcamp.employee.domain.model.customer.Customer;
import java.util.Optional;
import java.util.List;

/**
 * Customer 도메인 리포지토리 인터페이스입니다.
 * 도메인 계층에서 영속성(Persistence) 메커니즘을 추상화하는 계약 역할을 합니다.
 * 특정 데이터베이스 기술(예: JPA)에 의존하지 않고, 도메인 모델에 필요한
 * 데이터 접근 기능을 정의합니다.
 */
public interface CustomerRepository {
    Customer save(Customer customer);
    <S extends Customer> List<S> saveAll(Iterable<S> entities);
    Optional<Customer> findById(Long id);
    List<Customer> findAll();
    Optional<Customer> findByEmail(String email);
    long count();
}
