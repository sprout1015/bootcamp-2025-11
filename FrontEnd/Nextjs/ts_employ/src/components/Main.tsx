'use client' // ✅ Next.js App Router에서 클라이언트 컴포넌트임을 명시 (useState, useEffect 같은 훅 사용 가능)

// React와 리액트 훅(Hook)들을 가져옵니다.
// - useState: 컴포넌트의 상태(state)를 관리합니다. 상태가 변경되면 컴포넌트가 리렌더링됩니다.
// - useMemo: 계산 비용이 큰 함수의 결과값을 메모이제이션(기억)하여, 의존성이 변경될 때만 함수를 다시 실행합니다. 성능 최적화에 사용됩니다.
import React, {useMemo, useState} from 'react';
import EmployeeList from "@/components/EmployeeList";
import Update from "@/components/Update";
import Register from "@/components/Register"; // ✅ props를 전달받는 하위 컴포넌트

export const buttonBarStyle:React.CSSProperties = {
    display: "flex",
    flexDirection: "row",
    justifyContent: "center",
    alignItems: "center",
    gap: "10px",
    padding: "20px",
    backgroundColor: "rebeccapurple"
}

// ✅ 타입스크립트의 타입 별칭(type alias) 사용
// ✅ DB 테이블의 스키마처럼 데이터의 구조를 정의합니다.
// ✅ export 키워드를 통해 다른 파일(컴포넌트)에서 이 타입을 재사용할 수 있습니다.
export type EmployeeInfo = {
    id: number; // 고유 식별자
    name: string; // 이름
    age: number | string; // 숫자 또는 문자열 허용 (유연성 확보)
    job: string; // 직무
    language: string; // 사용하는 언어
    pay: number | string; // 급여 (단위나 형식이 다양할 수 있어 string 허용)
}

// ✅ 초기 상태값: EmployeeInfo 객체 배열
// ✅ useState<EmployeeInfo[]>의 초기값으로 사용됨
const initialTotal: EmployeeInfo[] = [
    { id: 1, name: 'John', age: 35, job: "frontend", language: "react", pay: 12 },
    { id: 2, name: 'Qohn', age: 15, job: "backend", language: "java", pay: 13 },
    { id: 3, name: 'Wohn', age: 25, job: "AI", language: "python", pay: 41 },
    { id: 4, name: 'Eohn', age: 55, job: "Infra", language: "AWS", pay: 51 }
]

type Mode = "default" | "register" | "update" | "delete" | "reset"

