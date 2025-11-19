import React, {createContext, PropsWithChildren, useContext, useMemo, useState} from 'react';

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

export type Mode = "default" | "register" | "update" | "delete" | "reset"

const modeList = useMemo(() => [
        {id:"register" as const, label:"register"},
        {id:"update" as const, label:"update"},
        {id:"delete" as const, label:"delete"},
        {id:"reset" as const, label:"reset"}]
    , [])


// ✅ 초기 상태값: EmployeeInfo 객체 배열
// ✅ useState<EmployeeInfo[]>의 초기값으로 사용됨
const initialTotal: EmployeeInfo[] = [
    { id: 1, name: 'John', age: 35, job: "frontend", language: "react", pay: 12 },
    { id: 2, name: 'Qohn', age: 15, job: "backend", language: "java", pay: 13 },
    { id: 3, name: 'Wohn', age: 25, job: "AI", language: "python", pay: 41 },
    { id: 4, name: 'Eohn', age: 55, job: "Infra", language: "AWS", pay: 51 }
]

interface ModeItem {
    id: Exclude<Mode, "default">; // "default"는 버튼 목록에 없으므로 제외
    label: string;
}

interface EmployeeContextValue {
    mode: Mode,
    modeList: ModeItem[],
    infoList: EmployeeInfo[],
    selectedId: number,
    handleMode: (mode:Mode)=> void,
    handleSelectedId: (id:number)=>void
    handleRegisterEmployee: (info:EmployeeInfo)=>void
    handleUpdateEmployee: (info:EmployeeInfo)=>void
}

export const EmployeeContext = createContext<EmployeeContextValue | undefined>(undefined);

export const EmployeeProvider = ({children}:PropsWithChildren) => {
    // ✅ 제네릭<EmployeeInfo[]>을 활용하여 infoList가 EmployeeInfo 객체 배열 타입임을 명시합니다.
    const [infoList, setInfoList] = useState<EmployeeInfo[]>(initialTotal);
    // ✅ selectedId는 현재 선택된 직원의 id를 저장하는 상태입니다.
    const [selectedId, setSelectedId] = useState<number>(0);
    // ✅ mode는 현재 UI의 모드(등록, 수정 등)를 관리하는 상태입니다.
    const [mode, setMode] = useState<Mode>("default");

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

    const value = useMemo(()=>(
        {
        infoList, mode, modeList, selectedId, handleMode, handleSelectedId, handleRegisterEmployee, handleUpdateEmployee
        }
    ),[infoList, mode, modeList, selectedId, handleMode, handleSelectedId, handleRegisterEmployee, handleUpdateEmployee])

    return (
        <EmployeeContext.Provider value={value}>
            {children}
        </EmployeeContext.Provider>
    )
}

// 커스터마이즈 hook : 맨 앞에 use사용
export const useEmployee= () => {
    const context = useContext(EmployeeContext);
    if(!context)
        throw new Error("useContext() not found!");
    return context;
}