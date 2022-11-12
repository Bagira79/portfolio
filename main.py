from data_parsing import parsing
from data_analysis import data_analysis
from total_report import reporting
url = 'https://dbfiddle.uk/?rdbms=sqlserver_2017&fiddle=39bc85a5dbd3202671979645068f8ce0&hide=1'

new_data = parsing(url)
data_gross_profit, data_price_markup, total_remains, lost_funds, additional_funds, data_profit_manufacturer, m_2000, m_2001, m_2002, m_2003 = data_analysis(new_data)
reporting(data_gross_profit, data_price_markup, total_remains, lost_funds, additional_funds, data_profit_manufacturer, m_2000, m_2001, m_2002, m_2003)
print('Отчет  total.pdf сформирован')
