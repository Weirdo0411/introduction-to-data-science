import pandas as pd
import glob
import os
import re
from snownlp import SnowNLP


TYPE_MAPPING = {
    'AI复活': '社会伦理',
    'AI取代我': '社会伦理',
    '罗翔': '社会伦理',
    '没有工作': '社会伦理', 

    '黑马': '知识科普',
    '清华': '知识科普',
    '官方课程': '知识科普', 

    '北京欢迎你': '技术应用',
    '霍格沃兹': '技术应用',   
    '模仿': '技术应用'        
}

ETHICS_KEYWORDS = {
    '伦理/法律': ['尊重', '逝者', '同意', '版权', '底线', '侵权', '失业', '取代', '骗子', '诈骗', '犯罪', '法律'],
    '情绪/感受': ['恐怖', '吓人', '害怕', '诡异', '感动', '泪目', '震撼', '牛逼', '强', '好听', '像'],
    '技术/产业': ['AI', '算法', '模型', '算力', '画质', '修复', '教程', '学习', '显卡', 'GPT', 'Sora']
}


def clean_grade(val):
    match = re.search(r'\d+', str(val))
    return int(match.group()) if match else 0

def clean_ip(val):
    if pd.isna(val): return "未知"
    return str(val).strip().replace('中国', '')

def get_sentiment_score(text):
    text = str(text)
    if not text or len(text.strip()) < 2: return 0.5
    try:
        return SnowNLP(text).sentiments
    except:
        return 0.5

def extract_topic(text):
    text = str(text)
    for category, keywords in ETHICS_KEYWORDS.items():
        for keyword in keywords:
            if keyword in text:
                return category
    return '一般评论'


def main():
    print("[开始] 正在读取并合并 10 个数据文件...")
    
    # 获取所有csv文件
    all_files = glob.glob("*.csv")
    
    # 排除掉输出结果文件，防止递归合并
    if 'final_analysis_result.csv' in all_files:
        all_files.remove('final_analysis_result.csv')

    df_list = []
    
    for filename in all_files:
        # 尝试匹配类别
        video_type = '其他'
        for key, type_name in TYPE_MAPPING.items():
            if key in filename:
                video_type = type_name
                break
        
        print(f"   -> 读取: {filename} | 归类为: [{video_type}]")

        try:
            # 读取文件 (尝试两种编码)
            try:
                temp_df = pd.read_csv(filename, encoding='utf-8-sig')
            except:
                temp_df = pd.read_csv(filename, encoding='gbk')

            # 打标签
            temp_df['video_type'] = video_type
            temp_df['source_filename'] = filename 
            
            df_list.append(temp_df)
            
        except Exception as e:
            print(f"[错误] 读取 {filename} 失败: {e}")

    if not df_list:
        print("[错误] 没有找到任何csv文件！")
        return

    # 合并
    df = pd.concat(df_list, axis=0, ignore_index=True)
    print(f"[合并] 共合并 {len(df)} 条原始数据。")
    print("[处理] 正在进行数据清洗、情感计算和话题提取 (可能需要几分钟)...")

    # 清洗重复数据
    if '评论ID' in df.columns:
        df.drop_duplicates(subset=['评论ID'], inplace=True)
    
    # 清洗列名
    df.columns = [c.strip() for c in df.columns]

    # 应用清洗函数
    df['level_num'] = df['用户等级'].apply(clean_grade)
    df['ip_clean'] = df['IP属地'].apply(clean_ip)
    df['content_str'] = df['评论内容'].astype(str).fillna('')
    
    # 过滤太短的评论
    df = df[df['content_str'].str.len() > 1]

    # 核心计算 (情感 + 话题)
    df['sentiment'] = df['content_str'].apply(get_sentiment_score)
    df['topic_tag'] = df['content_str'].apply(extract_topic)

    # 导出
    output_file = 'final_analysis_result.csv'
    df.to_csv(output_file, index=False, encoding='utf-8-sig')
    
    print("-" * 30)
    print(f"[成功] 处理完毕！")
    print(f"       有效数据量: {len(df)} 条")
    print(f"       包含类别: {df['video_type'].unique()}")
    print(f"       结果已保存为: {output_file}")
    print("-" * 30)
    print("现在请打开 visualization.ipynb 重新运行所有图表代码即可！")

if __name__ == "__main__":
    main()