import React, {useEffect, useState} from 'react';
import {formStyle, inputStyle, labelStyle} from "@/util/Style";
import {EmployeeInfo, handleUpdateEmployee} from "@/redux/employeeSlice";
import {useDispatch, useSelector} from "react-redux";
import {RootState} from "@/redux/employStore";


const initialInfo: EmployeeInfo = {
    id:0, name:'', job:'', pay: 0, age: 0, language: ''
}

const Update = () => {
    const dispatch = useDispatch();
    const { infoList, selectedId } = useSelector((state:RootState) => state.empStore)

    const [infoToUpdate, setInfoToUpdate] = useState<EmployeeInfo>(initialInfo);

    // useEffect (SelectedId 변경에 따른 상태 감지용)
    useEffect(() => {
        const foundInfo = infoList.find(info => info.id === selectedId);
        if(foundInfo)
            setInfoToUpdate(foundInfo);
    }, [infoList, selectedId]);

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>)=> {
        const { name, value } = e.target;
        setInfoToUpdate(prev => ({...prev, [name]:value}))
    }

    const handleSubmit = (e: React.FormEvent<HTMLFormElement>)=> {
        e.preventDefault();
        dispatch(handleUpdateEmployee(infoToUpdate));
    }

    return (
        <form style={formStyle} onSubmit={handleSubmit}>
            <label style={labelStyle} >
                Name
                <input type="text" name="name" onChange={handleChange} style={inputStyle} value={infoToUpdate.name} disabled/>
            </label>
            <label style={labelStyle} >
                Age
                <input type="number" name="age" onChange={handleChange} style={inputStyle} value={infoToUpdate.age} min={1} required/>
            </label>
            <label style={labelStyle} >
                Job
                <input type="text" name="job" onChange={handleChange} style={inputStyle} value={infoToUpdate.job} />
            </label>
            <label style={labelStyle} >
                Language
                <input type="text" name="language" onChange={handleChange} style={inputStyle} value={infoToUpdate.language} />
            </label>
            <label style={labelStyle} >
                Pay
                <input type="number" name="pay" min={0} onChange={handleChange} style={inputStyle}  value={infoToUpdate.pay} required/>
            </label>
            <button type="submit">등록</button>
        </form>
    );
};

export default Update;