import React, {useMemo} from 'react';
import {EmployeeInfo, useEmployee} from "@/context/EmployeeContext";

const InfoTable = () => {
    const {infoList, selectedId} = useEmployee();
    const dataList = useMemo<EmployeeInfo[]>    (()=>
        infoList, [selectedId, infoList]
    );

    if (dataList.length === 0) return <p>No data available</p>;

    // 첫 번째 객체에서 key 목록 추출 (id는 제외)
    const keys = Object.keys(dataList[0])
                            .filter((key) => key !== 'id');

    return (
        <table style={{ borderCollapse: 'collapse', width: '100%' }}>
            <thead>
            <tr>
                {keys.map((key) => (
                    <th key={key} style={thStyle}>
                        {key}
                    </th>
                ))}
            </tr>
            </thead>
            <tbody>
            {dataList
                .filter((item)=> item.id == selectedId)
                .map((item) => (
                <tr
                    key={item.id}
                    style={{
                        backgroundColor: selectedId === item.id ? '#f0f8ff' : 'white',
                        fontWeight: selectedId === item.id ? 'bold' : 'normal',
                    }}
                >
                    {keys.map((key) => (
                        <td key={key} style={tdStyle}>
                            {item[key as keyof EmployeeInfo]}
                        </td>
                    ))}
                </tr>
            ))}
            </tbody>
        </table>
    );
};


// 스타일 정의
const thStyle: React.CSSProperties = {
    border: '1px solid #ccc',
    padding: '8px',
    backgroundColor: '#d2fff2',
    textAlign: 'left',
    color: 'black'
};

const tdStyle: React.CSSProperties = {
    border: '1px solid #ccc',
    padding: '8px',
    color: 'black'
};


export default InfoTable;