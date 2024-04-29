import math

# Define parameters
# item_num = 6
# buyer_num = 2


class Parent:
    def __init__(self, demand, purchasing_cost, time_multipliers, major_setup_cost, minor_setup_cost, variable_cost, buyer_num, item_num):
        self.buyer_num = buyer_num
        self.demand = demand
        self.item_num = item_num
        self.v = purchasing_cost
        self.k = time_multipliers
        self.S = major_setup_cost
        self.s = minor_setup_cost
        self.r = variable_cost
   
    # Function to compute cycle time
    def cycle_time(self, k, t):
        T = k * t
        return T
    
    # Function to compute order quantity
    def order_quantity(self, demand, T):
        Q = []
        for i in range(self.buyer_num):
            buyer_demand = []
            for j in range(self.item_num):
                buyer_demand.append(T * demand[i][j])
                Q.append(buyer_demand)
        return Q
    
    # Function to compute holding cost
    def holding_cost(self, Q, v, r):
        total_holding_cost = 0
        for i in range(self.buyer_num):
            for j in range(self.item_num):
                total_holding_cost += (Q[i][j] * v[j] * r[j]) / 2
        return total_holding_cost
    
    # Function to compute setup costs
    def set_up_costs(self, k, T):
        cons = self.S / T
        set_up_array = []
        for i in range(self.buyer_num):
            for j in range(self.item_num):
                set_up_cost = self.s[i][j] / (self.k[i][j] * T)
                set_up_array.append(set_up_cost)
        total_set_up_cost = cons + sum(set_up_array)
        return total_set_up_cost
    
    # Function to compute total annual cost
    def total_annual_cost(self, Q, T):
        total_holding_cost = self.holding_cost(Q, v, r)
        total_setup_cost = self.set_up_costs(Q, T)
        return total_holding_cost + total_setup_cost
    
    # Rand Algorithm
    def rand_algorithm(self, demand, k):
        # Step 1: Initialize parameters
        t_max = self.find_cycle_time_max()
        t_min = self.find_cycle_time_min()

        # Step 2: Initialize variables
        T_p = t_min  # Start with the minimum cycle time
        q = 0  # Initialize iteration counter
        converged = False

        # Step 3: Iterate until convergence
        while not converged:
            # Step 4: Compute k_ijq
            k_ijq = self.compute_k_ijq(T_p, q, demand)

            # Step 6: Compute new cycle time T_p
            T_p = self.compute_new_cycle_time(k_ijq)

            # Step 7: Check for convergence
            if q == 1 or self.not_condition_met(k_ijq):
                q += 1
            else:
                converged = True

        return T_p, k_ijq
    
    # Function to compute k_ijq
    def compute_k_ijq(self, T_p, q, demand):
        k_ijq = []
        for i in range(self.buyer_num):
            for j in range(self.item_num):
                k_ijq.append(2 * self.s[i][j] * T_p**2 / math.sqrt(self.r[j] * self.demand[i][j] * self.v[i]))
        return k_ijq

    # Function to compute new cycle time T_p
    def compute_new_cycle_time(self, k_ijq):
        numerator = 2 * self.S
        denominator = sum(k_ijq)
        T_p = math.sqrt(numerator / denominator)
        return T_p

# Function to check condition for Step 7
    def not_condition_met(k_ijq):
        # Check if kp_ijq - kp_ijq-1 = 1 for any i and j
        # If condition is met, return True; otherwise, return False
        # Implementation depends on specific condition in your problem
        return False

# Helper functions and functions for finding t_max and t_min (to be implemented)
    def func1(self, item_num, buyer_num, s, S):
        set_up_array = []
        for i in range(buyer_num):
            for j in range(item_num):
                set_up_array.append(s[i][j])
        return S + sum(set_up_array)
    
    def func2(self, item_num, buyer_num, d, v, r):
        demand_array = []
        for i in range(buyer_num):
            for j in range(item_num):
                demand_array.append(d[i][j] * v[j])
        return sum([r[j] * demand_array[j] for j in range(len(r))])

    # functions to find tmax
    def find_cycle_time_max(self):
        var_1 = self.func1(self.item_num, self.buyer_num, self.s, self.S)
        var_2 = self.func2(self.item_num, self.buyer_num, self.demand, self.v, self.r)
        T_max = math.sqrt((2 * var_1)/var_2)
        return round(T_max)

    #functions to find Tmin
    # helper functions for tmin
    def t1_helper_function(self, s, r, d, v):
        t1_array = []
        for i in range(self.buyer_num):
            for j in range(self.item_num):
                t_variable = math.sqrt((2 * s) / (r * d * v))
                t1_array.append(t_variable)
                return min(t1_array)

