package com.bootcamp.employee.application.service.user;

import com.bootcamp.employee.application.dto.user.UserDto;
import com.bootcamp.employee.domain.model.user.User;
import com.bootcamp.employee.domain.repository.user.UserRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.stream.Collectors;

/**
 * User 도메인을 위한 애플리케이션 서비스입니다.
 * 유스케이스를 구현하고 도메인 리포지토리와의 상호작용을 조정하며, 트랜잭션을 관리합니다.
 * DTO와 도메인 모델 간의 변환을 담당하며, 사용자 생성 시 사용자 이름 중복 검사와 같은
 * 애플리케이션 수준의 비즈니스 규칙을 적용합니다.
 */
@Service
@RequiredArgsConstructor
@Transactional(readOnly = true) // 읽기 전용 트랜잭션 기본 적용
public class UserService {
    private final UserRepository userRepository;

    public List<UserDto> findAll(){
        return userRepository.findAll().stream()
                .map(UserDto::fromEntity)
                .collect(Collectors.toList());
    }

    @Transactional // 쓰기 작업에 대한 트랜잭션 적용
    public UserDto saveUser(UserDto userDto){
        // 사용자 이름 중복 검사
        if (userRepository.findByUserName(userDto.userName()).isPresent()) {
            throw new IllegalArgumentException("User with username " + userDto.userName() + " already exists.");
        }
        User user = userDto.toEntity();
        User savedUser = userRepository.save(user);
        return UserDto.fromEntity(savedUser);
    }

    public UserDto getUserByUserName(String userName){
        return userRepository.findByUserName(userName)
                .map(UserDto::fromEntity)
                .orElseThrow(() -> new RuntimeException("User not found with username: " + userName));
    }

    @Transactional // 삭제 작업에 대한 트랜잭션 적용
    public void deleteUser(Long id){
        userRepository.deleteById(id);
    }
}
