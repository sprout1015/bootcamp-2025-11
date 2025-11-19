// ✅ 하위 컴포넌트: props를 받아 직원 리스트를 렌더링
import React from 'react';
// ✅ 타입 재사용을 위한 import
// @< 절대경로
import type { EmployeeInfo } from "@/components/Main";
import InfoTable from "@/components/InfoTable";
import {buttonBarStyle} from "./Main"

const buttonStyles: React.CSSProperties = {
    padding: "6px 10px",
    borderRadius: 3,
    border: "1px solid #ccc"
}

// ✅ props 타입 정의
// ✅ infoList: 직원 배열, info: 단일 직원 정보
interface EmployeeInfoProps {
    infoList: EmployeeInfo[];
    selectedId?: number; // null 체크
    handleSelectedId: (id:number) => void;
}

// ✅ 구조 분해 할당으로 props를 바로 꺼냄
// ✅ 함수 선언부에서 어떤 props를 사용하는지 명확하게 드러남
const EmployeeList = ({ infoList, selectedId, handleSelectedId }: EmployeeInfoProps) => {

    const props = {infoList, selectedId}

    return (
        <>
            <div style={buttonBarStyle}>
                {
                    // ✅ map을 통해 infoList 배열을 순회하며 각 직원의 이름을 출력
                    // ✅ key로 index를 사용하는 것은 권장되지 않지만, id가 고유하므로 대체 가능
                    infoList?.map((info: EmployeeInfo, index: number) => (
                        <button
                            style={buttonStyles}
                            key={index}
                            onClick={()=>handleSelectedId(info.id)}
                        >
                            {info.name}
                        </button>
                    ))
                }
            </div>
            <InfoTable {...props}/>
        </>
    );
};

export default EmployeeList;