package com.bootcamp.employee.application.dto.user;

import com.bootcamp.employee.domain.model.user.User;
import lombok.Builder;

/**
 * User 도메인을 위한 DTO (Data Transfer Object) 레코드입니다.
 * 애플리케이션 계층에서 데이터를 전달하는 역할을 하며, 도메인 모델의 내부 구조를
 * 외부 계층(예: Interfaces Layer)에 직접 노출하지 않도록 합니다.
 * 엔티티를 DTO로 변환하거나, DTO를 엔티티로 변환하는 헬퍼 메서드를 포함합니다.
 */
@Builder
public record UserDto(
        Long id,
        String userName,
        Integer age,
        String job,
        String language,
        Integer pay
) {
    public static UserDto fromEntity(User user) {
        return UserDto.builder()
                .id(user.getId())
                .userName(user.getUserName())
                .age(user.getAge())
                .job(user.getJob())
                .language(user.getLanguage())
                .pay(user.getPay())
                .build();
    }

    public User toEntity() {
        return User.builder()
                .userName(this.userName)
                .age(this.age)
                .job(this.job)
                .language(this.language)
                .pay(this.pay)
                .build();
    }
}
