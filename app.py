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
    col1, col2 = st.columns([1, 1])

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
            height=550 # Điều chỉnh số này để khớp với chiều cao biểu đồ
        )

    with col2:
        # 1. Đảm bảo sắp xếp đồng bộ với bảng
        df_plot = df_sorted.sort_values('Tổng đã nhập', ascending=False).reset_index(drop=True)
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
    data_andieutra = {
        'Tỉnh': ['An Giang', 'Bắc Ninh', 'Cà Mau', 'Cao Bằng', 'Cần Thơ', 'Đà Nẵng', 'Đắk Lắk', 'Điện Biên', 'Đồng Nai', 'Đồng Tháp', 'Gia Lai', 'Hà Nội', 'Hà Tĩnh', 'Hải Phòng', 'Hồ Chí Minh', 'Hưng Yên', 'Khánh Hòa', 'Lai Châu', 'Lạng Sơn', 'Lào Cai', 'Lâm Đồng', 'Nghệ An', 'Ninh Bình', 'Phú Thọ', 'Quảng Ngãi', 'Quảng Ninh', 'Quảng Trị', 'Sơn La', 'Tây Ninh', 'Thái Nguyên', 'Thanh Hoá', 'Huế', 'Tuyên Quang', 'Vĩnh Long'], 
        'Số cần nhập': [426, 378, 188, 473, 80, 430, 182, 66, 457, 222, 287, 2967, 121, 504, 53, 154, 355, 47, 965, 98, 147, 291, 369, 261, 168, 1951, 125, 80, 179, 235, 121, 96, 120, 179], 
        'Số mới nhập': [12, 0, 0, 0, 12, 99, 0, 5, 39, 0, 0, 103, 1, 1, 38, 0, 0, 11, 0, 0, 0, 3, 1, 0, 4, 0, 1, 0, 22, 2, 31, 15, 1, 1], 
        'Tổng đã nhập': [201, 99, 99, 93, 227, 721, 149, 81, 457, 84, 193, 1099, 7, 170, 410, 135, 265, 381, 66, 164, 176, 104, 116, 88, 164, 1979, 141, 69, 427, 53, 697, 286, 75, 192]
        }

    data_anxetxu = {
        'Tỉnh': ['An Giang', 'Bắc Ninh', 'Cà Mau', 'Cao Bằng', 'Cần Thơ', 'Đà Nẵng', 'Đắk Lắk', 'Điện Biên', 'Đồng Nai', 'Đồng Tháp', 'Gia Lai', 'Hà Nội', 'Hà Tĩnh', 'Hải Phòng', 'Hồ Chí Minh', 'Hưng Yên', 'Khánh Hòa', 'Lai Châu', 'Lạng Sơn', 'Lào Cai', 'Lâm Đồng', 'Nghệ An', 'Ninh Bình', 'Phú Thọ', 'Quảng Ngãi', 'Quảng Ninh', 'Quảng Trị', 'Sơn La', 'Tây Ninh', 'Thái Nguyên', 'Thanh Hoá', 'Huế', 'Tuyên Quang', 'Vĩnh Long'], 
        'Số cần nhập': [426, 378, 188, 473, 80, 430, 182, 66, 457, 222, 287, 2967, 121, 504, 53, 154, 355, 47, 965, 98, 147, 291, 369, 261, 168, 1951, 125, 80, 179, 235, 121, 96, 120, 179], 
        'Số mới nhập': [12, 0, 0, 0, 12, 99, 0, 5, 39, 0, 0, 103, 1, 1, 38, 0, 0, 11, 0, 0, 0, 3, 1, 0, 4, 0, 1, 0, 22, 2, 31, 15, 1, 1], 
        'Tổng đã nhập': [201, 99, 99, 93, 227, 721, 149, 81, 457, 84, 193, 1099, 7, 170, 410, 135, 265, 381, 66, 164, 176, 104, 116, 88, 164, 1979, 141, 69, 427, 53, 697, 286, 75, 192]}
    
    
    st.title("Cập nhật tình hình nhập liệu trên nền tảng")    

    #tạo mục lớn "1. Tình hình nhập theo tỉnh"
    st.header("1. Tình hình nhập theo tỉnh")
    st.header("1.1 Nguồn tin về tội phạm")
    hienthidulieu(pd.DataFrame(data_tintoipham), "Tình hình nhập liệu nguồn tin về tội phạm")

    st.header("1.2 Án điều tra truy tố")
    hienthidulieu(pd.DataFrame(data_andieutra), "Tình hình nhập liệu án điều tra truy tố")
    
    st.header("1.2 Án điều tra truy tố")
    hienthidulieu(pd.DataFrame(data_anxetxu), "Tình hình nhập liệu án xét xử")



if __name__ == "__main__":
    main()