'''
Bài Tập Thực Hành Trực Quan Hóa Dữ Liệu: COVID-19 tại Đông Nam Á
Chuẩn bị Dữ liệu (Data Preparation)
Hãy chạy đoạn code sau để tự động lấy dữ liệu từ Our World in Data, lọc các quốc gia Đông Nam Á và xử lý sơ bộ các giá trị thiếu (NaN).

'''

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Prepare data
def load_data():
    """
    Tải và xử lý dữ liệu COVID-19 từ Our World in Data.
    Trả về DataFrame đã được lọc theo khu vực ASEAN và giai đoạn 2021-2022.
    """
    sns.set_theme(style="whitegrid")
 
    url = 'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv'
    print("Đang tải dữ liệu...")
    df_raw = pd.read_csv(url)
 
    asean_countries = ['Vietnam', 'Thailand', 'Indonesia', 'Malaysia', 'Singapore', 'Philippines']
    df = df_raw[df_raw['location'].isin(asean_countries)].copy()
 
    df['date'] = pd.to_datetime(df['date'])
    df = df[(df['date'] >= '2021-01-01') & (df['date'] <= '2022-12-31')]
 
    cols_to_keep = [
        'location', 'date', 'new_cases', 'new_deaths',
        'new_tests', 'total_vaccinations', 'people_fully_vaccinated_per_hundred'
    ]
    df = df[cols_to_keep]
 
    df[['new_cases', 'new_deaths', 'new_tests']] = df[['new_cases', 'new_deaths', 'new_tests']].fillna(0)
    df['total_vaccinations'] = df.groupby('location')['total_vaccinations'].ffill().fillna(0)
    df['people_fully_vaccinated_per_hundred'] = (
        df.groupby('location')['people_fully_vaccinated_per_hundred'].ffill().fillna(0)
    )
 
    print("Tải dữ liệu thành công!")
    print(df.head())
    return df

'''
Câu 1: Phân phối cơ bản (Histogram)
Bối cảnh: Trước khi so sánh các nước, ta cần biết quy mô lây nhiễm hàng ngày trong khu vực phân bổ như thế nào.

Yêu cầu: Vẽ Histogram cho cột new_cases.
Hint: Số ca mắc có ngày bằng 0, có ngày lên tới hàng chục ngàn. Hàm sns.histplot(bins=50) sẽ giúp bạn thấy dữ liệu bị lệch (skewed) về bên nào.
'''
def task1_histogram(df):
    """
    Vẽ Histogram cho cột new_cases để xem phân phối số ca mắc mới hàng ngày.
    Thêm đường KDE để thấy rõ dữ liệu bị lệch phải (right-skewed).
    """
    fig, ax = plt.subplots(figsize=(10, 5))
 
    sns.histplot(data=df, x='new_cases', bins=50, kde=True, color='steelblue', ax=ax)
 
    ax.set_title('Câu 1 – Phân Phối Số Ca Mắc Mới Hàng Ngày (2021–2022)', fontsize=14, fontweight='bold')
    ax.set_xlabel('Số Ca Mắc Mới (new_cases)')
    ax.set_ylabel('Số Ngày (Tần suất)')
 
    plt.tight_layout()
    plt.savefig('task1_histogram.png', dpi=150)
    plt.show()
    print(" Câu 1 hoàn thành: task1_histogram.png")

