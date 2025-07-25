# Example 01

## 问题数学定义

**目标函数：**
最大化 $Z = 1.2x + 1.8y + 2.1z$

**约束条件：**
1.  $1.5x + 1.2y + 1.8z \le 2.6$
2.  $0.8x + 0.6y + 0.9z \ge 1.2$

**变量范围（边界约束）：**
*   $0.1 \le x \le 0.6$
*   $0.2 \le y \le 1.5$
*   $0.3 \le z \le 2.8$

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
    # 所有变量、约束和目标函数都将添加到这个模型对象中。
    model = env.createModel("lp_example")

    # 3. 添加决策变量
    # model.addVar() 用于向模型中添加单个决策变量。
    # 参数说明：
    #   - lb: 变量的下界 (lower bound)。
    #   - ub: 变量的上界 (upper bound)。
    #   - name: 变量的名称，便于识别和结果输出。
    # 默认变量类型为连续型 (COPT.CONTINUOUS)。
    x = model.addVar(lb=0.1, ub=0.6, name="x")
    y = model.addVar(lb=0.2, ub=1.5, name="y")
    z = model.addVar(lb=0.3, ub=2.8, name="z")

    # 4. 添加约束条件
    # model.addConstr() 用于向模型中添加线性约束。
    # 可以直接使用Python的表达式和比较运算符 (<=, >=, ==) 来定义约束。
    # 参数 name: 约束的名称，便于识别和结果分析。
    c1 = model.addConstr(1.5*x + 1.2*y + 1.8*z <= 2.6, name="c1")
    c2 = model.addConstr(0.8*x + 0.6*y + 0.9*z >= 1.2, name="c2")

    # 5. 设置目标函数
    # model.setObjective() 用于设置模型的优化目标。
    # 第一个参数是目标函数表达式。
    # sense 参数指定优化方向：
    #   - COPT.MAXIMIZE: 最大化目标函数。
    #   - COPT.MINIMIZE: 最小化目标函数。
    model.setObjective(1.2*x + 1.8*y + 2.1*z, sense=COPT.MAXIMIZE)

    # 6. 设置求解参数 (可选)
    # model.setParam(参数常量, 值) 用于设置求解器的各种参数。
    # COPT.Param.TimeLimit: 设置求解时间限制，单位为秒。
    # 更多参数可以在COPT用户手册中查找，例如精度容差、算法选择等。
    model.setParam(COPT.Param.TimeLimit, 10.0)

    # 7. 求解模型
    # model.solve() 启动优化求解过程。
    # 求解器将根据模型定义和设置的参数寻找最优解。
    model.solve()

    # 8. 分析求解结果
    # model.status: 获取模型的求解状态。
    # COPT.OPTIMAL (1): 表示求解器找到了最优解。
    # 其他状态码如 COPT.INFEASIBLE (2) 表示模型无可行解，COPT.UNBOUNDED (3) 表示目标函数无界等。
    if model.status == COPT.OPTIMAL:
        print("\n--- 求解结果 ---")
        print("模型状态: 最优解 (COPT.OPTIMAL)")
        # model.objval: 获取目标函数的最优值。
        print("目标函数最优值: {:.4f}".format(model.objval))

        print("\n变量最优解:")
        # model.getVars() 返回模型中所有变量的列表。
        # var.name: 获取变量的名称。
        # var.x: 获取变量在最优解中的取值。
        for var in model.getVars():
            print("  {}: {:.4f}".format(var.name, var.x))

        print("\n变量基状态 (Basis Status):")
        # var.basis: 获取变量的基状态，这对于单纯形法求解结果的分析很有用。
        # COPT.BASIS_LOWER (0): 非基变量，取值下边界。
        # COPT.BASIS_BASIC (1): 基变量。
        # COPT.BASIS_UPPER (2): 非基变量，取值上边界。
        # COPT.BASIS_SUPERBASIC (3): 非基变量，但取值非上下边界 (通常用于内点法)。
        # COPT.BASIS_FIXED (4): 非基变量，固定在它唯一的边界。
        for var in model.getVars():
            basis_status_map = {
                COPT.BASIS_LOWER: "下边界非基变量",
                COPT.BASIS_BASIC: "基变量",
                COPT.BASIS_UPPER: "上边界非基变量",
                COPT.BASIS_SUPERBASIC: "超基变量",
                COPT.BASIS_FIXED: "固定非基变量"
            }
            print("  {}: {}".format(var.name, basis_status_map.get(var.basis, "未知状态")))

        print("\n约束松弛量 (Slack) 和对偶值 (Dual):")
        # model.getConstrs() 返回模型中所有约束的列表。
        # constr.name: 获取约束的名称。
        # constr.slack: 获取约束的松弛量。
        #   - 对于 <= 约束，松弛量 = RHS - LHS。
        #   - 对于 >= 约束，松弛量 = LHS - RHS。
        # constr.pi: 获取约束的对偶值 (或影子价格)。
        #   - 表示约束右侧值每单位变化对目标函数值的影响。
        for constr in model.getConstrs():
            print("  {}: 松弛量={:.4f}, 对偶值={:.4f}".format(constr.name, constr.slack, constr.pi))

    else:
        print("\n模型未找到最优解。状态码: {}".format(model.status))
        print("请检查模型定义或尝试调整求解参数。")

    # 9. 将模型和结果写入文件 (可选)
    # model.write("文件名") 可以将模型定义和求解结果保存到文件中。
    # 支持多种文件格式，通过文件扩展名自动识别：
    #   - .mps: MPS格式模型文件。
    #   - .lp: LP格式模型文件。
    #   - .sol: 解决方案文件，包含变量的最优值。
    #   - .bas: 基状态文件，保存变量和约束的基状态。
    #   - .par: 参数文件，保存当前模型中所有非默认的参数设置。
    model.write("lp_example.mps")
    model.write("lp_example.lp")
    model.write("lp_example.sol")
    model.write("lp_example.bas")
    model.write("lp_example.par")

