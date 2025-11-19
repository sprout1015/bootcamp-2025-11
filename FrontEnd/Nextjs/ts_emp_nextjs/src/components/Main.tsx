'use client' // ✅ Next.js App Router에서 클라이언트 컴포넌트임을 명시 (useState, useEffect 같은 훅 사용 가능)

// React와 리액트 훅(Hook)들을 가져옵니다.
// - useState: 컴포넌트의 상태(state)를 관리합니다. 상태가 변경되면 컴포넌트가 리렌더링됩니다.
// - useMemo: 계산 비용이 큰 함수의 결과값을 메모이제이션(기억)하여, 의존성이 변경될 때만 함수를 다시 실행합니다. 성능 최적화에 사용됩니다.
import React from 'react';
import EmployeeList from "@/components/EmployeeList";
import Update from "@/components/Update";
import Register from "@/components/Register";
import {useDispatch, useSelector} from "react-redux";
import {RootState} from "@/redux/employStore";
import {handleMode} from "@/redux/slice/employeeSlice";

export const buttonBarStyle:React.CSSProperties = {
    display: "flex",
    flexDirection: "row",
    justifyContent: "center",
    alignItems: "center",
    gap: "10px",
    padding: "20px",
    backgroundColor: "rebeccapurple"
}


const Main = () => {
    const {mode, modeList} = useSelector((state:RootState) => state.empStore);
    const dispatch = useDispatch();

    return (
        // 여러 JSX 요소를 반환할 때는 Fragment(<></>)로 감싸야 합니다.
        <>
            <div>
                <EmployeeList />
            </div>
            <div style={buttonBarStyle}>
                {
                    modeList.map(mode=> (
                    <button key={mode.id}
                        onClick={()=>dispatch(handleMode(mode.id))} >
                        {mode.label}
                    </button>
                ))
                }
            </div>
            <div>
                {mode==="register" &&  <Register />}
                {mode==="update" &&  <Update />}
            </div>
        </>
    );
};

export default Main;