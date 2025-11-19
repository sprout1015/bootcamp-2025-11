'use client' // ✅ Next.js App Router에서 클라이언트 컴포넌트임을 명시 (useState 등 훅 사용 가능)

import React, {useMemo, useState} from 'react'; // ✅ useState는 제네릭을 통해 타입 안정성 확보 가능
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
// ✅ DB 테이블의 스키마처럼 key-value 구조로 정의
// ✅ export로 다른 컴포넌트에서 재사용 가능
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
    // ✅ 제네릭을 활용한 상태 선언: infoList는 EmployeeInfo 객체 배열
    // ✅ 얕은 복사를 통해 상태 변경 시 불변성 유지 필요
    const [infoList, setInfoList] = useState<EmployeeInfo[]>(initialTotal);

    // ✅ selectedId은 현재 선택된 고용자가 누군지 관리하는 변수
    const [selectedId, setSelectedId] = useState<number>(0);
    // ✅ mode는 현재 선택된 방식이 누군지 관리하는 변수
    const [mode, setMode] = useState<Mode>("default");

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
                        infoList.find(info => info.id);
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

    const handleSelectedId = (id: number) => {
        setSelectedId(id)
    }

    const handleRegisterEmployee=(info: EmployeeInfo)=>{
        setInfoList(prev =>
            [...prev,
                {...info,
                    id:
                        infoList.length
                            ? Math.max(...infoList.map(i => i.id))+1
                            : 1
        }])
    }

    const handleUpdateEmployee=(info: EmployeeInfo)=>{
        setInfoList(prev => prev.map(item=>
            item.id === info.id ? {...item, ...info} : item
        ))
        setMode("default")
    }

    // ✅ props 객체 생성
    // ✅ 구조 분해 없이 spread 연산자(...)로 전달 가능
    const props = { infoList, selectedId, handleSelectedId };
    const registerProps = { handleRegisterEmployee };
    const updateProps = { infoList, selectedId, handleUpdateEmployee };

    return (
        // 블록 여러 개 담을 때는 빈박스"<>" 안에 넣기
        <>
            <div>
                {/* ❌ 아래는 props를 명시적으로 전달하는 방식 (가독성 떨어질 수 있음) */}
                {/* <EmployeeList infoList={infoList} updatedInfo={updatedInfo} /> */}

                {/* ✅ spread 연산자를 사용해 props를 한 번에 전달 (가독성 및 재사용성 향상) */}
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
                {mode==="register" &&  <Register {...registerProps} />}
                {mode==="update" &&  <Update {...updateProps} />}
            </div>
        </>
    );
};

export default Main;