import {createAsyncThunk} from "@reduxjs/toolkit";
import {EmployeeInfo} from "@/redux/slice/employeeSlice";
import axios from "axios";

const PROTOCOL = "http";
const DOMAIN = "localhost";
const PORT = "3001";

const API_URL = `${PROTOCOL}://${DOMAIN}:${PORT}`;

// GET methods
// 전체 조회
export const fetchEmployeeInfoList
    // 타입,
    = createAsyncThunk<EmployeeInfo[], void, {rejectValue: string}>(
        "emp/fetchEmployeeInfoList",
        async (_, thunkAPI) => {
                try{
                    const response = await axios.get(`${API_URL}/app/emp`)
                    return  response.data;
                } catch (e){
                    return thunkAPI.rejectWithValue("전체 조회 실패")
                }
        }
)

// 단일 조회
export const fetchEmployeeInfoById
    // 타입,
    = createAsyncThunk<EmployeeInfo, number, {rejectValue: string}>(
    "emp/fetchEmployeeInfoById",
    async (id, thunkAPI) => {
        try{
            const response = await axios.get(`${API_URL}/app/emp/${id}`)
            return  response.data;
        } catch (e){
            return thunkAPI.rejectWithValue("단일 조회 실패")
        }
    }
)

// POST method
// 추가
export const registerEmployeeInfo
    // 타입,
    = createAsyncThunk<EmployeeInfo, EmployeeInfo, {rejectValue: string}>(
    "emp/registerEmployeeInfo",
    async (employInfo, thunkAPI) => {
        try{
            const response = await axios.post<EmployeeInfo>(`${API_URL}/app/emp`, employInfo)
            return  response.data;
        } catch (e){
            return thunkAPI.rejectWithValue("추가 실패")
        }
    }
)

// Put method
// 단일 수정
export const putEmployeeInfoById
    // 타입,
    = createAsyncThunk<EmployeeInfo, EmployeeInfo, {rejectValue: string}>(
    "emp/putEmployeeInfoById",
    async (emp, thunkAPI) => {
        try{
            const response = await axios.put<EmployeeInfo>(`${API_URL}/app/emp/${emp.id}`,emp)
            return  response.data;
        } catch (e){
            return thunkAPI.rejectWithValue("수정 실패")
        }
    }
)

// DELETE method
// 단일 삭제
export const deleteEmployeeInfoById
    // 타입,
    = createAsyncThunk<number, number, {rejectValue: string}>(
    "emp/deleteEmployeeInfoById",
    async (id, thunkAPI) => {
        try{
            const response = await axios.delete(`${API_URL}/app/emp/${id}`)
            return  response.data;
        } catch (e){
            return thunkAPI.rejectWithValue("삭제 실패")
        }
    }
)