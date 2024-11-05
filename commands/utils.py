import pandas as pd

def generate_markdown_table(df:pd.DataFrame):
    """
    生成包含 DataFrame 统计信息的 Markdown 表格。
    
    :param df: 输入的 DataFrame
    :return: 格式化的 Markdown 表格字符串
    """
    # 计算统计信息
    stats = df.describe().transpose()
    stats['Variable'] = stats.index
    stats = stats[['Variable', 'count', 'mean', 'std', 'min', 'max']]
    stats.columns = ['Variable', 'Obs', 'Mean', 'Std', 'Min', 'Max']
    
    # 转换为 Markdown 表格
    markdown_table = stats.to_markdown(index=False)
    return markdown_table