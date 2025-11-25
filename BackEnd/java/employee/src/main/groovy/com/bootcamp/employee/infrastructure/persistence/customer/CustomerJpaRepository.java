package com.bootcamp.employee.infrastructure.persistence.customer;

import com.bootcamp.employee.domain.model.customer.Customer;
import com.bootcamp.employee.domain.repository.customer.CustomerRepository;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

/**
 * Customer 도메인 리포지토리의 인프라스트럭처 계층 구현체입니다.
 * Spring Data JPA의 JpaRepository를 상속받아 Customer 엔티티에 대한 실제 DB 접근 기능을 제공합니다.
 * 도메인 계층의 CustomerRepository 인터페이스를 구현하여 인프라 구현이 도메인 계약을 따르도록 합니다.
 */
@Repository
public interface CustomerJpaRepository extends JpaRepository<Customer, Long>, CustomerRepository {
    // Spring Data JPA의 명명 규칙에 따라 CustomerRepository 인터페이스의 findByEmail 메서드가 자동으로 구현됩니다.
    // 추가적인 쿼리 구현 없이 선언만으로 작동합니다.
}
