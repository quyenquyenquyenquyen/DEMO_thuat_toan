import numpy as np
import matplotlib.pyplot as plt

# --- Cấu hình bài toán ---
D = 5               # Số chiều
NP = 50             # Kích thước quần thể
F_DEFAULT = 0.8     # Hệ số khuếch đại mặc định (cho các biến thể cổ điển)
CR_DEFAULT = 0.9    # Xác suất lai ghép mặc định (cho các biến thể cổ điển)
GMAX = 500          # Số thế hệ tối đa
BOUNDS = [-5, 5]    # Miền tìm kiếm

# --- Hàm mục tiêu: Ackley Function ---
def ackley_function(x):
    """
    Tính giá trị hàm Ackley.
    Global Minimum: f(x) = 0 tại x = [0, ..., 0]
    """
    first_sum = np.sum(x**2)
    second_sum = np.sum(np.cos(2 * np.pi * x))
    n = float(len(x))
    return -20.0 * np.exp(-0.2 * np.sqrt(first_sum / n)) - np.exp(second_sum / n) + 20 + np.e

# --- Các hàm hỗ trợ cho JADE ---
def lehmer_mean(values):
    """Tính trung bình Lehmer"""
    return np.sum(values ** 2) / np.sum(values) if len(values) > 0 else 0

def cauchy_rand(loc, scale):
    """Sinh số ngẫu nhiên theo phân phối Cauchy"""
    return loc + scale * np.random.standard_cauchy()

def run_de(strategy_name):
    population = np.random.uniform(BOUNDS[0], BOUNDS[1], (NP, D))
    fitness = np.array([ackley_function(ind) for ind in population])
    best_idx = np.argmin(fitness)
    global_best_fitness = fitness[best_idx]
    global_best_position = population[best_idx].copy()
    history = [global_best_fitness]

    # --- Tham số riêng cho JADE ---
    mu_cr = 0.5     # Trung bình khởi tạo cho CR
    mu_f = 0.5      # Trung bình khởi tạo cho F
    c = 0.1         # Learning rate (hệ số học)
    p_jade = 0.05   # Top p% tốt nhất (cho current-to-pbest)

    for g in range(GMAX):
        new_population = np.copy(population)
        successful_cr = []
        successful_f = []
        sorted_indices = np.argsort(fitness)
        
        for i in range(NP):
            x_i = population[i]
            
            if strategy_name == 'JADE':
                cr_i = np.random.normal(mu_cr, 0.1)
                cr_i = np.clip(cr_i, 0, 1)
                
                while True:
                    f_i = cauchy_rand(mu_f, 0.1)
                    if f_i > 0:
                        break
                f_i = min(f_i, 1.0)
            else:
                cr_i = CR_DEFAULT
                f_i = F_DEFAULT

            idxs = [idx for idx in range(NP) if idx != i]
            
            if strategy_name == 'DE/rand/1/bin':
                choices = np.random.choice(idxs, 3, replace=False)
                r1_vec, r2_vec, r3_vec = population[choices]
                v = r1_vec + f_i * (r2_vec - r3_vec)

            elif strategy_name == 'DE/best/1/bin':
                choices = np.random.choice(idxs, 2, replace=False)
                r1_vec, r2_vec = population[choices]
                v = global_best_position + f_i * (r1_vec - r2_vec)

            elif strategy_name == 'DE/current-to-best/1':
                choices = np.random.choice(idxs, 2, replace=False)
                r1_vec, r2_vec = population[choices]
                v = x_i + f_i * (global_best_position - x_i) + f_i * (r1_vec - r2_vec)
            
            elif strategy_name == 'JADE':
                top_best_count = max(1, int(NP * p_jade))
                pbest_idx = np.random.choice(sorted_indices[:top_best_count])
                x_pbest = population[pbest_idx]
                
                choices = np.random.choice(idxs, 2, replace=False)
                r1_vec, r2_vec = population[choices]
                
                v = x_i + f_i * (x_pbest - x_i) + f_i * (r1_vec - r2_vec)
            
            else:
                choices = np.random.choice(idxs, 3, replace=False)
                r1_vec, r2_vec, r3_vec = population[choices]
                v = r1_vec + f_i * (r2_vec - r3_vec)

            v = np.clip(v, BOUNDS[0], BOUNDS[1])

            # Lai ghép (Crossover) 
            u = np.copy(x_i)
            j_rand = np.random.randint(D)
            for j in range(D):
                if np.random.rand() < cr_i or j == j_rand:
                    u[j] = v[j]

            # Chọn lọc (Selection) 
            f_u = ackley_function(u)
            if f_u < fitness[i]:
                new_population[i] = u
                fitness[i] = f_u
                
                # Lưu tham số thành công cho JADE
                if strategy_name == 'JADE':
                    successful_cr.append(cr_i)
                    successful_f.append(f_i)

                if f_u < global_best_fitness:
                    global_best_fitness = f_u
                    global_best_position = u

        # Cập nhật quần thể
        population = new_population
        history.append(global_best_fitness)

        # Cập nhật tham số thích nghi (Adaptive Update) cho JADE 
        if strategy_name == 'JADE' and len(successful_cr) > 0:
            # Cập nhật mu_cr (Arithmetic Mean)
            mean_a_cr = np.mean(successful_cr)
            mu_cr = (1 - c) * mu_cr + c * mean_a_cr
            
            # Cập nhật mu_f (Lehmer Mean)
            mean_l_f = lehmer_mean(np.array(successful_f))
            mu_f = (1 - c) * mu_f + c * mean_l_f

        # In tiến độ
        if (g + 1) % 100 == 0:
            print(f"Strategy: {strategy_name:<20} | Gen: {g+1}/{GMAX} | Best Fit: {global_best_fitness:.10f}")

    return history, global_best_position, global_best_fitness

def main():
    strategies = ['DE/rand/1/bin', 'DE/best/1/bin', 'DE/current-to-best/1', 'JADE']
    results = {}

    print(f"Chạy tối ưu hóa Ackley (D={D}, NP={NP}, MaxGen={GMAX})\n")

    plt.figure(figsize=(12, 7))

    for strat in strategies:
        hist, best_pos, best_fit = run_de(strat)
        results[strat] = hist
        print(f"--> Kết quả {strat}: Fitness = {best_fit:.2e}")
        
    for strat, hist in results.items():
        plt.plot(hist, label=strat, linewidth=2 if strat == 'JADE' else 1)

    plt.title('So sánh hội tụ: JADE vs Các biến thể DE cổ điển')
    plt.xlabel('Thế hệ')
    plt.grid(True, which="both", ls="-", alpha=0.5)
    plt.legend()
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()