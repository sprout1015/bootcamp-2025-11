import React, {useState} from 'react';
import type {EmployeeInfo} from "@/components/Main";
import {formStyle, inputStyle, labelStyle} from "@/util/Style";

interface RegisterProps {
    handleRegisterEmployee: (info:EmployeeInfo) => void;
}

const initialInfo: EmployeeInfo = {
    id:0, name:'', job:'', pay: 0, age: 0, language: ''
}

const Register = ({handleRegisterEmployee}: RegisterProps) => {
    // --- Form 상태 관리를 위한 useState ---
    // 폼의 각 입력 필드 값을 하나의 객체로 묶어 상태로 관리합니다.
    // 이렇게 React 상태와 폼 입력 값을 연결하는 것을 '제어 컴포넌트(Controlled Component)'라고 합니다.
    // 사용자의 모든 입력은 React의 상태를 통해 관리됩니다.
    const [info, setInfo] = useState<EmployeeInfo>(initialInfo);

    // --- 입력 필드 변경 핸들러 ---
    // 사용자가 input 필드에 값을 입력할 때마다 호출됩니다.
    const handleChange = (e: React.ChangeEvent<HTMLInputElement>)=> {
        // 이벤트가 발생한 input의 name과 value를 추출합니다.
        const { name, value } = e.target;
        // 이전 상태(prev)를 기반으로 새로운 상태 객체를 만듭니다.
        // spread 연산자(...)로 기존 상태를 복사하고,
        // 계산된 속성 이름([name])을 사용하여 변경된 필드의 값만 동적으로 업데이트합니다.
        setInfo(prev => ({...prev, [name]:value}))
    }

    // --- 폼 제출 핸들러 ---
    const handleSubmit = (e: React.FormEvent<HTMLFormElement>)=> {
        // e.preventDefault()를 호출하여 폼 제출 시 발생하는 브라우저의 기본 동작(페이지 새로고침)을 막습니다.
        e.preventDefault();
        // 부모 컴포넌트로부터 받은 handleRegisterEmployee 함수를 호출하여,
        // 현재 폼의 상태(info)를 부모에게 전달합니다.
        handleRegisterEmployee(info);
    }

    const checkValidity = (e: React.InvalidEvent<HTMLInputElement>)=> {
        const targetName = e.target.name;
        // HTML5 'required' 속성에 의해 유효성 검사가 실패했을 때 호출됩니다.
        // 여기에 커스텀 유효성 검사 로직이나 사용자 피드백을 추가할 수 있습니다.
        switch (targetName) {

        }
    }

    return (
        <form style={formStyle} onSubmit={handleSubmit}>
            <label style={labelStyle} >
                Name
                {/*
                  value={info.name} 처럼 value 속성을 명시적으로 바인딩하면 완전한 제어 컴포넌트가 됩니다.
                  현재는 onChange만 사용하고 있지만, value를 바인딩하면 React 상태가 항상 input의 값을 제어하게 됩니다.
                */}
                <input type="text" name="name" onChange={handleChange} style={inputStyle} required onInvalid={checkValidity}/>
            </label>
            <label style={labelStyle} >
                Age
                <input type="number" name="age" onChange={handleChange} style={inputStyle} min={1} required onInvalid={checkValidity}/>
            </label>
            <label style={labelStyle} >
                Job
                <input type="text" name="job" onChange={handleChange} style={inputStyle}  />
            </label>
            <label style={labelStyle} >
                Language
                <input type="text" name="language" onChange={handleChange} style={inputStyle}  />
            </label>
            <label style={labelStyle} >
                Pay
                <input type="number" name="pay" min={0} onChange={handleChange} style={inputStyle}  required onInvalid={checkValidity}/>
            </label>
            <button type="submit">등록</button>
        </form>
    );
};

export default Register;
