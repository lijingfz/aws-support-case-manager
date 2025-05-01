#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
AWS 技术支持案例管理工具

该模块提供创建、更新和管理AWS技术支持案例的功能。
"""

import boto3
import logging
from typing import Dict, Any, List, Optional

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class AWSSupportCaseManager:
    """AWS技术支持案例管理类"""
    
    def __init__(self, region_name: str = 'us-east-1'):
        """
        初始化AWS Support客户端
        
        Args:
            region_name: AWS区域名称，默认为us-east-1
        """
        self.support_client = boto3.client('support', region_name=region_name)
        logger.info(f"已初始化AWS Support客户端，区域: {region_name}")
    
    def create_case(self, 
                   service: str,
                   category: str, 
                   severity: str,
                   subject: str,
                   description: str,
                   language: str = 'zh',
                   issue_type: str = 'technical') -> Dict[str, Any]:
        """
        创建AWS技术支持案例
        
        Args:
            service: 服务名称，如'EC2', 'S3'等
            category: 问题类别
            severity: 严重程度，如'low', 'normal', 'high', 'urgent', 'critical'
            subject: 案例主题
            description: 案例详细描述
            language: 语言代码，默认为'zh'（中文）
            issue_type: 问题类型，默认为'technical'（技术问题）
            
        Returns:
            包含案例ID和其他信息的字典
        """
        try:
            response = self.support_client.create_case(
                subject=subject,
                serviceCode=service,
                severityCode=severity,
                categoryCode=category,
                communicationBody=description,
                language=language,
                issueType=issue_type
            )
            
            case_id = response.get('caseId')
            logger.info(f"成功创建案例，案例ID: {case_id}")
            return response
        except Exception as e:
            logger.error(f"创建案例失败: {str(e)}")
            raise
    
    def update_case_status(self, case_id: str, status: str) -> Dict[str, Any]:
        """
        更新案例状态（关闭或重新打开）
        
        Args:
            case_id: 案例ID
            status: 状态，可选值为'resolved'（关闭）或'reopened'（重新打开）
            
        Returns:
            API响应字典
        """
        if status.lower() not in ['resolved', 'reopened']:
            raise ValueError("状态必须是'resolved'（关闭）或'reopened'（重新打开）")
        
        try:
            if status.lower() == 'resolved':
                response = self.support_client.resolve_case(
                    caseId=case_id
                )
            else:
                # 使用add_communication_to_case方法重新打开案例
                response = self.support_client.add_communication_to_case(
                  caseId=case_id,
                  communicationBody="重新打开案例"
            )
            
            logger.info(f"成功将案例 {case_id} 状态更新为 {status}")
            return response
        except Exception as e:
            logger.error(f"更新案例状态失败: {str(e)}")
            raise
    
    def add_communication(self, case_id: str, body: str) -> Dict[str, Any]:
        """
        向案例添加通信（更新）
        
        Args:
            case_id: 案例ID
            body: 通信内容
            
        Returns:
            API响应字典
        """
        try:
            response = self.support_client.add_communication_to_case(
                caseId=case_id,
                communicationBody=body
            )
            
            logger.info(f"成功向案例 {case_id} 添加通信")
            return response
        except Exception as e:
            logger.error(f"添加案例通信失败: {str(e)}")
            raise
    
    def get_case_details(self, case_id: str) -> Dict[str, Any]:
        """
        获取案例详情
        
        Args:
            case_id: 案例ID
            
        Returns:
            案例详情字典
        """
        try:
            response = self.support_client.describe_cases(
                caseIdList=[case_id],
                includeResolvedCases=True
            )
            
            if response.get('cases'):
                logger.info(f"成功获取案例 {case_id} 详情")
                return response['cases'][0]
            else:
                logger.warning(f"未找到案例 {case_id}")
                return {}
        except Exception as e:
            logger.error(f"获取案例详情失败: {str(e)}")
            raise
    
    def list_cases(self, include_resolved: bool = False) -> List[Dict[str, Any]]:
        """
        列出所有案例
        
        Args:
            include_resolved: 是否包含已解决的案例，默认为False
            
        Returns:
            案例列表
        """
        try:
            response = self.support_client.describe_cases(
                includeResolvedCases=include_resolved
            )
            
            cases = response.get('cases', [])
            logger.info(f"成功获取案例列表，共 {len(cases)} 个案例")
            return cases
        except Exception as e:
            logger.error(f"获取案例列表失败: {str(e)}")
            raise


# 使用示例
if __name__ == "__main__":
    # 初始化案例管理器
    case_manager = AWSSupportCaseManager()
    
    # 示例1：创建新案例
    # new_case = case_manager.create_case(
    #     service='ec2',
    #     category='instance',
    #     severity='low',
    #     subject='EC2实例无法启动',
    #     description='我的EC2实例状态显示为"pending"超过30分钟，无法正常启动。实例ID: i-1234567890abcdef0',
    #     language='zh',
    #     issue_type='technical'
    # )
    # print(f"新案例ID: {new_case.get('caseId')}")
    
    # 示例2：更新案例状态（关闭案例）
    # case_manager.update_case_status('case-123456789012-myCaseId', 'resolved')
    
    # 示例3：重新打开案例
    # case_manager.update_case_status('case-123456789012-myCaseId', 'reopened')
    
    # 示例4：添加案例通信
    # case_manager.add_communication(
    #     'case-123456789012-myCaseId',
    #     '我已经尝试重启实例，但问题仍然存在。请提供进一步的帮助。'
    # )
    
    # 示例5：获取案例详情
    # case_details = case_manager.get_case_details('case-123456789012-myCaseId')
    # print(f"案例状态: {case_details.get('status')}")
    
    # 示例6：列出所有未解决的案例
    # open_cases = case_manager.list_cases()
    # for case in open_cases:
    #     print(f"案例ID: {case.get('caseId')}, 主题: {case.get('subject')}")
