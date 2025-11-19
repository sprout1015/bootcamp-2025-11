import React, {useMemo} from 'react';
import type {EmployeeInfo} from "@/components/Main";

interface InfoTableProps {
    infoList: EmployeeInfo[];
    selectedId?: number; // null 체크
}

const InfoTable = ({ infoList, selectedId }: InfoTableProps) => {
    // --- useMemo를 사용한 값 메모이제이션 ---
    // useMemo는 복잡한 연산의 결과값을 캐싱하여 성능을 최적화할 때 사용됩니다.
    // 의존성 배열([selectedId, infoList])의 값이 변경될 때만 내부 함수가 다시 실행됩니다.
    // 현재 코드에서는 단순히 infoList를 반환하고 있지만, 만약 infoList를 기반으로 복잡한 계산이 필요하다면
    // useMemo를 사용하는 것이 매우 효과적입니다.
    const dataList = useMemo<EmployeeInfo[]>(()=>
        infoList, [selectedId, infoList]
    );

    // 데이터가 없으면 메시지를 표시합니다.
    if (dataList.length === 0) return <p>No data available</p>;

    // --- 동적 테이블 헤더 생성 ---
    // 데이터의 첫 번째 객체에서 key들을 추출하여 테이블의 헤더(<th>)를 동적으로 생성합니다.
    // 'id' 필드는 화면에 표시할 필요가 없으므로 filter를 통해 제외합니다.
    // 이렇게 하면 데이터 구조가 변경되어도 코드를 수정할 필요가 없습니다.
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
            {/* --- 선택된 데이터만 필터링하여 행(Row) 렌더링 --- */}
            {dataList
                // 부모로부터 받은 selectedId와 일치하는 id를 가진 직원 정보만 필터링합니다.
                .filter((item)=> item.id == selectedId)
                // 필터링된 결과를 map으로 순회하여 테이블의 행(<tr>)과 셀(<td>)을 생성합니다.
                .map((item) => (
                <tr
                    key={item.id}
                    // 선택된 행에만 다른 배경색과 굵은 글씨를 적용하는 조건부 스타일링입니다.
                    style={{
                        backgroundColor: selectedId === item.id ? '#f0f8ff' : 'white',
                        fontWeight: selectedId === item.id ? 'bold' : 'normal',
                    }}
                >
                    {/* 추출된 key들을 순회하며 각 key에 해당하는 값을 동적으로 출력합니다. */}
                    {keys.map((key) => (
                        <td key={key} style={tdStyle}>
                            {/* item[key]와 같이 객체의 속성에 동적으로 접근합니다. */}
                            {/* 'as keyof EmployeeInfo'는 TypeScript에게 key가 EmployeeInfo 타입의 키 중 하나임을 알려줍니다. */}
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
