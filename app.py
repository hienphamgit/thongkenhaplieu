import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def plot_chart(df_plot, title):
        # 2. Tạo figure (Giảm figsize một chút để vừa vặn trong cột 2)
    fig, ax = plt.subplots(figsize=(10, 9)) 
    y_pos = np.arange(len(df_plot))

    # Vẽ biểu đồ stacked
    ax.barh(y_pos, df_plot['Đã nhập (cũ)'], 
            color='#2E86AB', label='Đã nhập (cũ)', edgecolor='white', linewidth=0.5)

    ax.barh(y_pos, df_plot['Số mới nhập'], 
            left=df_plot['Đã nhập (cũ)'],
            color='#06A77D', label='Số mới nhập', edgecolor='white', linewidth=0.5)

    ax.barh(y_pos, df_plot['Còn lại cần nhập'], 
            left=df_plot['Tổng đã nhập'],
            color='#F18F01', label='Còn lại cần nhập', edgecolor='white', linewidth=0.5)

    # 3. Tùy chỉnh trục và tiêu đề
    ax.set_yticks(y_pos)
    ax.set_yticklabels(df_plot['Tỉnh'], fontsize=9)
    ax.invert_yaxis() 
    ax.set_xlabel('Số lượng', fontsize=10, fontweight='bold')
    ax.set_title(title, fontsize=12, fontweight='bold', pad=15)

    # 4. Thêm số liệu nằm ngoài thanh bar
    max_val = max(df_plot['Số cần nhập'].max(), df_plot['Tổng đã nhập'].max())
    offset = max_val * 0.02

    for i, (idx, row) in enumerate(df_plot.iterrows()):
        total_req = row['Số cần nhập']
        total_imp = row['Tổng đã nhập']
        percentage = (total_imp / total_req * 100) if total_req > 0 else 0
        actual_end = max(total_req, total_imp)
        
        ax.text(actual_end + offset, i, 
                f"{int(total_imp)}/{int(total_req)} ({percentage:.0f}%)", 
                va='center', ha='left', fontsize=8, fontweight='bold')

    ax.set_xlim(0, max_val * 1.3) # Tạo khoảng trống cho text bên phải
    ax.grid(axis='x', alpha=0.3, linestyle='--')
    ax.legend(loc='lower right', frameon=True, fontsize=9)

    plt.tight_layout()
    st.pyplot(fig)
    return fig

def format_data(df):
    # Tính toán các thành phần
    df['Đã nhập (cũ)'] = df['Tổng đã nhập'] - df['Số mới nhập']
    df['Còn lại cần nhập'] =  df['Số cần nhập'] - df['Tổng đã nhập']
    #còn lại cần nhập 0 nếu đã nhập đủ hoặc vượt quá số cần nhập
    df['Còn lại cần nhập'] = df['Còn lại cần nhập'].apply(lambda x: 0 if x < 0 else x)
    # Tính toán tỷ lệ hoàn thành, nếu Số cần nhập = 0 thì tỷ lệ hoàn thành = 0 để tránh chia cho 0
    df['Tỷ lệ hoàn thành'] = df.apply(lambda row: row['Tổng đã nhập'] / row['Số cần nhập'] * 100 if row['Số cần nhập'] > 0 else 0, axis=1)
    return df
def hienthidulieu(df, title):
    df = format_data(df)
    # Sắp xếp theo tổng đã nhập từ cao đến thấp
    df_sorted = df.sort_values('Tổng đã nhập', ascending=False)
    
    # Chia layout 2 cột bằng nhau (1:1)
    col1, col2 = st.columns([2, 1])

    with col1:
        # Chuẩn bị dữ liệu bảng
        df_table = df_sorted.copy()
        df_table = df_table.sort_values('Tổng đã nhập', ascending=False).reset_index(drop=True)
        df_table.index = df_table.index + 1
        df_table.index.name = 'STT' # Đặt tên cho cột index là STT
        
        # Hiển thị bảng dạng dataframe để có thể tùy chỉnh chiều cao (height)
        # Giúp cột 1 cân đối hơn với biểu đồ ở cột 2
        st.dataframe(
            df_table[['Tỉnh', 'Số cần nhập', 'Số mới nhập', 'Tổng đã nhập', 'Tỷ lệ hoàn thành']].style.format({
                'Tỷ lệ hoàn thành': '{:.1f}%'
            }),
            use_container_width=True,
            height=500 # Điều chỉnh số này để khớp với chiều cao biểu đồ
        )

    with col2:
        # 1. Đảm bảo sắp xếp đồng bộ với bảng
        df_plot = df_sorted.sort_values('Tổng đã nhập', ascending=False).reset_index(drop=True)
        # Nếu df_plot lớn hơn 40 bản ghi thì chỉ vẽ 40 bản ghi đầu tiên
        if len(df_plot) > 40:
            df_plot = df_plot.head(40)
        plot_chart(df_plot, title)


