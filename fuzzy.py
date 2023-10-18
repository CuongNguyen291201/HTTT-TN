class FuzzySystem:

    def __init__(self, r, p, s):
        # Khởi tạo các thông số đầu vào
        self.r = r # Tỷ suất lợi nhuận
        self.p = p # Thời gian hoàn vốn
        self.s = s # Tỷ lệ rủi ro

        # Khởi tạo các tập mờ và các hàm thành viên cho mỗi thông số
        self.r_sets = ['RL', 'RM', 'RH'] # Các tập mờ của tỷ suất lợi nhuận
        self.r_funcs = [lambda r: max(0, min(1, (10 - r) / 10)), # Hàm thành viên của tập mờ RL
                        lambda r: max(0, min(1, (r - 5) / 10, (25 - r) / 10)), # Hàm thành viên của tập mờ RM
                        lambda r: max(0, min(1, (r - 20) / 10))] # Hàm thành viên của tập mờ RH

        self.p_sets = ['PS', 'PM', 'PL'] # Các tập mờ của thời gian hoàn vốn
        self.p_funcs = [lambda p: max(0, min(1, (2 - p) / 2)), # Hàm thành viên của tập mờ PS
                        lambda p: max(0, min(1, (p - 1) / 2, (5 - p) / 2)), # Hàm thành viên của tập mờ PM
                        lambda p: max(0, min(1, (p - 4) / 2))] # Hàm thành viên của tập mờ PL

        self.s_sets = ['SL', 'SM', 'SH'] # Các tập mờ của tỷ lệ rủi ro
        self.s_funcs = [lambda s: max(0, min(1, (5 - s) / 5)), # Hàm thành viên của tập mờ SL
                        lambda s: max(0, min(1, (s - 2.5) / 5, (12.5 - s) / 5)), # Hàm thành viên của tập mờ SM
                        lambda s: max(0, min(1, (s - 10) / 5))] # Hàm thành viên của tập mờ SH

        # Khởi tạo các luật suy diễn mờ và các toán tử logic
        self.rules = [('RL', 'PL', 'EI'), ('RL', 'SH', 'EI'), # Các luật suy diễn mờ dưới dạng bộ ba (R, P, S)
                      ('RL', 'PM', 'EL'), ('RL', 'SM', 'EL'),
                      ('RM', 'PM', 'EM'), ('RM', 'SM', 'EM'), ('RM', None, 'EM'),
                      ('RH', 'PS', 'EE'), ('RH', 'SL', 'EE'),
                      ('RH', 'PM', 'EH'), ('RH', 'SM', 'EH')]
        self.and_op = min # Toán tử logic và là hàm min
        self.or_op = max # Toán tử logic hoặc là hàm max

        # Khởi tạo các tập mờ và các hàm thành viên cho chỉ số hiệu quả đầu tư
        self.e_sets = ['EI', 'EL', 'EM', 'EH', 'EE'] # Các tập mờ của chỉ số hiệu quả đầu tư
        self.e_funcs = [lambda e: max(0, min(1, (20 - e) / 20)), # Hàm thành viên của tập mờ EI
                        lambda e: max(0, min(1, (e - 10) / 20, (50 - e) / 20)), # Hàm thành viên của tập mờ EL
                        lambda e: max(0, min(1, (e - 30) / 20, (70 - e) / 20)), # Hàm thành viên của tập mờ EM
                        lambda e: max(0, min(1, (e - 50) / 20, (90 - e) / 20)), # Hàm thành viên của tập mờ EH
                        lambda e: max(0, min(1, (e - 80) / 20))] # Hàm thành viên của tập mờ EE
        

        print('self', self, self.r)

    def fuzzify(self):
        # Hàm để tính giá trị thành viên của các thông số đầu vào cho các tập mờ tương ứng
        self.r_values = [f(self.r) for f in self.r_funcs] # Các giá trị thành viên của tỷ suất lợi nhuận
        self.p_values = [f(self.p) for f in self.p_funcs] # Các giá trị thành viên của thời gian hoàn vốn
        self.s_values = [f(self.s) for f in self.s_funcs] # Các giá trị thành viên của tỷ lệ rủi ro

    def infer(self):
        # Hàm để áp dụng các luật suy diễn mờ để tính giá trị thành viên của chỉ số hiệu quả đầu tư cho các tập mờ tương ứng
        self.e_values = [] # Các giá trị thành viên của chỉ số hiệu quả đầu tư
        for e_set in self.e_sets: # Duyệt qua các tập mờ của chỉ số hiệu quả đầu tư
            e_value = 0 # Giá trị thành viên ban đầu bằng 0
            for rule in self.rules: # Duyệt qua các luật suy diễn mờ
                if rule[2] == e_set: # Nếu luật suy diễn mờ có kết quả là tập mờ hiện tại
                    r_index = self.r_sets.index(rule[0]) # Lấy chỉ số của tập mờ của tỷ suất lợi nhuận trong luật
                    p_index = self.p_sets.index(rule[1]) # Lấy chỉ số của tập mờ của thời gian hoàn vốn trong luật
                    s_index = None # Khởi tạo chỉ số của tập mờ của tỷ lệ rủi ro trong luật là None
                    if rule[1] is not None: # Nếu luật có chứa tỷ lệ rủi ro
                        s_index = self.s_sets.index(rule[1]) # Lấy chỉ số của tập mờ của tỷ lệ rủi ro trong luật
                    if s_index is not None: # Nếu luật có chứa tỷ lệ rủi ro
                        rule_value = self.and_op(self.r_values[r_index], self.p_values[p_index], self.s_values[s_index]) # Tính giá trị thành viên của luật bằng toán tử và
                    else: # Nếu luật không chứa tỷ lệ rủi ro
                        rule_value = self.or_op(self.r_values[r_index], self.p_values[p_index]) # Tính giá trị thành viên của luật bằng toán tử hoặc
                    e_value = self.or_op(e_value, rule_value) # Cập nhật giá trị thành viên cho tập mờ hiện tại bằng toán tử hoặc
            self.e_values.append(e_value) # Thêm giá trị thành viên cho tập mờ hiện tại vào danh sách

    # def centroid(self):

    #     print('self centroid', self)

    #     # Hàm để tính trọng tâm của tập mờ kết quả để có được giá trị của chỉ số hiệu quả đầu tư bằng phương pháp centroid
    #     self.fuzzify() # Gọi hàm fuzzify để tính các giá trị thành viên cho các thông số đầu vào
    #     self.infer() # Gọi hàm infer để tính các giá trị thành viên cho chỉ số hiệu quả đầu tư

    #     numerator = 0 # Tử số ban đầu bằng 0
    #     denominator = 0 # Mẫu số ban đầu bằng 0

    #     print(self.e_sets)

    #     for i in range(len(self.e_sets)): # Duyệt qua các chỉ số của các tập mờ kết quả
    #         e_value = self.e_values[i] # Lấy giá trị thành viên của tập mờ hiện tại
    #         e_func = self.e_funcs[i] # Lấy hàm thành viên của tập mờ hiện tại
    #         e = e_value * (-80 + 20 * i + e_value * (-80 + 20 * i)) # Tính giá trị của E sao cho hàm thành viên của tập mờ bằng giá trị thành viên của luật suy diễn mờ

    #         print('e', e)

    #         numerator += e * e_func(e) # Cộng dồn tử số bằng tích của E và hàm thành viên của tập mờ cho E
    #         denominator += e_func(e) # Cộng dồn mẫu số bằng hàm thành viên của tập mờ cho E

    #     if denominator == 0: # Nếu mẫu số bằng 0
    #         return None # Trả về None
    #     else: # Nếu mẫu số khác 0
    #         return numerator / denominator # Trả về tỷ lệ của tử số và mẫu số làm giá trị của chỉ số hiệu quả đầu tư

    def centroid(self):

        print('cen self')
        # Hàm để tính trọng tâm của tập mờ kết quả để có được giá trị của chỉ số hiệu quả đầu tư bằng phương pháp centroid
        self.fuzzify()  # Gọi hàm fuzzify để tính các giá trị thành viên cho các thông số đầu vào
        self.infer()  # Gọi hàm infer để tính các giá trị thành viên cho chỉ số hiệu quả đầu tư

        # Hàm tính toán trọng tâm theo phương pháp centroid
        def calculate_centroid(values, funcs):
            weighted_sum = sum(x * f for x, f in zip(values, funcs))
            sum_of_weights = sum(funcs)

            print('weighted_sum', weighted_sum)
            print('sum_of_weights', sum_of_weights)

        #     if sum_of_weights == 0:
        #         return None
        #     return weighted_sum / sum_of_weights

        # # Tính toán trọng tâm cho chỉ số hiệu quả đầu tư
        # e = calculate_centroid(self.e_values, self.e_funcs)

        # return e
