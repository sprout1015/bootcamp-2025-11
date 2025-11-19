import React, {useEffect, useState} from 'react';
import type {EmployeeInfo} from "@/components/Main";
import {formStyle, inputStyle, labelStyle} from "@/util/Style";

interface UpdateProps {
    infoList: EmployeeInfo[];
    selectedId?: number;
    handleUpdateEmployee: (info:EmployeeInfo) => void;
}

const initialInfo: EmployeeInfo = {
    id:0, name:'', job:'', pay: 0, age: 0, language: ''
}

const Update = ({ infoList, selectedId, handleUpdateEmployee }: UpdateProps) => {
    // 폼 데이터를 관리하기 위한 상태
    const [infoToUpdate, setInfoToUpdate] = useState<EmployeeInfo>(initialInfo);

    // --- useEffect 훅: Side Effect 처리 ---
    // useEffect는 컴포넌트의 렌더링 이후에 특정 작업(Side Effect)을 수행하고 싶을 때 사용합니다.
    // (예: 데이터 가져오기, 구독 설정, 직접 DOM 조작 등)
    // 아래 코드는 'selectedId' prop이 변경될 때마다 실행됩니다.
    useEffect(() => {
        // infoList에서 선택된 id와 일치하는 직원 정보를 찾습니다.
        const foundInfo = infoList.find(info => info.id === selectedId);
        // 찾은 정보가 있으면, 해당 정보로 폼의 상태를 업데이트하여 input 필드들을 채웁니다.
        if(foundInfo)
            setInfoToUpdate(foundInfo);
    }, [selectedId, infoList]); // ✅ 의존성 배열: 이 배열 안의 값이 변경될 때만 useEffect 내부의 함수가 실행됩니다.

    // --- 제어 컴포넌트(Controlled Component) ---
    // input의 value를 React 상태(infoToUpdate)와 직접 바인딩하고,
    // onChange 핸들러를 통해 상태를 업데이트합니다.
    // 이렇게 하면 React 상태가 항상 input의 값을 제어하게 되어 데이터 흐름이 단방향으로 관리됩니다.
    const handleChange = (e: React.ChangeEvent<HTMLInputElement>)=> {
        const { name, value } = e.target;
        setInfoToUpdate(prev => ({...prev, [name]:value}))
    }

    const handleSubmit = (e: React.FormEvent<HTMLFormElement>)=> {
        e.preventDefault();
        handleUpdateEmployee(infoToUpdate);
    }

    return (
        <form style={formStyle} onSubmit={handleSubmit}>
            <label style={labelStyle} >
                Name
                {/* `value` prop을 React 상태와 연결합니다. */}
                <input type="text" name="name" onChange={handleChange} style={inputStyle} value={infoToUpdate.name} disabled/>
            </label>
            <label style={labelStyle} >
                Age
                <input type="number" name="age" onChange={handleChange} style={inputStyle} value={infoToUpdate.age} min={1} required/>
            </label>
            <label style={labelStyle} >
                Job
                <input type="text" name="job" onChange={handleChange} style={inputStyle} value={infoToUpdate.job} />
            </label>
            <label style={labelStyle} >
                Language
                <input type="text" name="language" onChange={handleChange} style={inputStyle} value={infoToUpdate.language} />
            </label>
            <label style={labelStyle} >
                Pay
                <input type="number" name="pay" min={0} onChange={handleChange} style={inputStyle}  value={infoToUpdate.pay} required/>
            </label>
            <button type="submit">수정</button>
        </form>
    );
};

export default Update;
