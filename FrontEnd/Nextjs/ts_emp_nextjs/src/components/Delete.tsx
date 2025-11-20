'use client';

import {useEffect} from 'react';
import {useDispatch, useSelector} from 'react-redux';
import {deleteEmployeeInfoById} from '@/redux/api/employeeAPI';
import {handleMode} from '@/redux/slice/employeeSlice';
import {RootDispatch, RootState} from '@/redux/employStore';

const Delete = () => {
    const dispatch = useDispatch<RootDispatch>();
    const { mode, selectedId, infoList } = useSelector((state: RootState) => state.empStore);

    useEffect(() => {
        // 이 console.log는 mode, selectedId 등이 변경될 때마다 실행되어 디버깅에 도움을 줍니다.
        console.log(`Effect triggered: mode=${mode}, selectedId=${selectedId}`);

        if (mode === 'delete') {
            if (selectedId) {
                const targetInfo = infoList.find(target => target.id === selectedId);
                if (targetInfo) {
                    // 사용자에게 삭제 여부 확인
                    if (window.confirm(`${targetInfo.name} 직원을 삭제하시겠습니까?`)) {
                        dispatch(deleteEmployeeInfoById(selectedId));
                    } else {
                        // 사용자가 '취소'를 누르면 모드를 'default'로 되돌림
                        dispatch(handleMode('default'));
                    }
                } else {
                    // 선택된 ID에 해당하는 직원이 목록에 없는 경우
                    alert("삭제할 직원을 찾을 수 없습니다.");
                    dispatch(handleMode('default'));
                }
            } else {
                // 직원을 선택하지 않고 'delete'를 누른 경우
                alert("삭제할 직원을 선택해주세요.");
                dispatch(handleMode('default'));
            }
        }
    }, [mode, selectedId, infoList, dispatch]);

    // 이 컴포넌트는 UI를 렌더링하지 않음
    return null;
};

export default Delete;
