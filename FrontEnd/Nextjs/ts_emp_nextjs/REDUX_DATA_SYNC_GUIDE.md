# Redux Toolkit을 사용한 데이터 동기화 가이드

`Register` 또는 `Update`와 같은 데이터 변경 작업 후, `infoList`에 최신 데이터를 자동으로 반영하는 가장 효율적인 방법은 `extraReducers`를 활용하는 것입니다. 이 가이드는 불필요한 API 재요청 없이 Redux 상태를 최신으로 유지하는 방법을 설명합니다.

## 핵심 개념: `extraReducers`를 이용한 상태 직접 업데이트

데이터 변경(등록, 수정) API 요청이 성공적으로 완료되면, 서버는 보통 변경된 최신 데이터를 응답으로 돌려줍니다. 이 응답 데이터를 `createAsyncThunk`의 `fulfilled` 액션의 `payload`로 받아 Redux 상태(`infoList`)를 직접 업데이트하는 방식입니다. 이렇게 하면 네트워크 요청을 한 번 더 보내는 비효율적인 `fetchEmployeeInfoList` 재실행 없이 즉시 UI를 최신 상태로 만들 수 있습니다.

### 1. `employeeAPI.ts` 수정: 변경된 데이터 반환 확인

`createAsyncThunk`로 정의된 API Thunk들이 서버로부터 받은 최신 데이터를 `return`하도록 해야 합니다. 이 `return` 값이 `fulfilled` 액션의 `payload`로 전달됩니다.

**`@/redux/api/employeeAPI.ts`**

```typescript
// @/redux/api/employeeAPI.ts

import { createAsyncThunk } from "@reduxjs/toolkit";
import axios from "axios";
import { EmployeeInfo } from "@/redux/slice/employeeSlice"; // EmployeeInfo 타입 import 확인

// registerEmployeeInfo 예시
export const registerEmployeeInfo = createAsyncThunk(
    'employee/registerEmployeeInfo',
    async (newEmployee: Omit<EmployeeInfo, 'id'>, thunkAPI) => {
        const response = await axios.post('http://localhost:3001/employees', newEmployee);
        // ★ 중요: 서버로부터 받은 생성된 데이터를 반환합니다.
        return response.data as EmployeeInfo;
    }
);

// putEmployeeInfoById 예시
export const putEmployeeInfoById = createAsyncThunk(
    'employee/putEmployeeInfoById',
    async (employee: EmployeeInfo, thunkAPI) => {
        const response = await axios.put(`http://localhost:3001/employees/${employee.id}`, employee);
        // ★ 중요: 서버로부터 받은 수정된 데이터를 반환합니다.
        return response.data as EmployeeInfo;
    }
);

// fetchEmployeeInfoList (이 함수는 페이지 최초 로드 또는 명시적인 재조회 시에만 필요합니다)
export const fetchEmployeeInfoList = createAsyncThunk(
    'employee/fetchEmployeeInfoList',
    async () => {
        const response = await axios.get('http://localhost:3001/employees');
        return response.data as EmployeeInfo[];
    }
);
```

### 2. `employeeSlice.ts` 수정: `extraReducers`에서 상태 업데이트

`createSlice`의 `extraReducers` 섹션을 수정하여, 각 비동기 Thunk가 성공(`fulfilled`)했을 때 `infoList` 상태를 직접 조작합니다. Redux Toolkit은 Immer.js를 내장하고 있으므로, `push`나 `map`과 같은 변형(mutating) 로직을 마치 불변(immutable) 데이터를 다루듯이 안전하게 사용할 수 있습니다.

**`@/redux/slice/employeeSlice.ts`**

```typescript
// @/redux/slice/employeeSlice.ts

import { createSlice, PayloadAction } from "@reduxjs/toolkit";
import { fetchEmployeeInfoList, putEmployeeInfoById, registerEmployeeInfo } from "@/redux/api/employeeAPI";

// EmployeeInfo, EmployeeState 인터페이스가 정의되어 있다고 가정합니다.
// 예시:
export interface EmployeeInfo {
    id: number;
    name: string;
    job: string;
    pay: number;
    age: number;
    language: string;
}

interface EmployeeState {
    infoList: EmployeeInfo[];
    selectedId: number;
    status: 'idle' | 'loading' | 'succeeded' | 'failed'; // 로딩 상태 추가
}