'''
Câu 2: Biến động theo thời gian (Line Chart)
Bối cảnh: Biểu đồ ở Câu 1 không cho ta thấy dịch bùng phát khi nào. Hãy thêm yếu tố thời gian.

Yêu cầu: Vẽ Line Chart thể hiện xu hướng new_cases theo date của từng quốc gia.
Hint: Sử dụng sns.lineplot(). Truyền x='date', y='new_cases' và phân loại màu sắc bằng hue='location'.
'''
def task2_linechart(df):
    """
    Vẽ Line Chart thể hiện xu hướng new_cases theo date của từng quốc gia.
    Dùng rolling average 7 ngày để giảm nhiễu cuối tuần / báo cáo trễ.
    """
    asean_countries = df['location'].unique()
 
    fig, ax = plt.subplots(figsize=(14, 6))
 
    for country in asean_countries:
        subset = df[df['location'] == country].set_index('date')
        rolling = subset['new_cases'].rolling(window=7).mean()
        ax.plot(rolling.index, rolling.values, label=country, linewidth=1.8)
 
    ax.set_title('Câu 2 – Xu Hướng Ca Mắc Mới Theo Thời Gian (Trung Bình 7 Ngày)', fontsize=14, fontweight='bold')
    ax.set_xlabel('Ngày')
    ax.set_ylabel('Số Ca Mắc Mới (7-day rolling avg)')
    ax.legend(title='Quốc Gia', loc='upper left')
    ax.xaxis.set_major_locator(plt.matplotlib.dates.MonthLocator(interval=2))
    ax.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%m/%Y'))
    plt.xticks(rotation=30)
 
    plt.tight_layout()
    plt.savefig('task2_linechart.png', dpi=150)
    plt.show()
    print("Câu 2 hoàn thành: task2_linechart.png")

'''
Câu 3: Tổng kết mất mát (Bar Chart)
Bối cảnh: Dịch bệnh bùng phát mạnh (Câu 2), vậy tổng thiệt hại về nhân mạng của mỗi quốc gia là bao nhiêu?

Yêu cầu: Dùng Bar Chart để vẽ Tổng số ca tử vong (new_deaths) của mỗi nước trong giai đoạn này.
Hint: Bạn không thể vẽ trực tiếp từ df. Hãy tạo một DataFrame mới bằng cách dùng .groupby('location')['new_deaths'].sum().reset_index(), sau đó dùng sns.barplot().
'''
def task3_barchart(df):
    """
    Vẽ Bar Chart tổng số ca tử vong (new_deaths) của mỗi quốc gia.
    Dùng groupby().sum() để tính tổng, sắp xếp giảm dần.
    """
    df_deaths = df.groupby('location')['new_deaths'].sum().reset_index()
    df_deaths = df_deaths.sort_values('new_deaths', ascending=False)
 
    fig, ax = plt.subplots(figsize=(9, 5))
 
    sns.barplot(data=df_deaths, x='location', y='new_deaths',
                palette='Reds_d', order=df_deaths['location'], ax=ax)
 
    ax.set_title('Câu 3 – Tổng Số Ca Tử Vong (2021–2022)', fontsize=14, fontweight='bold')
    ax.set_xlabel('Quốc Gia')
    ax.set_ylabel('Tổng Ca Tử Vong')
 
    for bar in ax.patches:
        ax.text(bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 500,
                f'{int(bar.get_height()):,}',
                ha='center', va='bottom', fontsize=10)
 
    plt.tight_layout()
    plt.savefig('task3_barchart.png', dpi=150)
    plt.show()
    print("Câu 3 hoàn thành → task3_barchart.png")

'''
Câu 4: Phân bổ nỗ lực phòng dịch (Pie Chart)
Bối cảnh: Để đối phó với số ca tử vong ở Câu 3, các nước bắt đầu chiến dịch tiêm chủng. Nước nào chiếm tỷ trọng số liều vaccine lớn nhất trong nhóm?

Yêu cầu: Vẽ Pie Chart thể hiện tỷ trọng tổng số liều vaccine (total_vaccinations) đã tiêm của từng nước.
Hint (Rất quan trọng): total_vaccinations là dữ liệu cộng dồn. Bạn không được dùng .sum(). Hãy dùng .groupby('location')['total_vaccinations'].max() để lấy con số cuối cùng lớn nhất của mỗi nước. Dùng plt.pie() để vẽ.
'''
def task4_piechart(df):
    """
    Vẽ Pie Chart tỷ trọng tổng liều vaccine (total_vaccinations) của mỗi nước.
    Dùng .max() thay .sum() vì total_vaccinations là dữ liệu tích lũy (cumulative).
    """
    df_vax = df.groupby('location')['total_vaccinations'].max()
 
    fig, ax = plt.subplots(figsize=(8, 8))
 
    wedges, texts, autotexts = ax.pie(
        df_vax.values,
        labels=df_vax.index,
        autopct='%1.1f%%',
        startangle=140,
        colors=sns.color_palette('pastel', len(df_vax)),
        wedgeprops=dict(edgecolor='white', linewidth=1.5)
    )
 
    for autotext in autotexts:
        autotext.set_fontsize(10)
 
    ax.set_title('Câu 4 – Tỷ Trọng Tổng Liều Vaccine Đã Tiêm\n(Tính đến cuối 2022)',
                 fontsize=14, fontweight='bold')
 
    plt.tight_layout()
    plt.savefig('task4_piechart.png', dpi=150)
    plt.show()
    print("Câu 4 hoàn thành: task4_piechart.png")

