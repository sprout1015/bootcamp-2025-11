import {createSlice, PayloadAction} from "@reduxjs/toolkit";
import {
    deleteEmployeeInfoById,
    fetchEmployeeInfoById,
    fetchEmployeeInfoList, putEmployeeInfoById,
    registerEmployeeInfo
} from "@/redux/api/employeeAPI";

interface EmployeeStateType {
    mode: Mode,
    modeList: ModeItem[],
    infoList: EmployeeInfo[],
    selectedId: number,
    error: string | null,
    loading: boolean
}

export type EmployeeInfo = {
    id: number; // 고유 식별자
    name: string; // 이름
    age: number | string; // 숫자 또는 문자열 허용 (유연성 확보)
    job: string; // 직무
    language: string; // 사용하는 언어q
    pay: number | string; // 급여 (단위나 형식이 다양할 수 있어 string 허용)
}

type Mode = "default" | "register" | "update" | "delete" | "reset"

interface ModeItem {
    id: Exclude<Mode, "default">; // "default"는 버튼 목록에 없으므로 제외
    label: string;
}

const modeList = [
        {id:"register" as const, label:"register"},
        {id:"update" as const, label:"update"},
        {id:"delete" as const, label:"delete"},
        {id:"reset" as const, label:"reset"}
]

// initialState 설정
const initialEmployeeState: EmployeeStateType = {
    mode: "default",
    modeList: modeList,
    infoList: [],
    selectedId: 0,
    error: null,
    loading: false
}

// Action Reducers 설정
const handleModeReducer = (
    state: EmployeeStateType, action : PayloadAction<Mode>) => {
    const mode = action.payload;
    const {selectedId} = state;
    switch (mode){
        case "update":
            if (!selectedId)
                alert("직원을 선택해주세요");
            else
                state.mode = mode;
            break;
        case "reset":
            if(confirm("목록을 초기 데이터로 돌릴까요?"))
            {
                state = initialEmployeeState;
            }
            break;
        default:
            state.mode = mode
    }
}
// 자식 컴포넌트(EmployeeList)로부터 호출될 함수.
// 자식이 부모의 상태(selectedId)를 변경할 수 있도록 함수 자체를 props로 전달합니다.
const handleSelectedIdReducer = (
    state:EmployeeStateType, action:PayloadAction<number>) => {
    const id = action.payload;
    state.selectedId = id;
}

// Register 컴포넌트에서 호출될 함수. 새 직원을 등록합니다.
const handleRegisterEmployeeReducer=(
    state:EmployeeStateType, action:PayloadAction<EmployeeInfo> )=>{
    const info = action.payload;
    const nextId = state.infoList.length
        ? Math.max(...state.infoList.map(i => i.id))+1
        : 1
    state.infoList = [...state.infoList, {...info, id: nextId}]
}

// Update 컴포넌트에서 호출될 함수. 직원 정보를 수정합니다.
const handleUpdateEmployeeReducer=(
    state:EmployeeStateType, action:PayloadAction<EmployeeInfo> )=>{
    const info = action.payload;

    state.infoList = state.infoList.map(item=>
        item.id === info.id ? {...item, ...info} : item
    )
    state.mode = "default"
}


// thunk Slice에 담기
const employeeSlice = createSlice(
    {
        // 슬라이스명
        name: "employeeSlice",
        // 초기 상태값
        initialState: initialEmployeeState,
        //
        reducers:{
            // 어디 선언한 함수들
            handleMode : handleModeReducer,
            handleSelectedId: handleSelectedIdReducer,
            // handleRegisterEmployee : handleRegisterEmployeeReducer,
            handleUpdateEmployee : handleUpdateEmployeeReducer,
        },
        // API 받는 함수
        extraReducers:(builder) => {
            // 전체 조회
            builder
                .addCase(fetchEmployeeInfoList.pending,  (state) => {
                    state.loading = true;
                    state.error = null;
                })
                .addCase(fetchEmployeeInfoList.fulfilled, (state, action) => {
                        state.loading = false;
                        state.infoList = action.payload; // === response.data
                })
                .addCase(fetchEmployeeInfoList.rejected, (state, action) => {
                    state.loading = false;
                    state.error = action.payload ?? '알 수 없는 오류';
                })
            // 단일 조회
            builder
                .addCase(
                    fetchEmployeeInfoById.pending
                    , (state, action) => {
                        state.loading = true;
                        state.error = null;
                    })
                .addCase(fetchEmployeeInfoById.fulfilled
                    , (state, action) => {
                        state.loading = false;
                    })
                .addCase(fetchEmployeeInfoById.rejected
                    , (state, action) => {
                        state.loading = false;
                        state.error = action.payload?? "알 수 없는 이유";
                    })

            // POST - 직원 등록
            builder
                .addCase(
                    registerEmployeeInfo.pending
                    , (state, action) => {
                        state.loading = true;
                        state.error = null;
                    })
                .addCase(registerEmployeeInfo.fulfilled
                    , (state, action) => {
                        state.loading = false;
                        state.infoList.push(action.payload);
                    })
                .addCase(registerEmployeeInfo.rejected
                    , (state, action) => {
                        state.loading = false;
                        state.error = action.payload?? "알 수 없는 이유";
                })
            // 삭제
            builder
                .addCase(
                    deleteEmployeeInfoById.pending
                    , (state) => {
                        state.loading = true;
                        state.error = null;
                    })
                .addCase(deleteEmployeeInfoById.fulfilled
                    , (state, action) => {
                        state.loading = false;
                        state.infoList = state.infoList.filter(emp => emp.id !== action.payload);
                        state.mode = "default";
                        state.selectedId = 0;
                    })
                .addCase(deleteEmployeeInfoById.rejected
                    , (state, action) => {
                        state.loading = false;
                        state.error = action.payload?? "알 수 없는 이유";
                    })
            // 수정
            builder
                .addCase(
                    putEmployeeInfoById.pending
                    , (state, action) => {
                        state.loading = true;
                        state.error = null;
                    })
                .addCase(putEmployeeInfoById.fulfilled
                    , (state, action) => {
                        state.loading = false;
                        state.infoList = state.infoList.map(item =>
                            item.id === action.payload.id ? action.payload : item
                        );
                        state.mode = "default";
                    })
                .addCase(putEmployeeInfoById.rejected
                    , (state, action) => {
                        state.loading = false;
                        state.error = action.payload?? "알 수 없는 이유";
                    })
        }
    }
)

export const {
    handleMode,
    handleSelectedId,
    // handleRegisterEmployee,
    handleUpdateEmployee,
} = employeeSlice.actions;
export default employeeSlice.reducer;