const Main = () => {
    // --- React State (상태) 관리 ---
    // useState 훅을 사용하여 컴포넌트의 상태를 선언합니다.
    // const [상태값, 상태변경함수] = useState(초기값);
    // 상태가 변경되면(setInfoList, setSelectedId 등 함수 호출 시) 컴포넌트가 자동으로 다시 렌더링됩니다.

    // ✅ 제네릭<EmployeeInfo[]>을 활용하여 infoList가 EmployeeInfo 객체 배열 타입임을 명시합니다.
    const [infoList, setInfoList] = useState<EmployeeInfo[]>(initialTotal);

    // ✅ selectedId는 현재 선택된 직원의 id를 저장하는 상태입니다.
    const [selectedId, setSelectedId] = useState<number>(0);
    // ✅ mode는 현재 UI의 모드(등록, 수정 등)를 관리하는 상태입니다.
    const [mode, setMode] = useState<Mode>("default");

    // --- 성능 최적화를 위한 useMemo ---
    // useMemo는 의존성 배열([])에 포함된 값이 변경되지 않는 한, 내부 함수의 결과값을 계속 재사용합니다.
    // 이 경우, modes 배열은 컴포넌트가 처음 렌더링될 때 한 번만 생성되고 이후에는 재생성되지 않아 불필요한 연산을 막습니다.
    const modes = useMemo(() => [
            {id:"register" as const, label:"register"},
            {id:"update" as const, label:"update"},
            {id:"delete" as const, label:"delete"},
            {id:"reset" as const, label:"reset"}]
        , [])

    const handleMode = (mod: Mode) => {
        switch (mod){
            case "update":
                if (!selectedId)
                    alert("직원을 선택해주세요");
                else
                    setMode(mod);
                break;
            case "delete":
                if (!selectedId){
                    alert("직원을 선택해주세요");
                    break;
                }
                const targetInfo = infoList.find(target => target.id === selectedId)
                if (!targetInfo)
                    alert("해당 직원은 존재하지 않는 직원입니다");
                else
                    if (confirm(`${targetInfo.name} 직원을 삭제할까요?`)) {
                        // filter를 사용하여 삭제할 직원을 제외한 새 배열을 만듭니다. (불변성 유지)
                        setInfoList(prev => prev.filter(info => info.id !== selectedId));
                        setMode("default");
                        setSelectedId(0);
                    }
                break;
            case "reset":
                if(confirm("목록을 초기 데이터로 돌릴까요?"))
                {
                    setInfoList(initialTotal);
                    setMode("default");
                    setSelectedId(0);
                }
                break;
            default:
                setMode(mod)
        }
    }

    // 자식 컴포넌트(EmployeeList)로부터 호출될 함수.
    // 자식이 부모의 상태(selectedId)를 변경할 수 있도록 함수 자체를 props로 전달합니다.
    const handleSelectedId = (id: number) => {
        setSelectedId(id)
    }

    // --- 상태 업데이트와 불변성 ---
    // React에서 상태를 업데이트할 때는 '불변성'을 지키는 것이 중요합니다.
    // 기존 상태 배열이나 객체를 직접 수정하는 대신, 복사본을 만들어 변경한 후 새로운 값으로 설정해야 합니다.
    // (예: spread 연산자 '...', filter, map 등 배열 메소드 사용)

    // Register 컴포넌트에서 호출될 함수. 새 직원을 등록합니다.
    const handleRegisterEmployee=(info: EmployeeInfo)=>{
        // setInfoList의 콜백 함수를 사용하여 이전 상태(prev)를 기반으로 새 상태를 만듭니다.
        // spread 연산자(...)를 사용해 기존 배열을 복사하고, 새 직원 정보를 추가한 '새로운 배열'을 반환합니다.
        setInfoList(prev =>
            [...prev,
                {...info,
                    id:
                        infoList.length
                            ? Math.max(...infoList.map(i => i.id))+1
                            : 1
        }])
        setMode("default");
    }

    // Update 컴포넌트에서 호출될 함수. 직원 정보를 수정합니다.
    const handleUpdateEmployee=(info: EmployeeInfo)=>{
        // map을 사용하여 기존 배열을 순회하면서, 수정할 직원의 id와 일치하는 항목을 찾아 새 정보로 교체합니다.
        // 일치하지 않는 항목은 그대로 유지하여 '새로운 배열'을 만듭니다.
        setInfoList(prev => prev.map(item=>
            item.id === info.id ? {...item, ...info} : item
        ))
        setMode("default")
    }

    // --- Props 전달 ---
    // 자식 컴포넌트에 전달할 데이터와 함수들을 객체로 묶습니다.
    const props = { infoList, selectedId, handleSelectedId };
    const registerProps = { handleRegisterEmployee };
    const updateProps = { infoList, selectedId, handleUpdateEmployee };

    return (
        // 여러 JSX 요소를 반환할 때는 Fragment(<></>)로 감싸야 합니다.
        <>
            <div>
                {/* ❌ 아래는 props를 하나하나 명시적으로 전달하는 방식입니다. */}
                {/* <EmployeeList infoList={infoList} updatedInfo={updatedInfo} /> */}

                {/* ✅ spread 연산자(...)를 사용해 props 객체의 모든 속성을 한 번에 전달합니다. (가독성 및 재사용성 향상) */}
                <EmployeeList {...props} />
            </div>
            <div style={buttonBarStyle}>
                {
                    modes.map(mode=> (
                    <button key={mode.id}
                        onClick={()=>handleMode(mode.id)} >
                        {mode.label}
                    </button>
                ))
                }
            </div>
            <div>
                {/* --- 조건부 렌더링 --- */}
                {/* && 연산자를 사용한 조건부 렌더링입니다. */}
                {/* mode 상태가 'register'일 때만 Register 컴포넌트를 렌더링합니다. */}
                {mode==="register" &&  <Register {...registerProps} />}
                {mode==="update" &&  <Update {...updateProps} />}
            </div>
        </>
    );
};

export default Main;