'''
Câu 5: Đo lường sự bất ổn (Box Plot)
Bối cảnh: Việc tiêm chủng (Câu 4) bắt đầu làm thay đổi cục diện. Quốc gia nào có số ca mắc mới mỗi ngày biến động khó lường nhất (nhiều outliers nhất)?

Yêu cầu: Vẽ Box Plot so sánh sự phân tán của new_cases giữa các nước.
Hint: Dùng sns.boxplot(x='location', y='new_cases'). Chú ý những điểm chấm đen ngoài râu (whiskers) biểu thị những ngày "đỉnh dịch" (outliers).
'''
def task5_boxplot(df):
    """
    Vẽ Box Plot so sánh mức độ biến động (phân tán) của new_cases giữa các quốc gia.
    Những điểm chấm ngoài whisker là các ngày đỉnh dịch (outliers).
    """
    fig, ax = plt.subplots(figsize=(11, 6))
 
    sns.boxplot(data=df, x='location', y='new_cases',
                palette='Set2',
                flierprops=dict(marker='o', markersize=3, alpha=0.4),
                ax=ax)
 
    ax.set_title('Câu 5 – Phân Tán Số Ca Mắc Mới Theo Quốc Gia (Box Plot)', fontsize=14, fontweight='bold')
    ax.set_xlabel('Quốc Gia')
    ax.set_ylabel('Số Ca Mắc Mới (new_cases)')
 
    plt.tight_layout()
    plt.savefig('task5_boxplot.png', dpi=150)
    plt.show()
    print("Câu 5 hoàn thành: task5_boxplot.png")

'''
Câu 6: Năng lực y tế và lây nhiễm (Scatter Plot)
Bối cảnh: Liệu số ca mắc nhiều (Câu 5) có phải chỉ đơn thuần là do nước đó xét nghiệm nhiều?

Yêu cầu: Vẽ Scatter Plot để xem xét mối quan hệ giữa số xét nghiệm (new_tests) và ca mắc mới (new_cases).
Hint: Dùng sns.scatterplot(). Vì có rất nhiều ngày số xét nghiệm là 0 (do không báo cáo), bạn có thể lọc các dòng df['new_tests'] > 0 trước khi vẽ để biểu đồ không bị nhiễu.
'''
def task6_scatterplot(df):
    """
    Vẽ Scatter Plot xem xét mối quan hệ giữa new_tests và new_cases.
    Lọc new_tests > 0 để loại bỏ các ngày không báo cáo xét nghiệm.
    """
    df_tests = df[df['new_tests'] > 0].copy()
 
    fig, ax = plt.subplots(figsize=(10, 6))
 
    sns.scatterplot(data=df_tests, x='new_tests', y='new_cases',
                    hue='location', alpha=0.5, s=25, palette='tab10', ax=ax)
 
    ax.set_title('Câu 6 – Mối Quan Hệ Giữa Số Xét Nghiệm và Ca Mắc Mới', fontsize=14, fontweight='bold')
    ax.set_xlabel('Số Xét Nghiệm Mới (new_tests)')
    ax.set_ylabel('Số Ca Mắc Mới (new_cases)')
    ax.legend(title='Quốc Gia', loc='upper left', markerscale=1.5)
 
    plt.tight_layout()
    plt.savefig('task6_scatterplot.png', dpi=150)
    plt.show()
    print("Câu 6 hoàn thành: task6_scatterplot.png")

