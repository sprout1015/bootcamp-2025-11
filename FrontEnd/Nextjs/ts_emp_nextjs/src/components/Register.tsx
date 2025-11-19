import React, {useEffect, useState} from 'react';
import {formStyle, inputStyle, labelStyle} from "@/util/Style";
import {useDispatch, useSelector} from "react-redux";
import {EmployeeInfo} from "@/redux/slice/employeeSlice";
import {RootDispatch, RootState} from "@/redux/employStore";
import {registerEmployeeInfo} from "@/redux/api/employeeAPI";

const initialInfo: EmployeeInfo = {
    id:0, name:'', job:'', pay: 0, age: 0, language: ''
}

const Register = () => {
    const {infoList} = useSelector((state:RootState) => state.empStore);
    const dispatch = useDispatch<RootDispatch>();

    const [info, setInfo] = useState<EmployeeInfo>(initialInfo);

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>)=> {
        const { name, value } = e.target;
        setInfo(prev => ({...prev, [name]:value}))
    }

    const handleSubmit = (e: React.FormEvent<HTMLFormElement>)=> {
        e.preventDefault();
        // 기존 extra
        // dispatch(handleRegisterEmployee(info));
        if (!info.name) {
            alert("이름은 필수입니다.")
            return;
        }
        if (!info.age || Number(info.age) < 0) {
            alert("나이는 필수입니다.")
            return;
        }
        if (!info.pay || Number(info.pay) < 0) {
            alert("급여는 필수입니다.")
            return;
        }
        if (infoList.some(item => item.name === info.name)) {
            alert("이미 존재하는 이름입니다.")
            return;
        }
        dispatch(registerEmployeeInfo(info));
    }

    const checkValidity = (e: React.InvalidEvent<HTMLInputElement>)=> {
        const targetName = e.target.name;
        // 유효성 어쩌고
        switch (targetName) {

        }
    }

    return (
        <form style={formStyle} onSubmit={handleSubmit}>
            <label style={labelStyle} >
                Name
                <input type="text" name="name" onChange={handleChange} style={inputStyle} required onInvalid={checkValidity}/>
            </label>
            <label style={labelStyle} >
                Age
                <input type="number" name="age" onChange={handleChange} style={inputStyle} min={1} required onInvalid={checkValidity}/>
            </label>
            <label style={labelStyle} >
                Job
                <input type="text" name="job" onChange={handleChange} style={inputStyle}  />
            </label>
            <label style={labelStyle} >
                Language
                <input type="text" name="language" onChange={handleChange} style={inputStyle}  />
            </label>
            <label style={labelStyle} >
                Pay
                <input type="number" name="pay" min={0} onChange={handleChange} style={inputStyle}  required onInvalid={checkValidity}/>
            </label>
            <button type="submit">등록</button>
        </form>
    );
};

export default Register;