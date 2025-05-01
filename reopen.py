#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from aws_support_case import AWSSupportCaseManager

def reopen_resolved_case(case_id):
    """
    重新打开一个已解决的AWS支持案例
    
    Args:
        case_id: 要重新打开的案例ID
        
    Returns:
        API响应结果
    """
    # 初始化AWS支持案例管理器
    case_manager = AWSSupportCaseManager()
    
    # 获取案例详情，确认案例状态
    case_details = case_manager.get_case_details(case_id)
    
    if not case_details:
        print(f"未找到案例 {case_id}")
        return None
    
    # 检查案例状态
    current_status = case_details.get('status')
    print(f"案例当前状态: {current_status}")
    
    if current_status.lower() == 'resolved':
        # 重新打开已解决的案例
        print(f"正在重新打开案例 {case_id}...")
        response = case_manager.update_case_status(case_id, 'reopened')
        
        # 可选：添加重新打开的原因
        case_manager.add_communication(
            case_id,
            "重新打开案例的原因：问题仍然存在，需要进一步技术支持。"
        )
        
        print(f"案例 {case_id} 已成功重新打开")
        return response
    else:
        print(f"案例 {case_id} 当前状态为 {current_status}，不需要重新打开")
        return None

if __name__ == "__main__":
    # 使用示例 - 替换为实际的案例ID
    case_id = "case-890717383483-mczh-2025-184a8619767dbb6e"  # 替换为您的实际案例ID
    reopen_resolved_case(case_id)