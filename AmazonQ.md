# AWS 技术支持案例管理工具

## 项目概述

这个项目是一个使用Python boto3开发的AWS技术支持案例管理工具，可以帮助用户创建、更新和管理AWS技术支持案例。

## 主要功能

1. **创建AWS技术支持案例**
   - 支持指定服务（如EC2、S3等）
   - 支持指定问题类别
   - 支持指定严重程度（低、中、高、紧急等）
   - 支持设置案例描述
   - 支持选择语言（默认中文）
   - 支持设置问题类型（默认技术问题）

2. **更新案例状态**
   - 支持关闭案例（resolved）
   - 支持重新打开案例（reopened）

3. **更新案例通信**
   - 支持向案例添加最新情况更新
   - 支持追加问题描述或解决方案

4. **查询案例信息**
   - 支持获取单个案例的详细信息
   - 支持列出所有未解决的案例

## 项目结构

```
awscase/
├── README.md           # 项目说明文档
├── requirements.txt    # 项目依赖
├── aws_support_case.py # 主要实现代码
└── example.py          # 使用示例
```

## 安装与配置

1. 安装依赖：
   ```
   pip install -r requirements.txt
   ```

2. 确保已配置AWS凭证：
   - 通过AWS CLI配置（`aws configure`）
   - 或设置环境变量（AWS_ACCESS_KEY_ID、AWS_SECRET_ACCESS_KEY）
   - 或使用IAM角色（如在EC2实例上）

## 使用方法

1. **创建案例**：
   ```python
   from aws_support_case import AWSSupportCaseManager
   
   case_manager = AWSSupportCaseManager()
   new_case = case_manager.create_case(
       service='ec2',
       category='instance',
       severity='low',
       subject='EC2实例无法启动',
       description='详细描述...',
       language='zh',
       issue_type='technical'
   )
   case_id = new_case.get('caseId')
   ```

2. **更新案例状态**：
   ```python
   # 关闭案例
   case_manager.update_case_status(case_id, 'resolved')
   
   # 重新打开案例
   case_manager.update_case_status(case_id, 'reopened')
   ```

3. **添加案例通信**：
   ```python
   case_manager.add_communication(
       case_id,
       '我已经尝试重启实例，但问题仍然存在。请提供进一步的帮助。'
   )
   ```

4. **获取案例详情**：
   ```python
   case_details = case_manager.get_case_details(case_id)
   print(f"案例状态: {case_details.get('status')}")
   ```

5. **列出所有未解决的案例**：
   ```python
   open_cases = case_manager.list_cases()
   for case in open_cases:
       print(f"案例ID: {case.get('caseId')}, 主题: {case.get('subject')}")
   ```

## 注意事项

1. 使用此工具需要AWS账户具有创建和管理支持案例的权限
2. 建议使用Business或Enterprise级别的AWS支持计划，以获得完整的支持功能
3. 某些API调用可能会根据您的AWS支持计划级别受到限制
