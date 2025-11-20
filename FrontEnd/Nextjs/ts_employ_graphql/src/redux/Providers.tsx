'use client';

import React from 'react';
import {Provider} from "react-redux";
import {employStore} from "@/redux/employStore";

const Providers = ({children}:{children:React.ReactNode}) => {
    return (
        <Provider store={employStore}>
            {children}
        </Provider>
    );
};

export default Providers;