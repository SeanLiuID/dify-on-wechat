import json

def parse_chat_message_str(message_str):
    """
    将ChatMessage的字符串表示转换为JSON格式
    
    Args:
        message_str (str): ChatMessage的字符串表示
        
    Returns:
        dict: 包含消息属性的字典
    """
    # 移除开头的"ChatMessage: "
    if message_str.startswith("ChatMessage: "):
        message_str = message_str[len("ChatMessage: "):]
    
    # 解析属性
    result = {}
    pairs = message_str.split(", ")
    
    for pair in pairs:
        if "=" in pair:
            key, value = pair.split("=", 1)
            # 处理None值
            if value == "None":
                result[key] = None
            # 处理布尔值
            elif value.lower() == "true":
                result[key] = True
            elif value.lower() == "false":
                result[key] = False
            # 处理数字
            elif value.isdigit():
                result[key] = int(value)
            else:
                result[key] = value
    
    return result

def to_json_str(message_str):
    """
    将消息字符串转换为JSON字符串，自动识别XML和ChatMessage格式
    
    Args:
        message_str (str): 消息字符串，可以是XML格式或ChatMessage格式
        
    Returns:
        str: JSON字符串
    """
    # 检查是否为XML格式
    if message_str.strip().startswith('<?xml') or ('<' in message_str and '>' in message_str):
        return parse_wechat_xml_message(message_str)
    else:
        # 默认作为ChatMessage格式处理
        result = parse_chat_message_str(message_str)
        return json.dumps(result, ensure_ascii=False, indent=2)

def parse_wechat_xml_message(xml_str):
    """
    将微信XML消息转换为JSON格式，自动适应XML的结构层级和字段名称
    
    Args:
        xml_str (str): 微信XML消息字符串
        
    Returns:
        str: JSON字符串
    """
    import xml.etree.ElementTree as ET
    from io import StringIO
    
    def parse_element(element):
        """
        递归解析XML元素
        
        Args:
            element: XML元素
            
        Returns:
            dict: 包含元素内容的字典
        """
        result = {}
        
        # 处理元素的属性
        if element.attrib:
            result['@attributes'] = dict(element.attrib)
        
        # 处理子元素
        children = list(element)
        if children:
            child_dict = {}
            for child in children:
                child_name = child.tag
                child_result = parse_element(child)
                
                # 处理同名子元素
                if child_name in child_dict:
                    if isinstance(child_dict[child_name], list):
                        child_dict[child_name].append(child_result)
                    else:
                        child_dict[child_name] = [child_dict[child_name], child_result]
                else:
                    child_dict[child_name] = child_result
            
            result.update(child_dict)
        
        # 处理元素的文本内容
        if element.text and element.text.strip():
            if result:
                result['#text'] = element.text.strip()
            else:
                result = element.text.strip()
        
        return result
    
    # 解析XML字符串
    tree = ET.parse(StringIO(xml_str))
    root = tree.getroot()
    
    # 递归解析XML树
    result = {root.tag: parse_element(root)}
    
    return json.dumps(result, ensure_ascii=False, indent=2)