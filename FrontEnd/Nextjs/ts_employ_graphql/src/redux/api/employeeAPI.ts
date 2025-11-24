import { createAsyncThunk } from "@reduxjs/toolkit";
import { EmployeeInfo } from "@/redux/slice/employeeSlice";
import axios from "axios";

const API_URL = "http://backend/graphql";

// GraphQL 요청을 위한 헬퍼 함수
const graphqlRequest = async (query: string, variables?: object) => {
    try {
        const response = await axios.post(API_URL, {
            query,
            variables,
        });

        if (response.data.errors) {
            throw new Error(response.data.errors.map((err: any) => err.message).join(', '));
        }

        return response.data.data;
    } catch (error: any) {
        // 네트워크 오류 또는 GraphQL 오류를 처리
        const errorMessage = error.response?.data?.errors?.[0]?.message || error.message || "An unknown error occurred";
        throw new Error(errorMessage);
    }
};

// 전체 직원 조회
export const fetchEmployeeInfoList = createAsyncThunk<EmployeeInfo[], void, { rejectValue: string }>(
    "emp/fetchEmployeeInfoList",
    async (_, thunkAPI) => {
        const query = `
            query GetEmployeeList {
                getEmployeeList {
                    id
                    name
                    age
                    job
                    language
                    pay
                }
            }
        `;
        try {
            const data = await graphqlRequest(query);
            // Strawberry-graphql은 ID를 문자열로 반환하므로, 숫자형으로 변환해줍니다.
            return data.getEmployeeList.map((emp: any) => ({ ...emp, id: Number(emp.id) }));
        } catch (e: any) {
            return thunkAPI.rejectWithValue(`전체 조회 실패: ${e.message}`);
        }
    }
);

// 단일 조회
export const fetchEmployeeInfoById = createAsyncThunk<EmployeeInfo, number, { rejectValue: string }>(
    "emp/fetchEmployeeInfoById",
    async (input, thunkAPI) => {
        const query = `
            query GetEmployeeById($input: Int!) {
                getEmployeeById(input: $input) {
                    id
                    name
                    age
                    job
                    language
                    pay
                }
            }
        `;
        try {
            const data = await graphqlRequest(query, { input });
            // Strawberry-graphql은 ID를 문자열로 반환하므로, 숫자형으로 변환해줍니다.
            return {...data.getEmployeeById, id:Number(data.getEmployeeById.id)};
        } catch (e: any) {
            return thunkAPI.rejectWithValue(`단일 조회 실패: ${e.message}`);
        }
    }
);

// 직원 등록
export const registerEmployeeInfo = createAsyncThunk<EmployeeInfo, Omit<EmployeeInfo, 'id'>, { rejectValue: string }>(
    "emp/registerEmployeeInfo",
    async (employeeInput, thunkAPI) => {
        // id 필드를 제거하고, age와 pay를 숫자로 변환합니다.
        const { id, age, pay, ...rest } = employeeInput as EmployeeInfo; // 'id'는 무시하고, 'age', 'pay'는 문자열 가능성이 있으므로 변환
        const processedInput = {
            ...rest,
            age: Number(age),
            pay: Number(pay),
        };

        const mutation = `
            mutation RegisterEmployee($input: EmployeeInput!) {
                registerEmployee(input: $input) {
                    id
                    name
                    age
                    job
                    language
                    pay
                }
            }
        `;
        try {
            const data = await graphqlRequest(mutation, { input: processedInput });
            const newEmp = data.registerEmployee;
            // ID를 숫자형으로 변환
            return { ...newEmp, id: Number(newEmp.id) };
        } catch (e: any) {
            return thunkAPI.rejectWithValue(`직원 등록 실패: ${e.message}`);
        }
    }
);

// 직원 정보 수정
export const putEmployeeInfoById = createAsyncThunk<EmployeeInfo, EmployeeInfo, { rejectValue: string }>(
    "emp/putEmployeeInfoById",
    async (employee, thunkAPI) => {
        const { id, age, pay, ...rest } = employee;
        const processedInput = {
            ...rest,
            age: Number(age),
            pay: Number(pay),
        };

        const mutation = `
            mutation UpdateEmployee($id: ID!, $input: EmployeeInput!) {
                updateEmployee(id: $id, input: $input) {
                    id
                    name
                    age
                    job
                    language
                    pay
                }
            }
        `;
        try {
            const data = await graphqlRequest(mutation, { id: String(id), input: processedInput });
            const updatedEmp = data.updateEmployee;
            // ID를 숫자형으로 변환
            return { ...updatedEmp, id: Number(updatedEmp.id) };
        } catch (e: any) {
            return thunkAPI.rejectWithValue(`직원 수정 실패: ${e.message}`);
        }
    }
);

// 직원 삭제
export const deleteEmployeeInfoById = createAsyncThunk<number, number, { rejectValue: string }>(
    "emp/deleteEmployeeInfoById",
    async (id, thunkAPI) => {
        const mutation = `
            mutation DeleteEmployee($id: ID!) {
                deleteEmployee(id: $id)
            }
        `;
        try {
            // GraphQL API가 삭제된 ID를 반환하지만, 요청에 사용된 ID를 그대로 사용하여 리듀서의 일관성을 유지합니다.
            await graphqlRequest(mutation, { id: String(id) });
            return id;
        } catch (e: any) {
            return thunkAPI.rejectWithValue(`직원 삭제 실패: ${e.message}`);
        }
    }
);

// 이 예제에서는 클라이언트 측에서 처리하므로 해당 Thunk는 제거하거나 주석 처리합니다.
// export const fetchEmployeeInfoById = ...
