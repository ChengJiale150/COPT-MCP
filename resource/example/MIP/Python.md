# Example 01

## 问题数学定义

这是一个经典的0-1背包问题。假设有一个背包，其最大承重为15个单位。现有5个物品，每个物品有各自的重量和价值。目标是在不超过背包承重的前提下，选择装入哪些物品，使得装入物品的总价值最大。

**决策变量：**
*   $x_i$ 为二进制变量，如果选择物品 $i$，则 $x_i=1$，否则 $x_i=0$。

**目标函数：**
最大化 $Z = 10x_1 + 15x_2 + 8x_3 + 12x_4 + 5x_5$

**约束条件：**
1.  $5x_1 + 8x_2 + 3x_3 + 6x_4 + 4x_5 \le 15$

**变量类型：**
*   $x_i \in \{0, 1\}, \quad \forall i \in \{1, 2, 3, 4, 5\}$

## 求解代码
```python
import coptpy as cp
from coptpy import COPT

try:
    # 1. 创建COPT求解环境
    # cp.Envr() 用于初始化COPT求解器环境。
    # 这是所有COPT操作的起点，负责管理许可、日志和全局配置。
    env = cp.Envr()

    # 2. 创建优化模型
    # env.createModel("模型名称") 用于创建一个新的优化模型对象。
    model = env.createModel("mip_knapsack_example")

    # 3. 定义问题数据
    # 物品价值
    values = [10, 15, 8, 12, 5]
    # 物品重量
    weights = [5, 8, 3, 6, 4]
    # 背包容量
    capacity = 15
    # 物品数量
    n_items = len(values)

    # 4. 添加决策变量
    # model.addVars() 用于向模型中批量添加一组决策变量。
    # 第一个参数是变量的数量或索引集。
    # vtype 参数指定变量类型：
    #   - COPT.CONTINUOUS: 连续变量 (默认)
    #   - COPT.BINARY: 二进制变量 (0-1)
    #   - COPT.INTEGER: 整数变量
    # nameprefix 参数为变量名自动生成前缀。
    # 返回一个 tupledict 对象，可以通过索引访问每个变量。
    x = model.addVars(n_items, vtype=COPT.BINARY, nameprefix="x")

    # 5. 添加约束条件
    # model.addConstr() 用于向模型中添加约束。
    # cp.quicksum() 是一个高效的求和函数，用于构建线性表达式，性能优于Python内置的sum()。
    # 此处定义了背包的重量容量约束。
    model.addConstr(cp.quicksum(weights[i] * x[i] for i in range(n_items)) <= capacity, name="weight_capacity")

    # 6. 设置目标函数
    # model.setObjective() 用于设置模型的优化目标。
    # 第一个参数是目标函数表达式，同样使用 cp.quicksum() 构建。
    # sense 参数指定优化方向：COPT.MAXIMIZE (最大化) 或 COPT.MINIMIZE (最小化)。
    model.setObjective(cp.quicksum(values[i] * x[i] for i in range(n_items)), sense=COPT.MAXIMIZE)

    # 7. 求解模型
    # model.solve() 启动优化求解过程。
    # 对于MIP问题，COPT将使用分支切割等算法进行求解。
    model.solve()

    # 8. 分析求解结果
    # model.status: 获取模型的求解状态。
    # COPT.OPTIMAL (1): 表示求解器找到了最优解。
    if model.status == COPT.OPTIMAL:
        print("\n--- 求解结果 ---")
        print("模型状态: 最优解 (COPT.OPTIMAL)")
        # model.objval: 获取目标函数的最优值。
        print("目标函数最优值: {:.4f}".format(model.objval))

        print("\n决策变量最优解 (选择的物品):")
        # 遍历决策变量并打印其最优值。
        # 对于二进制变量，值为1表示选择该物品，值为0表示不选择。
        total_weight = 0
        for i in range(n_items):
            # 由于数值精度问题，判断变量是否为1时最好设置一个容差
            if x[i].x > 0.5:
                print("  选择物品 {}: 价值={}, 重量={}".format(i + 1, values[i], weights[i]))
                total_weight += weights[i]
        print("装入背包总重量: {} / {}".format(total_weight, capacity))


        print("\nMIP 求解统计信息:")
        # model.getAttr() 用于获取模型的各种属性。
        # COPT.Attr.BestBnd: MIP求解过程中的最优界。对于最大化问题，这是目标值的上界。
        # COPT.Attr.BestGap: 最优解的目标值与最优界之间的相对差距 (BestObj - BestBnd) / |BestObj|。
        # COPT.Attr.NodeCnt: 分支切割算法探索的节点总数。
        print("  最优界 (Best Bound): {:.4f}".format(model.getAttr(COPT.Attr.BestBnd)))
        print("  最优间隙 (Optimality Gap): {:.4f}%".format(model.getAttr(COPT.Attr.BestGap) * 100))
        print("  搜索节点数 (Node Count): {}".format(model.getAttr(COPT.Attr.NodeCnt)))

    else:
        print("\n模型未找到最优解。状态码: {}".format(model.status))
        # 打印模型状态的文字描述，便于理解
        status_map = {
            COPT.INFEASIBLE: "模型无可行解",
            COPT.UNBOUNDED: "目标函数无界",
            COPT.TIMEOUT: "求解超时",
            COPT.INTERRUPTED: "用户中断"
        }
        print("状态描述: {}".format(status_map.get(model.status, "未知状态")))

    # 9. 将模型和结果写入文件 (可选)
    # model.write() 可以将模型定义和求解结果保存到文件中。
    # .mps 和 .lp 是标准的模型格式。
    # .sol 是解决方案文件，包含变量的最优值。
    model.write("mip_knapsack_example.mps")
    model.write("mip_knapsack_example.lp")
    model.write("mip_knapsack_example.sol")

except cp.CoptError as e:
    # 捕获COPT特有的错误，例如许可问题、建模错误等。
    print(f"COPT Error: {e.retcode} - {e.message}")
except Exception as e:
    # 捕获其他Python异常，例如导入错误、变量未定义等。
    print(f"An unexpected error occurred: {e}")
finally:
    # 确保在程序结束时关闭COPT环境，释放所有相关资源。
    if 'env' in locals() and env is not None:
        env.close()
```

