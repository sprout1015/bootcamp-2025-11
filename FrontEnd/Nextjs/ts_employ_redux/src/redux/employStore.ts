import {configureStore} from "@reduxjs/toolkit";
import employeeSlice from "@/redux/employeeSlice";

export const employStore = configureStore(
    {
        reducer: {
            empStore: employeeSlice,
        }
    }
)

// state
export type RootState = ReturnType<typeof employStore.getState>;
// action
export type RootDispatch = typeof employStore.dispatch;