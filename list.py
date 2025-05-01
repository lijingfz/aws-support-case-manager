from aws_support_case import AWSSupportCaseManager
import json

def get_case_details_by_id(case_id):
    """
    根据案例ID查询AWS技术支持案例的详细信息
    
    参数:
        case_id (str): AWS支持案例的ID
        
    返回:
        dict: 包含案例详细信息的字典
    """
    try:
        # 初始化案例管理器
        case_manager = AWSSupportCaseManager()
        
        # 获取案例详情
        case_details = case_manager.get_case_details(case_id)
        
        # 打印案例详情
        print(f"案例ID: {case_details.get('caseId')}")
        print(f"显示ID (Display ID): {case_details.get('displayId')}")  # 添加显示ID
        print(f"主题: {case_details.get('subject')}")
        print(f"状态: {case_details.get('status')}")
        print(f"服务: {case_details.get('serviceCode')}")
        print(f"类别: {case_details.get('categoryCode')}")
        print(f"严重程度: {case_details.get('severityCode')}")
        print(f"提交时间: {case_details.get('timeCreated')}")
        
        # 打印通信历史
        if 'recentCommunications' in case_details:
            print("\n通信历史:")
            for comm in case_details['recentCommunications'].get('communications', []):
                print(f"时间: {comm.get('timeCreated')}")
                print(f"内容: {comm.get('body')}")
                print("-" * 50)
        
        return case_details
        
    except Exception as e:
        print(f"获取案例详情时出错: {str(e)}")
        return None

if __name__ == "__main__":
    # 使用示例
    case_id = "case-890717383483-mczh-2025-184a8619767dbb6e"  # 替换为您的实际案例ID
    case_details = get_case_details_by_id(case_id)
    
    # 如果需要，可以将结果保存为JSON文件
    if case_details:
        with open(f"case_{case_details.get('displayId', case_id)}_details.json", "w", encoding="utf-8") as f:
            json.dump(case_details, f, ensure_ascii=False, indent=4)
            print(f"案例详情已保存到 case_{case_details.get('displayId', case_id)}_details.json")