from django import template
 
register = template.Library()
 
@register.filter
def format_with_commas(value):
    """数値にカンマを追加するフィルター"""
    try:
        value = float(value)  # Decimal を float に変換
        return "{:,.0f}".format(value)  # 小数点なしのカンマ区切りフォーマット
    except (ValueError, TypeError):
        return value  # 数値以外ならそのまま返す
 