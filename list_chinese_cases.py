import boto3
import json

def list_chinese_cases():
    client = boto3.client('support', region_name='us-east-1')
    
    # 获取所有案例，包括已解决的
    response = client.describe_cases(includeResolvedCases=True)
    cases = response.get('cases', [])
    
    # 处理分页
    while 'nextToken' in response:
        response = client.describe_cases(
            includeResolvedCases=True,
            nextToken=response['nextToken']
        )
        cases.extend(response.get('cases', []))
    
    chinese_cases = []
    
    for case in cases:
        # 检查案例的语言是否为中文
        # 有些案例可能没有明确的语言字段，我们可以通过其他方式判断
        language = case.get('language', '')
        communications = case.get('recentCommunications', {}).get('communications', [])
        
        is_chinese = False
        
        # 检查语言字段
        if language and ('zh' in language.lower() or 'chinese' in language.lower()):
            is_chinese = True
        
        # 如果没有明确的语言字段，检查通信内容是否包含中文字符
        if not is_chinese and communications:
            for comm in communications:
                body = comm.get('body', '')
                # 简单检查是否包含常见中文字符范围
                if any('\u4e00' <= char <= '\u9fff' for char in body):
                    is_chinese = True
                    break
        
        if is_chinese:
            chinese_cases.append({
                'caseId': case.get('caseId'),
                'displayId': case.get('displayId'),
                'subject': case.get('subject'),
                'status': case.get('status'),
                'timeCreated': case.get('timeCreated'),
                'language': language
            })
    
    # 按创建时间排序
    chinese_cases.sort(key=lambda x: x.get('timeCreated', ''), reverse=True)
    
    return chinese_cases

if __name__ == "__main__":
    cases = list_chinese_cases()
    
    if cases:
        print(f"找到 {len(cases)} 个中文支持案例:")
        print("-" * 80)
        
        for case in cases:
            print(f"显示ID: {case['displayId']}")
            print(f"案例ID: {case['caseId']}")
            print(f"主题: {case['subject']}")
            print(f"状态: {case['status']}")
            print(f"创建时间: {case['timeCreated']}")
            print(f"语言: {case.get('language', '未指定')}")
            print("-" * 80)
    else:
        print("未找到任何中文支持案例。")
