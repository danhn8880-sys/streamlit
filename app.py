import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
import io
from PIL import Image

# Tiêu đề ứng dụng
st.title("Phân tích dữ liệu điểm số học sinh")

# Upload file - Sửa lỗi đóng ngoặc và chuỗi văn bản
uploaded_file = st.file_uploader("Chọn file Excel (có cột 'Điểm số')", type=["xlsx"])

# Hàm tính điểm trung bình
def calculate_average(scores):
    if not scores: return 0
    return sum(scores) / len(scores)

# Hàm phân loại điểm số
def percentage_distribution(scores):
    bins = {"90-100": 0, "80-89": 0, "70-79": 0, "60-69": 0, "<60": 0}
    for score in scores:
        if score >= 90:
            bins["90-100"] += 1
        elif score >= 80:
            bins["80-89"] += 1
        elif score >= 70:
            bins["70-79"] += 1
        elif score >= 60:
            bins["60-69"] += 1
        else:
            bins["<60"] += 1
    return bins

# Xử lý khi có file
if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)
        
        # Kiểm tra xem cột 'Điểm số' có tồn tại không
        if "Điểm số" in df.columns:
            scores = df["Điểm số"].dropna().astype(float).tolist()
            
            if scores:
                avg_score = calculate_average(scores)
                st.write(f"**Tổng số học sinh:** {len(scores)} | **Điểm trung bình:** {round(avg_score, 2)}")
                
                # Phân loại điểm
                dist = percentage_distribution(scores)
                labels = list(dist.keys())
                values = list(dist.values())
                
                # Vẽ biểu đồ với Matplotlib
                fig, ax = plt.subplots(figsize=(6, 6)) # Tăng kích thước để nhìn rõ hơn
                ax.pie(
                    values,
                    labels=labels,
                    autopct="%1.1f%%",
                    startangle=140,
                    colors=['#ff9999','#66b3ff','#99ff99','#ffcc99','#c2c2f0']
                )
                ax.axis("equal")
                
                # Lưu biểu đồ vào bộ nhớ đệm
                buf = io.BytesIO()
                fig.savefig(buf, format="png", dpi=300)
                buf.seek(0)
                
                # Hiển thị biểu đồ trung tâm
                st.markdown("### Biểu đồ phân bố điểm số")
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    st.image(buf, use_container_width=True)
            else:
                st.warning("Cột 'Điểm số' không có dữ liệu hợp lệ.")
        else:
            st.error("File Excel không có cột 'Điểm số'. Vui lòng kiểm tra lại!")
            
    except Exception as e:
        st.error(f"Đã xảy ra lỗi khi đọc file: {e}")