except cp.CoptError as e:
    # 捕获COPT特有的错误，例如许可问题、建模错误等。
    print(f"COPT Error: {e.retcode} - {e.message}")
except Exception as e:
    # 捕获其他Python异常，例如导入错误、变量未定义等。
    print(f"An unexpected error occurred: {e}")
finally:
    # 确保在程序结束时关闭COPT环境，释放所有相关资源。
    # 这是一个良好的编程习惯，尤其是在处理大量模型或长时间运行时。
    if 'env' in locals() and env is not None:
        env.close()
```

# Example 02

## 问题数学定义

本问题为一个多周期生产与库存计划问题。一家公司生产多种产品以满足未来几个周期的需求，目标是在满足所有需求和生产、库存限制的前提下，最小化总生产与库存成本。

**集合与索引:**
*   $P$: 产品的集合, 索引为 $p$。
*   $T$: 时间周期的集合, 索引为 $t$。

**参数:**
*   $d_{pt}$: 在周期 $t$ 对产品 $p$ 的需求量。
*   $c_{p}^{prod}$: 生产单位产品 $p$ 的成本。
*   $c_{p}^{inv}$: 在周期结束时，持有一单位产品 $p$ 库存的成本。
*   $C_{t}$: 在周期 $t$ 的总生产能力（例如，机器小时）。
*   $r_{p}$: 生产一单位产品 $p$ 所需的资源量。
*   $I_{p}^{max}$: 产品 $p$ 的最大允许库存量。
*   $I_{p}^{0}$: 产品 $p$ 的初始库存量（周期1开始前）。

**决策变量:**
*   $x_{pt} \ge 0$: 在周期 $t$ 生产产品 $p$ 的数量。
*   $i_{pt} \ge 0$: 在周期 $t$ 结束时产品 $p$ 的库存量。

**目标函数:**
最小化总成本（生产成本 + 库存成本）：
$$ \text{Minimize} \quad \sum_{p \in P} \sum_{t \in T} (c_{p}^{prod} \cdot x_{pt} + c_{p}^{inv} \cdot i_{pt}) $$

**约束条件:**
1.  **库存平衡约束:** 每个产品在每个周期的库存必须平衡。期初库存加上本期产量等于本期需求加上期末库存。
    $$ I_{p, t-1} + x_{pt} = d_{pt} + i_{pt} \quad \forall p \in P, \forall t \in T $$
    其中 $i_{p,0}$ 定义为初始库存 $I_{p}^{0}$。

2.  **生产能力约束:** 每个周期的总资源消耗不能超过该周期的生产能力。
    $$ \sum_{p \in P} r_{p} \cdot x_{pt} \le C_{t} \quad \forall t \in T $$

3.  **库存容量约束:** 每个产品在每个周期的期末库存不能超过其最大库存容量。
    $$ i_{pt} \le I_{p}^{max} \quad \forall p \in P, \forall t \in T $$

4.  **非负约束:**
    $$ x_{pt} \ge 0, \quad i_{pt} \ge 0 \quad \forall p \in P, \forall t \in T $$

## 求解代码
```python
import coptpy as cp
from coptpy import COPT
import pandas as pd

