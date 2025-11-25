package com.bootcamp.employee.domain.repository.user;

import com.bootcamp.employee.domain.model.user.User;
import java.util.Optional;
import java.util.List;

/**
 * User 도메인 리포지토리 인터페이스입니다.
 * 도메인 계층에서 영속성(Persistence) 메커니즘을 추상화하는 계약 역할을 합니다.
 * 특정 데이터베이스 기술(예: JPA)에 의존하지 않고, 도메인 모델에 필요한
 * 데이터 접근 기능을 정의합니다.
 * <p>
 * `saveAll` 메서드는 Spring Data JPA의 `CrudRepository`와의 시그니처 충돌을 피하기 위해
 * `<S extends User>` 형태의 제네릭 시그니처를 사용합니다.
 */
public interface UserRepository {
    User save(User user);
    <S extends User> List<S> saveAll(Iterable<S> entities);
    void deleteById(Long id);
    Optional<User> findById(Long id);
    List<User> findAll();
    Optional<User> findByUserName(String userName);
    long count();
}
