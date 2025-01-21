import os
import json

def read_config():
    # 获取当前文件所在目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # 获取上级目录
    parent_dir = os.path.dirname(current_dir)
    # 构建config.json的完整路径
    config_path = os.path.join(parent_dir, 'config.json')
    
    try:
        # 读取并解析JSON文件
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        # 打印JSON内容
        print(json.dumps(config, ensure_ascii=False, indent=2))
    except FileNotFoundError:
        print(f"错误：在{parent_dir}目录下未找到config.json文件")
    except json.JSONDecodeError:
        print("错误：config.json文件格式不正确")
    except Exception as e:
        print(f"发生错误：{str(e)}")

if __name__ == "__main__":
    read_config()