try:
    # 1. 数据定义
    # --- 数据手动添加 ---
    # 定义生产成本、库存成本、资源消耗率、最大库存容量和初始库存
    prod_cost = {'P1': 10, 'P2': 12}
    inv_cost = {'P1': 2, 'P2': 3}
    resource_rate = {'P1': 1.0, 'P2': 1.2}
    inv_capacity = {'P1': 50, 'P2': 60}
    initial_inv = {'P1': 20, 'P2': 15}

    # --- 使用 pandas 从外界批量读入数据 ---
    # header: | Product | Period | Demand |
    df_demand = pd.read_csv('demand_data.csv')
    # header: | Period | Capacity |
    df_capacity = pd.read_csv('capacity_data.csv')

    # 将 DataFrame 转换为 COPT 建模所需的字典格式
    # 需求字典，键为 (产品, 周期) 元组
    demand = df_demand.set_index(['Product', 'Period'])['Demand'].to_dict()
    # 生产能力字典，键为周期
    prod_capacity = df_capacity.set_index('Period')['Capacity'].to_dict()

    # 从数据中动态获取产品和周期集合
    products = df_demand['Product'].unique().tolist()
    periods = df_demand['Period'].unique().tolist()

    # 2. 创建模型
    env = cp.Envr()
    model = env.createModel("production_planning_pandas")

    # 3. 添加决策变量
    # --- 批量添加变量 ---
    # 使用 model.addVars 批量添加所有产品在所有周期的生产量变量 x
    # 变量的索引是产品和周期的组合，lb=0.0 设置了非负约束
    x = model.addVars(products, periods, lb=0.0, nameprefix="produce")
    # 批量添加所有产品在所有周期的库存量变量 i
    i = model.addVars(products, periods, lb=0.0, nameprefix="inventory")

    # 4. 设置目标函数
    # 使用 quicksum 高效地构建求和表达式
    # 计算总生产成本
    total_prod_cost = cp.quicksum(prod_cost[p] * x[p, t] for p in products for t in periods)
    # 计算总库存成本
    total_inv_cost = cp.quicksum(inv_cost[p] * i[p, t] for p in products for t in periods)
    # 设置模型的目标函数为最小化总成本
    model.setObjective(total_prod_cost + total_inv_cost, sense=COPT.MINIMIZE)

    # 5. 添加约束
    # --- 逐条添加与批量添加约束的混合使用 ---
    # 约束1: 库存平衡约束
    # 这种约束逻辑依赖于时间周期(t=1时特殊处理)，使用循环逐条添加更清晰
    for p in products:
        for t in periods:
            if t == 1:
                # 周期1的期初库存是给定的初始库存
                model.addConstr(initial_inv[p] + x[p, t] == demand[p, t] + i[p, t], 
                                name=f"inv_balance_{p}_{t}")
            else:
                # 其他周期的期初库存是上一周期的期末库存
                model.addConstr(i[p, t-1] + x[p, t] == demand[p, t] + i[p, t], 
                                name=f"inv_balance_{p}_{t}")

    # 约束2: 生产能力约束
    # 使用 model.addConstrs 和生成器表达式批量添加每个周期的生产能力约束
    # 约束左侧的求和同样使用 quicksum
    model.addConstrs((cp.quicksum(resource_rate[p] * x[p, t] for p in products) <= prod_capacity[t] for t in periods), nameprefix="prod_cap")

    # 约束3: 库存容量约束
    # 批量添加每个产品在每个周期的最大库存约束
    model.addConstrs((i[p, t] <= inv_capacity[p] for p, t in i.keys()), nameprefix="inv_cap")

    # 6. 求解模型
    model.solve()

    # 7. 分析并输出结果
    # 检查求解状态，如果找到最优解，则输出结果
    if model.status == COPT.OPTIMAL:
        print(f"\n求解成功，找到最优解！")
        print(f"最小总成本为: {model.objval:.2f}")

        print("\n--- 生产计划 (x_pt) ---")
        for p in products:
            for t in periods:
                if x[p, t].x > 1e-6: # 只打印非零的生产量
                    print(f"周期 {t}, 产品 {p}: 生产 {x[p, t].x:.2f} 单位")

        print("\n--- 库存水平 (i_pt) ---")
        for p in products:
            for t in periods:
                if i[p, t].x > 1e-6: # 只打印非零的库存量
                    print(f"周期 {t} 末, 产品 {p}: 库存 {i[p, t].x:.2f} 单位")
        
        # 8. (可选) 写入模型文件
        # model.write("文件名") 可以将模型定义和求解结果保存到文件中。
        # 支持多种文件格式，通过文件扩展名自动识别：
        #   - .mps: MPS格式模型文件。
        #   - .lp: LP格式模型文件。
        #   - .sol: 解决方案文件，包含变量的最优值。
        #   - .bas: 基状态文件，保存变量和约束的基状态。
        #   - .par: 参数文件，保存当前模型中所有非默认的参数设置。
        model.write("lp_example.mps")
        model.write("lp_example.lp")
        model.write("lp_example.sol")
        model.write("lp_example.bas")
        model.write("lp_example.par")

    else:
        print(f"\n求解失败，模型状态码: {model.status}")

except cp.CoptError as e:
    # 捕获COPT特有的错误，例如许可问题、建模错误等。
    print(f"COPT Error: {e.retcode} - {e.message}")
except Exception as e:
    # 捕获其他Python异常，例如导入错误、变量未定义等。
    print(f"An unexpected error occurred: {e}")
finally:
    # 确保在程序结束时关闭COPT环境，释放所有相关资源。
    # 这是一个良好的编程习惯，尤其是在处理大量模型或长时间运行时。
    if 'env' in locals() and env is not None:
        env.close()
```