#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
AWS 技术支持案例管理工具使用示例
"""

from aws_support_case import AWSSupportCaseManager

def main():
    """主函数，演示AWS技术支持案例管理工具的使用"""
    
    # 初始化案例管理器
    case_manager = AWSSupportCaseManager()
    
    # 示例1：创建新案例
    # print("创建新的技术支持案例...")
    # new_case = case_manager.create_case(
    #     service='amazon-elastic-compute-cloud-linux',
    #     category='other',
    #     severity='low',
    #     subject='EC2实例无法启动',
    #     description='我的EC2实例状态显示为"pending"超过30分钟，无法正常启动。实例ID: i-1234567890abcdef0',
    #     language='zh',
    #     issue_type='technical'
    # )
    # case_id = new_case.get('caseId')
    # print(f"案例创建成功，案例ID: {case_id}")
    
    # # 示例2：向案例添加通信
    # print("\n向案例添加最新情况...")
    # case_manager.add_communication(
    #     case_id,
    #     '我已经尝试重启实例，但问题仍然存在。请提供进一步的帮助。'
    # )
    # print("通信添加成功")
    
    # # 示例3：获取案例详情
    # print("\n获取案例详情...")
    # case_details = case_manager.get_case_details(case_id)
    # print(f"案例状态: {case_details.get('status')}")
    # print(f"案例主题: {case_details.get('subject')}")
    
    # # 示例4：关闭案例
    print("\n关闭案例...")
    case_id = 'case-890717383483-mczh-2025-184a8619767dbb6e'
    case_manager.update_case_status(case_id, 'resolved')
    print("案例已关闭")
    
    # 示例5：重新打开案例
    print("\n重新打开案例...")
    case_manager.update_case_status(case_id, 'reopened')
    print("案例已重新打开")
    
    # 示例6：列出所有未解决的案例
    print("\n列出所有未解决的案例...")
    open_cases = case_manager.list_cases()
    print(f"共有 {len(open_cases)} 个未解决的案例:")
    for case in open_cases:
        print(f"  - 案例ID: {case.get('caseId')}, 主题: {case.get('subject')}")

if __name__ == "__main__":
    main()