# Example 02

# 问题数学定义

**背景:**
一家公司计划开设若干新仓库（设施）来服务一系列客户。每个潜在的仓库位置都有一个固定的开设成本和一定的产能上限。同时，从每个仓库向每个客户运送单位产品的成本是已知的。每个客户都有固定的产品需求量。

**目标:**
公司需要决定：
1.  开设哪些仓库。
2.  从每个开设的仓库向各个客户运送多少产品。
目标是最小化总成本，总成本包括开设仓库的固定成本和运输产品的可变成本。

**索引:**
*   $i \in I$: 潜在的仓库（设施）集合。
*   $j \in J$: 客户集合。

**参数:**
*   $f_i$: 开设仓库 $i$ 的固定成本。
*   $M_i$: 仓库 $i$ 的最大产能。
*   $d_j$: 客户 $j$ 的需求量。
*   $c_{ij}$: 从仓库 $i$ 向客户 $j$ 运输单位产品的成本。

**决策变量:**
*   $y_i$: 二进制变量。如果决定开设仓库 $i$，则 $y_i = 1$，否则 $y_i = 0$。
*   $x_{ij}$: 连续变量。从仓库 $i$ 向客户 $j$ 运输的产品数量。

**目标函数：**
最小化总成本 $Z = \sum_{i \in I} f_i y_i + \sum_{i \in I} \sum_{j \in J} c_{ij} x_{ij}$

**约束条件：**
1.  **需求满足约束:** 每个客户的需求必须被完全满足。
    $\sum_{i \in I} x_{ij} = d_j, \quad \forall j \in J$
2.  **产能与逻辑关联约束:** 从一个仓库发出的总产品量不能超过该仓库的产能，并且只有当该仓库被开设时，才能从中发货。
    $\sum_{j \in J} x_{ij} \le M_i \cdot y_i, \quad \forall i \in I$
    *(这个约束巧妙地将二进制变量 $y_i$ 和连续变量 $x_{ij}$ 关联起来。如果 $y_i=0$，则右侧为0，所有从仓库 $i$ 出发的 $x_{ij}$ 都必须为0。如果 $y_i=1$，则该约束变为标准的产能约束。)*

**变量范围（边界约束）：**
*   $x_{ij} \ge 0, \quad \forall i \in I, j \in J$
*   $y_i \in \{0, 1\}, \quad \forall i \in I$

