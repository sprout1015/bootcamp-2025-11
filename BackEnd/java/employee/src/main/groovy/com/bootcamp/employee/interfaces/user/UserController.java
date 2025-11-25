package com.bootcamp.employee.interfaces.user;

import com.bootcamp.employee.application.dto.user.UserDto;
import com.bootcamp.employee.application.service.user.UserService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.net.URI;
import java.util.List;

/**
 * User 도메인을 위한 인터페이스 계층의 REST 컨트롤러입니다.
 * 클라이언트의 HTTP 요청을 처리하고, 애플리케이션 서비스(UserService)를 통해
 * 비즈니스 로직을 호출하며, DTO를 사용하여 응답을 구성합니다.
 * 도메인 모델의 직접적인 노출을 방지하여 계층 간의 의존성을 분리합니다.
 */
@RestController
@RequiredArgsConstructor
@RequestMapping("/api/users")
public class UserController {
    private final UserService userService;

    /**
     * 새로운 사용자를 생성합니다.
     * @param userDto 생성할 사용자 정보를 포함하는 DTO
     * @return 생성된 사용자 정보를 담은 ResponseEntity (201 Created)
     */
    @PostMapping
    public ResponseEntity<UserDto> saveUser(@RequestBody UserDto userDto) {
        try {
            var savedUser = userService.saveUser(userDto);
            return ResponseEntity
                    .created(URI.create("/api/users/" + savedUser.id()))
                    .body(savedUser);
        } catch (IllegalArgumentException e) {
            // 사용자 이름 중복 등의 비즈니스 예외 처리
            return ResponseEntity.badRequest().build();
        }
    }

    /**
     * 모든 사용자 목록을 조회합니다.
     * @return 모든 사용자 정보를 담은 ResponseEntity (200 OK)
     */
    @GetMapping
    public ResponseEntity<List<UserDto>> findAll() {
        return ResponseEntity.ok(userService.findAll());
    }

    /**
     * 사용자 이름으로 단일 사용자 정보를 조회합니다.
     * @param userName 조회할 사용자의 이름
     * @return 사용자 정보를 담은 ResponseEntity (200 OK) 또는 404 Not Found
     */
    @GetMapping("/{userName}")
    public ResponseEntity<UserDto> getUserByUserName(@PathVariable("userName") String userName) {
        try {
            return ResponseEntity.ok(userService.getUserByUserName(userName));
        } catch (RuntimeException e) {
            // 사용자를 찾을 수 없는 경우 예외 처리
            return ResponseEntity.notFound().build();
        }
    }

    /**
     * 특정 ID를 가진 사용자를 삭제합니다.
     * @param id 삭제할 사용자의 ID
     * @return ResponseEntity (204 No Content)
     */
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteUser(@PathVariable("id") Long id) {
        userService.deleteUser(id);
        return ResponseEntity.noContent().build();
    }
}
