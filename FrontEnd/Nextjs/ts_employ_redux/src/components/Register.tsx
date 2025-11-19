import React, {useState} from 'react';
import {formStyle, inputStyle, labelStyle} from "@/util/Style";
import {useDispatch} from "react-redux";
import {EmployeeInfo, handleRegisterEmployee} from "@/redux/employeeSlice";

const initialInfo: EmployeeInfo = {
    id:0, name:'', job:'', pay: 0, age: 0, language: ''
}

const Register = () => {
    const dispatch = useDispatch();

    const [info, setInfo] = useState<EmployeeInfo>(initialInfo);

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>)=> {
        const { name, value } = e.target;
        setInfo(prev => ({...prev, [name]:value}))
    }

    const handleSubmit = (e: React.FormEvent<HTMLFormElement>)=> {
        e.preventDefault();
        dispatch(handleRegisterEmployee(info));
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