'''
Câu 7: Bức tranh toàn cảnh (Heatmap)
Bối cảnh: Đến đây, ta có 4 yếu tố chính: Ca mắc, Ca tử vong, Xét nghiệm, Tỷ lệ tiêm chủng. Chúng tác động qua lại với nhau như thế nào?

Yêu cầu: Vẽ Heatmap thể hiện ma trận tương quan giữa 4 cột: new_cases, new_deaths, new_tests, và people_fully_vaccinated_per_hundred.
Hint: Lọc ra 4 cột trên, dùng .corr() để tạo ma trận toán học, sau đó đưa vào sns.heatmap(annot=True, cmap='coolwarm').
'''
def task7_heatmap(df):
    """
    Vẽ Heatmap ma trận tương quan giữa 4 chỉ số chính:
    new_cases, new_deaths, new_tests, people_fully_vaccinated_per_hundred.
    Giá trị gần +1 = tương quan thuận mạnh, gần -1 = tương quan nghịch mạnh.
    """
    corr_cols = ['new_cases', 'new_deaths', 'new_tests', 'people_fully_vaccinated_per_hundred']
    corr_matrix = df[corr_cols].corr()
 
    fig, ax = plt.subplots(figsize=(8, 6))
 
    sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm',
                square=True, linewidths=0.5,
                annot_kws={'size': 12}, ax=ax)
 
    ax.set_title('Câu 7 – Ma Trận Tương Quan Giữa Các Chỉ Số COVID-19', fontsize=14, fontweight='bold')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=20, ha='right')
    ax.set_yticklabels(ax.get_yticklabels(), rotation=0)
 
    plt.tight_layout()
    plt.savefig('task7_heatmap.png', dpi=150)
    plt.show()
    print("Câu 7 hoàn thành: task7_heatmap.png")

'''
Câu 8: Chứng minh hiệu quả Vắc-xin (Linear Regression Plot)
Bối cảnh: Từ Heatmap ở Câu 7, hãy đi sâu vào mối quan hệ quan trọng nhất: Tỷ lệ tiêm chủng cao có thực sự giúp giảm ca tử vong mới không?

Yêu cầu: Vẽ biểu đồ hồi quy Linear Regression Plot với trục X là people_fully_vaccinated_per_hundred và trục Y là new_deaths.
Hint: Dùng sns.regplot(). Đường thẳng (trendline) sẽ cho bạn biết xu hướng chung của dữ liệu thực tế.
'''
def task8_regplot(df):
    """
    Vẽ Linear Regression Plot: trục X là tỷ lệ tiêm chủng đầy đủ,
    trục Y là số ca tử vong mới. Đường hồi quy đi xuống cho thấy
    tiêm chủng cao → ca tử vong giảm.
    """
    fig, ax = plt.subplots(figsize=(10, 6))
 
    sns.regplot(data=df,
                x='people_fully_vaccinated_per_hundred',
                y='new_deaths',
                scatter_kws={'alpha': 0.2, 's': 15, 'color': 'steelblue'},
                line_kws={'color': 'crimson', 'linewidth': 2},
                ax=ax)
 
    ax.set_title('Câu 8 – Tỷ Lệ Tiêm Chủng vs. Ca Tử Vong Mới\n(Linear Regression)',
                 fontsize=14, fontweight='bold')
    ax.set_xlabel('Tỷ Lệ Tiêm Chủng Đầy Đủ (%, people_fully_vaccinated_per_hundred)')
    ax.set_ylabel('Số Ca Tử Vong Mới (new_deaths)')
 
    plt.tight_layout()
    plt.savefig('task8_regplot.png', dpi=150)
    plt.show()
    print("Câu 8 hoàn thành: task8_regplot.png")

def main():
    df = load_data()

    task1_histogram(df)
    task2_linechart(df)
    task3_barchart(df)
    task4_piechart(df)
    task5_boxplot(df)
    task6_scatterplot(df)
    task7_heatmap(df)
    task8_regplot(df)


if __name__ == "__main__":
    main()