def main():
    # Sửa hiển thị trang toàn khung
    st.set_page_config(layout="wide")


    #Chuẩn bị dữ liệu
    data_tintoipham = {
        'Tỉnh': ['An Giang', 'Bắc Ninh', 'Cà Mau', 'Cao Bằng', 'Cần Thơ', 'Đà Nẵng', 
                'Đắk Lắk', 'Điện Biên', 'Đồng Nai', 'Đồng Tháp', 'Gia Lai', 'Hà Nội',
                'Hà Tĩnh', 'Hải Phòng', 'Hồ Chí Minh', 'Hưng Yên', 'Khánh Hòa', 'Kiên Giang',
                'Lạng Sơn', 'Lào Cai', 'Lâm Đồng', 'Nghệ An', 'Ninh Bình', 'Phú Thọ',
                'Quảng Ngãi', 'Quảng Ninh', 'Quảng Trị', 'Sơn La', 'Tây Ninh', 'Thái Nguyên',
                'Thanh Hóa', 'Huế', 'Tuyên Quang', 'Vĩnh Long'],
        'Số cần nhập': [426, 378, 188, 473, 80, 430, 182, 66, 457, 222, 287, 2367, 121, 504,
                        53, 154, 355, 47, 365, 38, 147, 291, 363, 261, 166, 1951, 125, 80, 
                        173, 235, 120, 86, 120, 173],
        'Số mới nhập': [12, 0, 0, 0, 12, 99, 0, 3, 39, 0, 0, 103, 1, 1, 38, 0, 0, 11, 0, 0,
                        0, 3, 1, 0, 4, 0, 1, 0, 0, 2, 31, 15, 1, 0],
        'Tổng đã nhập': [201, 99, 99, 93, 227, 721, 149, 61, 457, 84, 193, 1099, 7, 170, 410,
                        135, 265, 381, 66, 164, 176, 104, 116, 88, 164, 1979, 141, 63, 427,
                        53, 637, 286, 75, 192]
    }
    data_andieutra = {'Tỉnh': ['An Giang', 'Bắc Ninh', 'Cà Mau', 'Cao Bằng', 'Cần Thơ', 'Đà Nẵng', 'Đắk Lắk', 'Điện Biên', 'Đồng Nai', 'Đồng Tháp', 'Gia Lai', 'Hà Nội', 'Hà Tĩnh', 'Hải Phòng', 'Hồ Chí Minh', 'Hưng Yên', 'Khánh Hòa', 'Lai Châu', 'Lạng Sơn', 'Lào Cai', 'Lâm Đồng', 'Nghệ An', 'Ninh Bình', 'Phú Thọ', 'Quảng Ngãi', 'Quảng Ninh', 'Quảng Trị', 'Sơn La', 'Tây Ninh', 'Thái Nguyên', 'Thanh Hoá', 'Huế', 'Tuyên Quang', 'Vĩnh Long'], 'Số cần nhập': [330, 342, 200, 307, 77, 351, 180, 90, 410, 263, 340, 1226, 123, 397, 105, 190, 176, 35, 241, 160, 73, 211, 175, 306, 172, 1908, 210, 126, 233, 173, 293, 57, 123, 179], 'Số mới nhập': [7, 0, 0, 0, 1, 111, 2, 1, 62, 0, 5, 62, 1, 0, 19, 0, 0, 15, 1, 0, 1, 0, 0, 0, 19, 0, 1, 1, 9, 9, 47, 1, 2, 2], 'Tổng đã nhập': [130, 58, 78, 99, 159, 756, 304, 243, 553, 124, 446, 1192, 106, 511, 371, 134, 144, 316, 187, 149, 134, 126, 105, 217, 245, 1914, 233, 119, 325, 140, 1000, 164, 100, 214]}

    data_anxetxu = {'Tỉnh': ['An Giang', 'Bắc Ninh', 'Cà Mau', 'Cao Bằng', 'Cần Thơ', 'Đà Nẵng', 'Đắk Lắk', 'Điện Biên', 'Đồng Nai', 'Đồng Tháp', 'Gia Lai', 'Hà Nội', 'Hà Tĩnh', 'Hải Phòng', 'Hồ Chí Minh', 'Hưng Yên', 'Khánh Hòa', 'Lai Châu', 'Lạng Sơn', 'Lào Cai', 'Lâm Đồng', 'Nghệ An', 'Ninh Bình', 'Phú Thọ', 'Quảng Ngãi', 'Quảng Ninh', 'Quảng Trị', 'Sơn La', 'Tây Ninh', 'Thái Nguyên', 'Thanh Hoá', 'Huế', 'Tuyên Quang', 'Vĩnh Long'], 'Số cần nhập': [62, 61, 17, 26, 2, 59, 40, 3, 76, 4, 41, 237, 12, 59, 22, 23, 30, 2, 32, 3, 10, 32, 22, 18, 31, 463, 17, 2, 34, 5, 27, 2, 2, 20], 'Số mới nhập': [2, 0, 0, 0, 0, 15, 0, 9, 1, 0, 1, 11, 0, 2, 0, 0, 0, 9, 1, 1, 0, 4, 0, 3, 0, 4, 1, 0, 1, 0, 17, 2, 0, 1], 'Tổng đã nhập': [6, 0, 0, 24, 0, 119, 26, 38, 24, 8, 33, 53, 11, 69, 7, 28, 13, 22, 2, 15, 28, 30, 18, 38, 16, 502, 19, 9, 11, 20, 225, 37, 33, 39]}
    
    data_tintoiphamkv = {'Tỉnh': ['Khu vực 1 - An Giang', 'Khu vực 10 - An Giang', 'Khu vực 12 - An Giang', 'Khu vực 13 - An Giang', 'Khu vực 14 - An Giang', 'Khu vực 15 - An Giang', 'Khu vực 2 - An Giang', 'Khu vực 3 - An Giang', 'Khu vực 4 - An Giang', 'Khu vực 5 - An Giang', 'Khu vực 7 - An Giang', 'Khu vực 8 - An Giang', 'Khu vực 9 - An Giang', 'Khu vực 10 - Cần Thơ', 'Khu vực 11 - Cần Thơ', 'Khu vực 2 - Cần Thơ', 'Khu vực 5 - Cần Thơ', 'Khu vực 7 - Cần Thơ', 'Khu vực 8 - Cần Thơ', 'Khu vực 9 - Cần Thơ', 'Khu vực 1 - Huế', 'Khu vực 2 - Huế', 'Khu vực 3 - Huế', 'Khu vực 4 - Huế', 'Khu vực 1 - Hà Nội', 'Khu vực 10 - Hà Nội', 'Khu vực 11 - Hà Nội', 'Khu vực 12 - Hà Nội', 'Khu vực 2 - Hà Nội', 'Khu vực 3 - Hà Nội', 'Khu vực 4 - Hà Nội', 'Khu vực 5 - Hà Nội', 'Khu vực 6 - Hà Nội', 'Khu vực 7 - Hà Nội', 'Khu vực 8 - Hà Nội', 'Khu vực 9 - Hà Nội', 'Khu vực 1 - Hồ Chí Minh', 'Khu vực 10 - Hồ Chí Minh', 'Khu vực 11 - Hồ Chí Minh', 'Khu vực 12 - Hồ Chí Minh', 'Khu vực 13 - Hồ Chí Minh', 'Khu vực 14 - Hồ Chí Minh', 'Khu vực 15 - Hồ Chí Minh', 'Khu vực 16 - Hồ Chí Minh', 'Khu vực 17 - Hồ Chí Minh', 'Khu vực 18 - Hồ Chí Minh', 'Khu vực 19 - Hồ Chí Minh', 'Khu vực 2 - Hồ Chí Minh', 'Khu vực 3 - Hồ Chí Minh', 'Khu vực 4 - Hồ Chí Minh', 'Khu vực 5 - Hồ Chí Minh', 'Khu vực 6 - Hồ Chí Minh', 'Khu vực 7 - Hồ Chí Minh', 'Khu vực 8 - Hồ Chí Minh', 'Khu vực 9 - Hồ Chí Minh', 'Khu vực 1 - Lai Châu', 'Khu vực 2 - Lai Châu', 'Khu vực 3 - Lai Châu', 'Khu vực 4 - Lai Châu', 'Khu vực 4 - Nghệ An', 'Khu vực 5 - Ninh Bình', 'Khu vực 1 - Quảng Ninh', 'Khu vực 2 - Quảng Ninh', 'Khu vực 3 - Quảng Ninh', 'Khu vực 4 - Quảng Ninh', 'Khu vực 5 - Quảng Ninh', 'Khu vực 6 - Quảng Ninh', 'Khu vực 1 - Thanh Hóa', 'Khu vực 10 - Thanh Hóa', 'Khu vực 11 - Thanh Hóa', 'Khu vực 12 - Thanh Hóa', 'Khu vực 13 - Thanh Hóa', 'Khu vực 2 - Thanh Hóa', 'Khu vực 3 - Thanh Hóa', 'Khu vực 4 - Thanh Hóa', 'Khu vực 5 - Thanh Hóa', 'Khu vực 6 - Thanh Hóa', 'Khu vực 7 - Thanh Hóa', 'Khu vực 8 - Thanh Hóa', 'Khu vực 9 - Thanh Hóa', 'Khu vực 6 - Tuyên Quang', 'Khu vực 1 - Tây Ninh', 'Khu vực 10 - Tây Ninh', 'Khu vực 11 - Tây Ninh', 'Khu vực 12 - Tây Ninh', 'Khu vực 2 - Tây Ninh', 'Khu vực 3 - Tây Ninh', 'Khu vực 4 - Tây Ninh', 'Khu vực 5 - Tây Ninh', 'Khu vực 6 - Tây Ninh', 'Khu vực 7 - Tây Ninh', 'Khu vực 8 - Tây Ninh', 'Khu vực 9 - Tây Ninh', 'Khu vực 3 - Điện Biên', 'Khu vực 5 - Điện Biên', 'Khu vực 1 - Đà Nẵng', 'Khu vực 10 - Đà Nẵng', 'Khu vực 11 - Đà Nẵng', 'Khu vực 12 - Đà Nẵng', 'Khu vực 2 - Đà Nẵng', 'Khu vực 3 - Đà Nẵng', 'Khu vực 4 - Đà Nẵng', 'Khu vực 5 - Đà Nẵng', 'Khu vực 6 - Đà Nẵng', 'Khu vực 7 - Đà Nẵng', 'Khu vực 8 - Đà Nẵng', 'Khu vực 9 - Đà Nẵng', 'Khu vực 1 - Đồng Nai', 'Khu vực 10 - Đồng Nai', 'Khu vực 11 - Đồng Nai', 'Khu vực 12 - Đồng Nai', 'Khu vực 13 - Đồng Nai', 'Khu vực 14 - Đồng Nai', 'Khu vực 2 - Đồng Nai', 'Khu vực 3 - Đồng Nai', 'Khu vực 4 - Đồng Nai', 'Khu vực 5 - Đồng Nai', 'Khu vực 6 - Đồng Nai', 'Khu vực 7 - Đồng Nai', 'Khu vực 8 - Đồng Nai', 'Khu vực 9 - Đồng Nai'], 'Số cần nhập': [221, 116, 47, 232, 158, 164, 281, 111, 80, 89, 104, 94, 329, 113, 112, 236, 290, 155, 207, 182, 199, 117, 91, 97, 4293, 691, 1596, 381, 4391, 2511, 11062, 2456, 1536, 1415, 903, 504, 9, 6, 3, 8, 2, 7, 10, 4, 0, 5, 1, 11, 7, 4, 1, 3, 15, 29, 18, 40, 110, 112, 78, 81, 284, 570, 274, 309, 124, 159, 160, 151, 65, 11, 37, 16, 82, 66, 50, 60, 44, 46, 70, 70, 21, 133, 195, 228, 235, 111, 286, 131, 76, 48, 75, 51, 45, 67, 36, 209, 232, 63, 11, 251, 244, 223, 198, 133, 118, 25, 24, 855, 257, 113, 90, 82, 56, 332, 313, 112, 67, 122, 69, 63, 318], 'Số mới nhập': [3, 0, 0, 1, 0, 2, 1, 2, 0, 0, 0, 0, 2, 9, 0, 0, 0, 0, 0, 0, 0, 6, 9, 0, 0, 7, 0, 9, 0, 24, 5, 13, 13, 3, 5, 24, 1, 1, 0, 0, 3, 1, 0, 1, 2, 2, 2, 2, 0, 1, 0, 5, 3, 2, 6, 0, 6, 3, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 1, 5, 8, 4, 0, 10, 0, 1, 2, 9, 1, 1, 2, 1, 5, 0, 0, 1, 0, 0, 4, 0, 14, 12, 2, 0, 1, 20, 30, 16, 2, 0, 1, 1, 6, 0, 0, 0, 0, 4, 4, 1, 0, 3, 15, 6, 0, 0], 'Tổng đã nhập': [33, 1, 1, 35, 0, 26, 4, 12, 0, 0, 8, 13, 14, 26, 1, 5, 0, 10, 1, 0, 70, 47, 82, 35, 0, 121, 1, 89, 0, 47, 35, 142, 27, 7, 10, 138, 16, 16, 4, 20, 6, 11, 14, 15, 9, 10, 5, 20, 8, 5, 1, 8, 23, 34, 35, 21, 141, 125, 45, 1, 0, 574, 277, 311, 125, 159, 161, 73, 45, 25, 28, 9, 68, 29, 62, 60, 27, 15, 135, 11, 1, 17, 174, 20, 32, 37, 30, 13, 4, 7, 8, 1, 5, 5, 0, 173, 88, 7, 15, 48, 71, 80, 86, 35, 25, 5, 3, 63, 13, 1, 0, 0, 4, 10, 118, 0, 41, 43, 10, 4, 15]}
    data_andieutrakv = {'Tỉnh': ['Khu vực 1 - An Giang', 'Khu vực 10 - An Giang', 'Khu vực 12 - An Giang', 'Khu vực 13 - An Giang', 'Khu vực 14 - An Giang', 'Khu vực 15 - An Giang', 'Khu vực 2 - An Giang', 'Khu vực 3 - An Giang', 'Khu vực 4 - An Giang', 'Khu vực 5 - An Giang', 'Khu vực 7 - An Giang', 'Khu vực 8 - An Giang', 'Khu vực 9 - An Giang', 'Khu vực 10 - Cần Thơ', 'Khu vực 11 - Cần Thơ', 'Khu vực 2 - Cần Thơ', 'Khu vực 5 - Cần Thơ', 'Khu vực 7 - Cần Thơ', 'Khu vực 8 - Cần Thơ', 'Khu vực 9 - Cần Thơ', 'Khu vực 1 - Huế', 'Khu vực 2 - Huế', 'Khu vực 3 - Huế', 'Khu vực 4 - Huế', 'Khu vực 1 - Hà Nội', 'Khu vực 10 - Hà Nội', 'Khu vực 11 - Hà Nội', 'Khu vực 12 - Hà Nội', 'Khu vực 2 - Hà Nội', 'Khu vực 3 - Hà Nội', 'Khu vực 4 - Hà Nội', 'Khu vực 5 - Hà Nội', 'Khu vực 6 - Hà Nội', 'Khu vực 7 - Hà Nội', 'Khu vực 8 - Hà Nội', 'Khu vực 9 - Hà Nội', 'Khu vực 1 - Hồ Chí Minh', 'Khu vực 10 - Hồ Chí Minh', 'Khu vực 11 - Hồ Chí Minh', 'Khu vực 12 - Hồ Chí Minh', 'Khu vực 13 - Hồ Chí Minh', 'Khu vực 14 - Hồ Chí Minh', 'Khu vực 15 - Hồ Chí Minh', 'Khu vực 16 - Hồ Chí Minh', 'Khu vực 17 - Hồ Chí Minh', 'Khu vực 18 - Hồ Chí Minh', 'Khu vực 19 - Hồ Chí Minh', 'Khu vực 2 - Hồ Chí Minh', 'Khu vực 3 - Hồ Chí Minh', 'Khu vực 4 - Hồ Chí Minh', 'Khu vực 5 - Hồ Chí Minh', 'Khu vực 6 - Hồ Chí Minh', 'Khu vực 7 - Hồ Chí Minh', 'Khu vực 8 - Hồ Chí Minh', 'Khu vực 9 - Hồ Chí Minh', 'Khu vực 1 - Lai Châu', 'Khu vực 2 - Lai Châu', 'Khu vực 3 - Lai Châu', 'Khu vực 4 - Lai Châu', 'Khu vực 4 - Nghệ An', 'Khu vực 5 - Ninh Bình', 'Khu vực 1 - Quảng Ninh', 'Khu vực 2 - Quảng Ninh', 'Khu vực 3 - Quảng Ninh', 'Khu vực 4 - Quảng Ninh', 'Khu vực 5 - Quảng Ninh', 'Khu vực 6 - Quảng Ninh', 'Khu vực 1 - Thanh Hóa', 'Khu vực 10 - Thanh Hóa', 'Khu vực 11 - Thanh Hóa', 'Khu vực 12 - Thanh Hóa', 'Khu vực 13 - Thanh Hóa', 'Khu vực 2 - Thanh Hóa', 'Khu vực 3 - Thanh Hóa', 'Khu vực 4 - Thanh Hóa', 'Khu vực 5 - Thanh Hóa', 'Khu vực 6 - Thanh Hóa', 'Khu vực 7 - Thanh Hóa', 'Khu vực 8 - Thanh Hóa', 'Khu vực 9 - Thanh Hóa', 'Khu vực 6 - Tuyên Quang', 'Khu vực 1 - Tây Ninh', 'Khu vực 10 - Tây Ninh', 'Khu vực 11 - Tây Ninh', 'Khu vực 12 - Tây Ninh', 'Khu vực 2 - Tây Ninh', 'Khu vực 3 - Tây Ninh', 'Khu vực 4 - Tây Ninh', 'Khu vực 5 - Tây Ninh', 'Khu vực 6 - Tây Ninh', 'Khu vực 7 - Tây Ninh', 'Khu vực 8 - Tây Ninh', 'Khu vực 9 - Tây Ninh', 'Khu vực 3 - Điện Biên', 'Khu vực 5 - Điện Biên', 'Khu vực 1 - Đà Nẵng', 'Khu vực 10 - Đà Nẵng', 'Khu vực 11 - Đà Nẵng', 'Khu vực 12 - Đà Nẵng', 'Khu vực 2 - Đà Nẵng', 'Khu vực 3 - Đà Nẵng', 'Khu vực 4 - Đà Nẵng', 'Khu vực 5 - Đà Nẵng', 'Khu vực 6 - Đà Nẵng', 'Khu vực 7 - Đà Nẵng', 'Khu vực 8 - Đà Nẵng', 'Khu vực 9 - Đà Nẵng', 'Khu vực 1 - Đồng Nai', 'Khu vực 10 - Đồng Nai', 'Khu vực 11 - Đồng Nai', 'Khu vực 12 - Đồng Nai', 'Khu vực 13 - Đồng Nai', 'Khu vực 14 - Đồng Nai', 'Khu vực 2 - Đồng Nai', 'Khu vực 3 - Đồng Nai', 'Khu vực 4 - Đồng Nai', 'Khu vực 5 - Đồng Nai', 'Khu vực 6 - Đồng Nai', 'Khu vực 7 - Đồng Nai', 'Khu vực 8 - Đồng Nai', 'Khu vực 9 - Đồng Nai'], 'Số cần nhập': [558, 542, 229, 620, 495, 195, 498, 174, 111, 134, 127, 136, 1493, 147, 113, 270, 518, 210, 284, 209, 258, 132, 76, 106, 2433, 387, 1088, 433, 1942, 1527, 2161, 1422, 1564, 1469, 636, 728, 6, 3, 7, 8, 1, 0, 6, 5, 2, 4, 0, 14, 13, 2, 10, 1, 6, 15, 14, 118, 161, 194, 135, 123, 380, 417, 282, 217, 81, 150, 165, 705, 154, 33, 93, 70, 216, 154, 234, 88, 129, 89, 191, 191, 21, 276, 400, 422, 455, 192, 450, 190, 105, 97, 151, 74, 69, 63, 118, 207, 514, 120, 9, 243, 202, 320, 427, 259, 241, 103, 80, 3737, 251, 177, 59, 140, 60, 1107, 708, 285, 75, 225, 98, 127, 296], 'Số mới nhập': [3, 0, 0, 3, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 4, 0, 8, 0, 6, 7, 12, 4, 0, 0, 21, 0, 0, 2, 0, 0, 0, 0, 1, 1, 5, 0, 1, 0, 0, 0, 2, 2, 0, 3, 0, 3, 10, 2, 0, 0, 0, 0, 0, 0, 1, 1, 6, 0, 3, 0, 0, 6, 6, 5, 1, 3, 1, 17, 0, 1, 0, 1, 0, 4, 2, 0, 2, 0, 0, 1, 0, 0, 3, 0, 2, 25, 1, 0, 4, 9, 31, 20, 11, 1, 1, 0, 50, 0, 0, 0, 7, 0, 6, 0, 0, 0, 0, 3, 0, 1], 'Tổng đã nhập': [27, 0, 0, 14, 0, 13, 7, 3, 0, 0, 1, 11, 2, 1, 0, 1, 0, 3, 0, 0, 38, 6, 16, 3, 0, 35, 0, 79, 0, 12, 30, 69, 53, 0, 5, 104, 14, 14, 15, 15, 2, 4, 12, 15, 7, 22, 2, 31, 22, 4, 14, 10, 22, 27, 24, 4, 168, 56, 36, 0, 0, 416, 281, 219, 81, 152, 167, 111, 12, 25, 16, 12, 54, 113, 40, 41, 62, 22, 100, 9, 1, 7, 34, 5, 16, 17, 3, 4, 2, 0, 9, 0, 0, 4, 0, 131, 90, 2, 4, 46, 43, 63, 62, 45, 28, 3, 0, 207, 4, 7, 0, 7, 0, 10, 43, 1, 23, 10, 5, 2, 5]}
    data_anxetxukv = {'Tỉnh': ['Khu vực 1 - An Giang', 'Khu vực 10 - An Giang', 'Khu vực 12 - An Giang', 'Khu vực 13 - An Giang', 'Khu vực 14 - An Giang', 'Khu vực 15 - An Giang', 'Khu vực 2 - An Giang', 'Khu vực 3 - An Giang', 'Khu vực 4 - An Giang', 'Khu vực 5 - An Giang', 'Khu vực 7 - An Giang', 'Khu vực 8 - An Giang', 'Khu vực 9 - An Giang', 'Khu vực 10 - Cần Thơ', 'Khu vực 11 - Cần Thơ', 'Khu vực 2 - Cần Thơ', 'Khu vực 5 - Cần Thơ', 'Khu vực 7 - Cần Thơ', 'Khu vực 8 - Cần Thơ', 'Khu vực 9 - Cần Thơ', 'Khu vực 1 - Huế', 'Khu vực 2 - Huế', 'Khu vực 3 - Huế', 'Khu vực 4 - Huế', 'Khu vực 1 - Hà Nội', 'Khu vực 10 - Hà Nội', 'Khu vực 11 - Hà Nội', 'Khu vực 12 - Hà Nội', 'Khu vực 2 - Hà Nội', 'Khu vực 3 - Hà Nội', 'Khu vực 4 - Hà Nội', 'Khu vực 5 - Hà Nội', 'Khu vực 6 - Hà Nội', 'Khu vực 7 - Hà Nội', 'Khu vực 8 - Hà Nội', 'Khu vực 9 - Hà Nội', 'Khu vực 1 - Hồ Chí Minh', 'Khu vực 10 - Hồ Chí Minh', 'Khu vực 11 - Hồ Chí Minh', 'Khu vực 12 - Hồ Chí Minh', 'Khu vực 13 - Hồ Chí Minh', 'Khu vực 14 - Hồ Chí Minh', 'Khu vực 15 - Hồ Chí Minh', 'Khu vực 16 - Hồ Chí Minh', 'Khu vực 17 - Hồ Chí Minh', 'Khu vực 18 - Hồ Chí Minh', 'Khu vực 19 - Hồ Chí Minh', 'Khu vực 2 - Hồ Chí Minh', 'Khu vực 3 - Hồ Chí Minh', 'Khu vực 4 - Hồ Chí Minh', 'Khu vực 5 - Hồ Chí Minh', 'Khu vực 6 - Hồ Chí Minh', 'Khu vực 7 - Hồ Chí Minh', 'Khu vực 8 - Hồ Chí Minh', 'Khu vực 9 - Hồ Chí Minh', 'Khu vực 1 - Lai Châu', 'Khu vực 2 - Lai Châu', 'Khu vực 3 - Lai Châu', 'Khu vực 4 - Lai Châu', 'Khu vực 4 - Nghệ An', 'Khu vực 5 - Ninh Bình', 'Khu vực 1 - Quảng Ninh', 'Khu vực 2 - Quảng Ninh', 'Khu vực 3 - Quảng Ninh', 'Khu vực 4 - Quảng Ninh', 'Khu vực 5 - Quảng Ninh', 'Khu vực 6 - Quảng Ninh', 'Khu vực 1 - Thanh Hóa', 'Khu vực 10 - Thanh Hóa', 'Khu vực 11 - Thanh Hóa', 'Khu vực 12 - Thanh Hóa', 'Khu vực 13 - Thanh Hóa', 'Khu vực 2 - Thanh Hóa', 'Khu vực 3 - Thanh Hóa', 'Khu vực 4 - Thanh Hóa', 'Khu vực 5 - Thanh Hóa', 'Khu vực 6 - Thanh Hóa', 'Khu vực 7 - Thanh Hóa', 'Khu vực 8 - Thanh Hóa', 'Khu vực 9 - Thanh Hóa', 'Khu vực 6 - Tuyên Quang', 'Khu vực 1 - Tây Ninh', 'Khu vực 10 - Tây Ninh', 'Khu vực 11 - Tây Ninh', 'Khu vực 12 - Tây Ninh', 'Khu vực 2 - Tây Ninh', 'Khu vực 3 - Tây Ninh', 'Khu vực 4 - Tây Ninh', 'Khu vực 5 - Tây Ninh', 'Khu vực 6 - Tây Ninh', 'Khu vực 7 - Tây Ninh', 'Khu vực 8 - Tây Ninh', 'Khu vực 9 - Tây Ninh', 'Khu vực 3 - Điện Biên', 'Khu vực 5 - Điện Biên', 'Khu vực 1 - Đà Nẵng', 'Khu vực 10 - Đà Nẵng', 'Khu vực 11 - Đà Nẵng', 'Khu vực 12 - Đà Nẵng', 'Khu vực 2 - Đà Nẵng', 'Khu vực 3 - Đà Nẵng', 'Khu vực 4 - Đà Nẵng', 'Khu vực 5 - Đà Nẵng', 'Khu vực 6 - Đà Nẵng', 'Khu vực 7 - Đà Nẵng', 'Khu vực 8 - Đà Nẵng', 'Khu vực 9 - Đà Nẵng', 'Khu vực 1 - Đồng Nai', 'Khu vực 10 - Đồng Nai', 'Khu vực 11 - Đồng Nai', 'Khu vực 12 - Đồng Nai', 'Khu vực 13 - Đồng Nai', 'Khu vực 14 - Đồng Nai', 'Khu vực 2 - Đồng Nai', 'Khu vực 3 - Đồng Nai', 'Khu vực 4 - Đồng Nai', 'Khu vực 5 - Đồng Nai', 'Khu vực 6 - Đồng Nai', 'Khu vực 7 - Đồng Nai', 'Khu vực 8 - Đồng Nai', 'Khu vực 9 - Đồng Nai'], 'Số cần nhập': [41, 9, 0, 24, 9, 0, 30, 2, 3, 11, 2, 11, 10, 3, 27, 15, 16, 15, 10, 13, 36, 4, 6, 2, 97, 20, 22, 3, 95, 132, 139, 127, 44, 116, 32, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 2, 31, 114, 71, 83, 24, 51, 67, 4, 5, 4, 9, 8, 17, 5, 5, 1, 14, 1, 1, 1, 0, 6, 11, 32, 31, 9, 17, 4, 0, 2, 6, 1, 9, 0, 1, 6, 91, 7, 0, 24, 25, 0, 27, 13, 9, 7, 0, 133, 28, 8, 1, 1, 8, 11, 16, 11, 18, 11, 12, 28, 0], 'Số mới nhập': [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, -1, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 4, 0, 1, 3, 5, 0, 5, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 7, 0, 0, 0, 0, 2, 0, 1, 3, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'Tổng đã nhập': [1, 0, 0, 2, 0, 0, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 2, 6, 6, 0, 0, 0, 10, 1, 0, 0, 3, 2, 0, 0, 31, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 8, 2, 0, 0, 0, 117, 80, 83, 25, 54, 69, 29, 3, 9, 3, 8, 38, 20, 4, 29, 6, 18, 2, 2, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 58, 5, 0, 1, 7, 6, 1, 10, 4, 10, 0, 0, 2, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1]}
    st.title("Cập nhật tình hình nhập liệu trên nền tảng")    

    #tạo mục lớn "1. Tình hình nhập theo tỉnh"
    st.header("1. Tình hình nhập theo tỉnh")
    st.header("1.1 Nguồn tin về tội phạm")
    hienthidulieu(pd.DataFrame(data_tintoipham), "Tình hình nhập liệu nguồn tin về tội phạm theo tỉnh")

    st.header("1.2 Án điều tra truy tố")
    hienthidulieu(pd.DataFrame(data_andieutra), "Tình hình nhập liệu án điều tra truy tố theo tỉnh")
    
    st.header("1.2 Án điều tra truy tố")
    hienthidulieu(pd.DataFrame(data_anxetxu), "Tình hình nhập liệu án xét xử theo tỉnh")
    
    st.header("2. Tình hình nhập theo khu vực")
    st.header("2.1 Nguồn tin về tội phạm theo khu vực")
    hienthidulieu(pd.DataFrame(data_tintoiphamkv), "Tình hình nhập liệu nguồn tin về tội phạm theo khu vực")

    st.header("2.2 Án điều tra truy tố theo khu vực")
    hienthidulieu(pd.DataFrame(data_andieutrakv), "Tình hình nhập liệu án điều tra truy tố theo khu vực")
    
    st.header("2.3 Án điều tra xét xử theo khu vực")
    hienthidulieu(pd.DataFrame(data_anxetxukv), "Tình hình nhập liệu án xét xử theo khu vực")

if __name__ == "__main__":
    main()