const initialState: EmployeeState = {
    infoList: [],
    selectedId: 0,
    status: 'idle',
};

const employeeSlice = createSlice({
    name: 'employee',
    initialState,
    reducers: {
        // ... (기존 동기 reducers, 예: setSelectedId)
        setSelectedId: (state, action: PayloadAction<number>) => {
            state.selectedId = action.payload;
        },
    },
    // ★ 핵심: 비동기 액션의 결과를 처리하는 부분
    extraReducers: (builder) => {
        builder
            // --- 목록 조회 관련 ---
            .addCase(fetchEmployeeInfoList.pending, (state) => {
                state.status = 'loading';
            })
            .addCase(fetchEmployeeInfoList.fulfilled, (state, action: PayloadAction<EmployeeInfo[]>) => {
                state.status = 'succeeded';
                state.infoList = action.payload;
            })
            .addCase(fetchEmployeeInfoList.rejected, (state) => {
                state.status = 'failed';
            })

            // --- 직원 등록 관련 ---
            .addCase(registerEmployeeInfo.pending, (state) => {
                state.status = 'loading';
            })
            .addCase(registerEmployeeInfo.fulfilled, (state, action: PayloadAction<EmployeeInfo>) => {
                state.status = 'succeeded';
                // 받아온 새로운 직원 정보를 infoList에 추가
                state.infoList.push(action.payload);
            })
            .addCase(registerEmployeeInfo.rejected, (state) => {
                state.status = 'failed';
            })

            // --- 직원 수정 관련 ---
            .addCase(putEmployeeInfoById.pending, (state) => {
                state.status = 'loading';
            })
            .addCase(putEmployeeInfoById.fulfilled, (state, action: PayloadAction<EmployeeInfo>) => {
                state.status = 'succeeded';
                // 받아온 수정된 직원 정보로 infoList에서 해당 항목을 교체
                const index = state.infoList.findIndex(emp => emp.id === action.payload.id);
                if (index !== -1) {
                    state.infoList[index] = action.payload;
                }
            })
            .addCase(putEmployeeInfoById.rejected, (state) => {
                state.status = 'failed';
            });
    }
});

export const { setSelectedId } = employeeSlice.actions; // 기존 액션 export 유지
export default employeeSlice.reducer;
```

### 왜 이 방법이 최적인가요?

1.  **성능 최적화**: `Register`나 `Update` 후에 `infoList` 전체를 다시 불러오는 불필요한 네트워크 요청을 방지하여 애플리케이션의 반응 속도를 향상시킵니다. 서버로부터 받은 최소한의 데이터만으로 상태를 업데이트합니다.
2.  **관심사 분리 (Separation of Concerns)**: 컴포넌트는 오직 "데이터 변경" 액션(예: `registerEmployeeInfo`)을 디스패치하는 역할에만 집중하고, 그에 따른 상태 변화(목록 업데이트)는 Redux Slice 내부에서 처리됩니다. 이는 컴포넌트의 로직을 간결하게 유지하고 유지보수를 용이하게 합니다.
3.  **코드 일관성 및 재사용성**: `registerEmployeeInfo` 또는 `putEmployeeInfoById` 액션이 성공적으로 완료되면, `infoList`는 항상 정확하게 업데이트됩니다. 이 로직은 Redux Slice에 중앙화되어 있으므로, 어떤 컴포넌트에서 이 액션을 디스패치하든 일관된 상태 업데이트를 보장하며 코드 중복을 피할 수 있습니다.
4.  **Redux Toolkit의 활용**: `createAsyncThunk`와 `extraReducers`는 Redux Toolkit이 비동기 로직과 상태 관리를 효율적으로 처리하기 위해 제공하는 강력한 기능입니다. 이 기능을 최대한 활용하는 것이 Redux Toolkit의 의도와도 부합합니다.

### 결론

이 설계 방식은 `Register.tsx` 및 `Update.tsx` 컴포넌트의 `handleSubmit` 함수 로직은 그대로 유지하면서, 데이터 변경 후 `infoList`를 자동으로 최신 상태로 동기화할 수 있게 해줍니다. 이제 `dispatch(registerEmployeeInfo(info))` 또는 `dispatch(putEmployeeInfoById(infoToUpdate))`가 성공하면, `extraReducers`가 해당 `fulfilled` 액션을 감지하고 `infoList`를 직접 업데이트하여 UI에 즉시 반영될 것입니다.