# code for finding the minimum cycle time
    def find_t1(self, s, r, demand, v):
        t1_min = float('inf')
    
        # iteration over all elements of the demand matrix
        for i in range(self.buyer_num):
            for j in range(self.item_num):
                expr = math.sqrt((2 * s[i][j]) / (r[j] * demand[i][j] * v[i]))
                t1_min = min(t1_min, expr)
    
        return t1_min
            
    def func_min1(self, s, k, buyer_num, item_num, S, t1):
        array1 = []
        for i in range(buyer_num):
            for j in range(item_num):
                set_up_cost = s[i][j]/ (k[i][j] * t1)
                array1.append(set_up_cost)
        return S + sum(array1)

    def func_min2(d, v, k, r, buyer_num, item_num, t1):
        array2 = []
        for i in range(buyer_num):
            for j in range(item_num):
                demand_cost = d[i][j] * v[i] / k[i][j] * t1
                array2.append(demand_cost)
        return sum([r[i] * array2[i] for i in range(len(r))])

    def find_cycle_time_min(self):
        t1 = self.find_t1(self.s, self.r, self.demand, self.v)
        var_1 = self.func_min1(self.s, self.k, self.buyer_num, self.item_num, self.S, t1)
        var_2 = self.func_min2(self.demand, self.v, self.k, self.r, self.buyer_num, self.item_num, t1)
        Tmin = math.sqrt((2 * var_1)/ var_2)
        return round(Tmin)


# Given parameters
# S = 1000	# Major setup cost
# s = [[350, 300, 320, 400, 400, 300], [250, 200, 300, 420, 450, 400]]  # Minor setup cost when item i is included in a group replenishment in buyer j
# v = [50, 50, 50, 50, 50, 50]  # Unit variable cost of item i
# r = [5, 5, 5, 5, 5, 5]  # Inventory carrying charge per unit time
# demand = [[10000, 5000, 3000, 1000, 600, 200], [8000, 1000, 12000, 6000, 4500, 100]]	#demand per unit time
# k_ij = [[2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2]] 


    

def calculate_cost(parameters):
    
    # Initialize variables to store extracted parameters
    # demand = None
    # purchasing_cost = None
    # time_multipliers = None
    # major_setup_cost = None
    # variable_cost = None
    
    # # Extract parameters from the dictionary
    # for param_name, param_value in parameters.items():
    #     if param_name == 'Demand':
    #         demand = param_value
    #     elif param_name == 'Price':
    #         purchasing_cost = param_value
    #     elif param_name == 'Time Multipliers':
    #         time_multipliers = param_value
    #     elif param_name == 'Major Setup Cost':
    #         major_setup_cost = param_value
    #     elif param_name == 'inventoryCarryingCharge':
    #         variable_cost = param_value
    #     # Add other parameters as needed
#     demand = parameters.get('Demand', [])
#     purchasing_cost = parameters.get('price', [])
#     time_multipliers = parameters.get('frequency', [])
#     major_setup_cost = parameters.get('Major Setup Cost', 0.0)
#     variable_cost = parameters.get('inventoryCarryingCharge', [])
#     minor_setup_cost = parameters.get('Minor Setup Cost', [])

    # Check if all required parameters are extracted and of the correct type
#     if demand is None or purchasing_cost is None or time_multipliers is None or major_setup_cost is None or variable_cost is None:
#         return {"error": "Required parameters not provided"}
# 
#     # Ensure that the parameters are of the expected type (e.g., list)
#     if not isinstance(demand, list) or not isinstance(purchasing_cost, list) \
#             or not isinstance(time_multipliers, list) or not isinstance(variable_cost, list):
#         return {"error": "Parameters must be provided as lists"}
    parent_instance = Parent(**parameters)

    T_p, k_ijq = parent_instance.rand_algorithm(parameters['demand'], parameters['time_multipliers'])
    Q = parent_instance.order_quantity(parameters['demand'], T_p)
    C = parent_instance.total_annual_cost(Q, T_p)

    return {"T_p": T_p, "Q": Q, "C": C}


# Main function
parameters = {
    'demand': [[10000, 5000, 3000, 1000, 600, 200], [8000, 1000, 12000, 6000, 4500, 100]],
    'purchasing_cost': [50, 50, 50, 50, 50, 50],
    'time_multipliers': [2,2,2,2,2,2],  # Fill in as needed
    'major_setup_cost': 1000,
    'variable_cost': [5, 5, 5, 5, 5, 5],
    'minor_setup_cost': [[350, 300, 320, 400, 400, 300], [250, 200, 300, 420, 450, 400]],
    'buyer_num': 2,
    'item_num': 6
}
calculate_cost(parameters)