# 求解代码
```python
import coptpy as cp
from coptpy import COPT
import pandas as pd

try:
    # 1. 使用 pandas 从文件中读取数据
    # header: | Facility_ID | Fixed_Cost | Capacity |
    facilities_df = pd.read_csv('facilities.csv')
    # header: | Customer_ID | Demand |
    customers_df = pd.read_csv('customers.csv')
    # header: | Facility_ID | Customer_ID | Cost |
    shipping_costs_df = pd.read_csv('shipping_costs.csv')

    # 2. 将数据处理成便于建模的格式
    # 将DataFrame转换为列表或字典，方便后续在模型中引用。
    facilities = facilities_df['Facility_ID'].tolist()
    customers = customers_df['Customer_ID'].tolist()

    # 使用字典推导式创建参数字典，以ID为键，方便查找。
    fixed_costs = facilities_df.set_index('Facility_ID')['Fixed_Cost'].to_dict()
    capacities = facilities_df.set_index('Facility_ID')['Capacity'].to_dict()
    demands = customers_df.set_index('Customer_ID')['Demand'].to_dict()

    # 对于运输成本，创建一个以 (facility, customer) 元组为键的字典。
    shipping_costs = shipping_costs_df.set_index(['Facility_ID', 'Customer_ID'])['Cost'].to_dict()
    
    # 创建所有可能的运输路径
    routes = list(shipping_costs.keys())

    # 3. 创建COPT求解环境和模型
    env = cp.Envr()
    model = env.createModel("facility_location_mip")

    # 4. 添加决策变量
    # y_i: 是否开设仓库 i (二进制变量)
    # 使用仓库ID列表作为索引，为每个潜在仓库创建一个二进制变量。
    y = model.addVars(facilities, vtype=COPT.BINARY, nameprefix="y")

    # x_ij: 从仓库 i 向客户 j 的发货量 (连续变量)
    # 使用运输路径元组列表作为索引，为每条路径创建一个非负连续变量。
    # lb=0.0 确保发货量非负。
    x = model.addVars(routes, lb=0.0, nameprefix="x")

    # 5. 添加约束条件
    # 约束1: 需求满足约束
    # 为每个客户 j，所有仓库到它的发货量之和必须等于其需求。
    # x.select('*', j) 是一个高效的语法，用于选择所有第一个索引为任意值、第二个索引为 j 的变量。
    for j in customers:
        model.addConstr(x.sum('*', j) == demands[j], name=f"demand_{j}")

    # 约束2: 产能与逻辑关联约束
    # 为每个仓库 i，其发货总量不能超过其产能，且只有在仓库被开设 (y[i]=1) 时才能发货。
    # x.sum(i, '*') 选择所有第一个索引为 i、第二个索引为任意值的变量。
    for i in facilities:
        model.addConstr(x.sum(i, '*') <= capacities[i] * y[i], name=f"capacity_{i}")

    # 6. 设置目标函数
    # 目标是最小化总成本，包括固定成本和运输成本。
    # 使用 cp.quicksum() 高效构建目标函数表达式。
    total_fixed_cost = cp.quicksum(fixed_costs[i] * y[i] for i in facilities)
    total_shipping_cost = cp.quicksum(shipping_costs[i, j] * x[i, j] for i, j in routes)
    
    model.setObjective(total_fixed_cost + total_shipping_cost, sense=COPT.MINIMIZE)

    # 7. 求解模型
    model.solve()

    # 8. 分析求解结果
    if model.status == COPT.OPTIMAL:
        print("\n--- 求解结果 ---")
        print(f"模型状态: 最优解 (COPT.OPTIMAL)")
        print(f"最小总成本: {model.objval:,.2f}")

        print("\n决策方案:")
        print("  开设的仓库:")
        opened_facilities = []
        for i in facilities:
            if y[i].x > 0.5: # 使用0.5作为阈值判断二进制变量是否为1
                opened_facilities.append(i)
                print(f"    - {i} (固定成本: {fixed_costs[i]:,})")
        
        if not opened_facilities:
            print("    - 无")

        print("\n  运输计划 (仅显示非零运输):")
        for i, j in routes:
            if x[i, j].x > 1e-6: # 使用一个小的容差来避免打印非常小的数值
                print(f"    - 从 {i} 到 {j}: {x[i, j].x:.2f} 单位")

        print("\n资源使用情况:")
        for i in opened_facilities:
            shipped_amount = sum(x[i, j].x for j in customers if (i, j) in x)
            print(f"  仓库 {i}: 已用产能 {shipped_amount:.2f} / {capacities[i]} (使用率: {shipped_amount/capacities[i]:.2%})")

    else:
        print(f"\n模型未找到最优解。状态码: {model.status}")

except cp.CoptError as e:
    print(f"COPT Error: {e.retcode} - {e.message}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
finally:
    if 'env' in locals() and env is not None:
        env.close()
```