<h1 align="center">So sánh Hiệu năng: Differential Evolution (DE) vs JADE</h1>

<p align="center">
Dự án thực hiện cài đặt và so sánh hiệu năng giữa chiến lược <b>Differential Evolution (DE)</b> cổ điển và biến thể thích nghi <b>JADE (Adaptive Differential Evolution)</b>.
</p>

Bài toán được sử dụng để kiểm thử là tối ưu hóa hàm Ackley - một hàm mục tiêu phổ biến để đánh giá các thuật toán tiến hóa do có nhiều cực trị địa phương (local optima).

Tính năng

Mã nguồn bao gồm việc cài đặt các thuật toán sau:

DE/rand/1/bin: Chiến lược DE cổ điển và phổ biến nhất.

DE/best/1/bin: Lai ghép dựa trên cá thể tốt nhất toàn cục.

DE/current-to-best/1: Lai ghép hướng từ vị trí hiện tại đến vị trí tốt nhất.

JADE (Adaptive DE):

Sử dụng chiến lược lai ghép DE/current-to-pbest/1 (chọn ngẫu nhiên từ top $p\%$ tốt nhất).

Cơ chế thích nghi: Tự động điều chỉnh hệ số lai ghép ($CR$) và hệ số khuếch đại ($F$) dựa trên dữ liệu lịch sử thành công sử dụng phân phối Cauchy và Normal.

Yêu cầu cài đặt

Để chạy chương trình, bạn cần cài đặt Python 3 và các thư viện NumPy, Matplotlib. Cài đặt bằng lệnh sau:

pip install numpy matplotlib


Cách sử dụng

Đảm bảo bạn đã lưu mã nguồn vào file (ví dụ: DE_bien_the.py).

Chạy chương trình bằng lệnh:

python DE_bien_the.py


Cấu hình bài toán

Bạn có thể thay đổi các tham số trong phần đầu của file code để thử nghiệm:

D = 5             # Số chiều của không gian tìm kiếm
NP = 50           # Kích thước quần thể (Population Size)
GMAX = 500        # Số thế hệ tối đa (Generations)
BOUNDS = [-5, 5]  # Miền giá trị tìm kiếm


Kết quả mong đợi

Sau khi chạy, chương trình sẽ:

In ra tiến độ chạy của từng chiến lược (Gen/Best Fitness) trên Terminal.

Hiển thị một biểu đồ đường (Line Chart) so sánh tốc độ hội tụ của 4 chiến lược.

Hàm mục tiêu (Ackley)

Giá trị tối ưu toàn cục (Global Minimum) là $0$ tại vị trí $x = [0, ..., 0]$.

Thuật toán nào có đường biểu diễn đi xuống nhanh hơn và tiệm cận về 0 tốt hơn là thuật toán hiệu quả hơn.

Cấu trúc Code

ackley_function(x): Hàm đánh giá độ thích nghi.

lehmer_mean(values): Tính trung bình Lehmer (dùng để cập nhật tham số $F$ trong JADE).

cauchy_rand(loc, scale): Sinh số ngẫu nhiên theo phân phối Cauchy.

run_de(strategy_name): Hàm chính thực thi thuật toán DE dựa trên tên chiến lược được truyền vào.

main(): Thiết lập bài toán và vẽ biểu đồ.

