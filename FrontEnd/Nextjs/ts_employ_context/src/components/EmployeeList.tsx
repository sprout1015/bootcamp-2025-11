// ✅ 하위 컴포넌트: 부모(Main) 컴포넌트로부터 props를 받아 직원 리스트를 렌더링합니다.
import React, {useContext} from 'react';
// ✅ 타입 재사용을 위한 import
// @< 절대경로
import {EmployeeContext, EmployeeInfo, useEmployee} from "@/context/EmployeeContext";
import InfoTable from "@/components/InfoTable";
import {buttonBarStyle} from "./Main"

const buttonStyles: React.CSSProperties = {
    padding: "6px 10px",
    borderRadius: 3,
    border: "1px solid #ccc"
}

// --- 컴포넌트 선언 및 Props 사용 ---
// 함수형 컴포넌트를 선언합니다.
// 파라미터에서 '구조 분해 할당'을 사용하여 props 객체에서 필요한 값들을 바로 추출합니다.
// 이렇게 하면 함수 본문에서 'props.infoList' 대신 'infoList'처럼 바로 사용할 수 있어 코드가 간결해집니다.
const EmployeeList = () => {
    const {infoList, handleSelectedId} = useEmployee();

    return (
        <>
            <div style={buttonBarStyle}>
                {
                    // --- 리스트 렌더링 ---
                    // .map() 배열 메소드를 사용하여 infoList 데이터를 JSX 요소 배열로 변환합니다.
                    // React에서 동적인 리스트를 생성할 때 가장 일반적으로 사용되는 패턴입니다.
                    infoList?.map((info: EmployeeInfo) => (
                        <button
                            style={buttonStyles}
                            // --- 'key' Prop ---
                            // map 안에서 리스트를 렌더링할 때는 각 요소에 고유한 'key' prop을 지정해야 합니다.
                            // React는 이 key를 사용하여 어떤 항목이 변경, 추가 또는 삭제되었는지 식별하고, DOM을 효율적으로 업데이트합니다.
                            // index를 key로 사용하는 것은 리스트 순서가 바뀌지 않는 정적인 경우에만 괜찮지만, 고유 id를 사용하는 것이 가장 좋습니다.
                            key={info.id}
                            // --- 이벤트 핸들러와 데이터 전달 ---
                            // 버튼 클릭 시, 부모로부터 받은 handleSelectedId 함수를 호출합니다.
                            // 이때 해당 직원의 id를 인자로 전달하여, 자식 컴포넌트(EmployeeList)에서 발생한 이벤트를
                            // 부모 컴포넌트(Main)에 알리고 상태를 변경하게 합니다. (자식 -> 부모 데이터 전달 패턴)
                            onClick={()=>handleSelectedId(info.id)}
                        >
                            {info.name}
                        </button>
                    ))
                }
            </div>
            <InfoTable />
        </>
    );
};

export default EmployeeList;
