# Example 01

## 问题数学定义

**目标函数：**
最小化 $Z = x + y + z$

**约束条件：**
1.  $x + y + z = 1$
2.  $\sqrt{x^2 + y^2} \le z$

**变量范围（边界约束）：**
*   $x \ge 0$
*   $y \ge 0$
*   $z \ge 0$

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
    model = env.createModel("socp_example")

    # 3. 添加决策变量
    # model.addVar() 用于向模型中添加单个决策变量。
    # 参数说明：
    #   - lb: 变量的下界 (lower bound)。本例中为0，表示非负。
    #   - name: 变量的名称，便于识别和结果输出。
    # 默认变量类型为连续型 (COPT.CONTINUOUS)。
    x = model.addVar(lb=0.0, name="x")
    y = model.addVar(lb=0.0, name="y")
    z = model.addVar(lb=0.0, name="z")

    # 4. 设置目标函数
    # model.setObjective() 用于设置模型的优化目标。
    # 第一个参数是目标函数表达式。
    # sense 参数指定优化方向：
    #   - COPT.MINIMIZE: 最小化目标函数。
    #   - COPT.MAXIMIZE: 最大化目标函数。
    model.setObjective(x + y + z, sense=COPT.MINIMIZE)

    # 5. 添加约束条件
    # model.addConstr() 用于添加线性约束。
    c1 = model.addConstr(x + y + z == 1, name="c1")

    # model.addCone() 用于添加二阶锥约束。
    # 对于标准二阶锥约束 t >= sqrt(x1^2 + x2^2 + ...)，变量列表应为 [t, x1, x2, ...]。
    # 本例中的约束为 z >= sqrt(x^2 + y^2)，因此变量列表为 [z, x, y]。
    # ctype表示二阶锥约束类型，目前支持如下两种:
    #     - COPT.CONE_QUAD 指定了约束类型为标准二阶锥 (Standard Second-Order Cone)
    #     - CONE_RQUAD 指定了约束类型为旋转二阶锥
    soc1 = model.addCone([z, x, y], ctype=COPT.CONE_QUAD)

    # 6. 求解模型
    # model.solve() 启动优化求解过程。
    # COPT将自动识别模型类型为SOCP，并调用内点法进行求解。
    model.solve()

    # 7. 分析求解结果
    # model.status 获取模型的求解状态。
    # COPT.OPTIMAL (1): 表示求解器找到了最优解。
    if model.status == COPT.OPTIMAL:
        print("\n--- 求解结果 ---")
        print("模型状态: 最优解 (COPT.OPTIMAL)")
        # model.objval 获取目标函数的最优值。
        print("目标函数最优值: {:.4f}".format(model.objval))

        print("\n变量最优解:")
        # model.getVars() 返回模型中所有变量的列表。
        # var.x 获取变量在最优解中的取值。
        for var in model.getVars():
            print("  {}: {:.4f}".format(var.name, var.x))

        print("\n线性约束信息:")
        # model.getConstrs() 返回模型中所有线性约束的列表。
        # 对于SOCP问题，可以分析线性约束的松弛量和对偶值。
        # constr.slack 获取约束的松弛量。对于等式约束，松弛量应接近于0。
        # constr.pi 获取约束的对偶值 (或影子价格)。
        for constr in model.getConstrs():
            print("  {}: 松弛量={:.4f}, 对偶值={:.4f}".format(constr.name, constr.slack, constr.pi))

    else:
        print("\n模型未找到最优解。状态码: {}".format(model.status))
        print("请检查模型定义或尝试调整求解参数。")

    # 8. 将模型写入文件 (可选)
    # model.write() 可以将模型定义保存到文件中。
    # .lp 格式可读性强，便于检查模型定义。
    # .cbf (Conic Benchmark Format) 是锥优化的标准格式。
    model.write("socp_example.lp")
    model.write("socp_example.cbf")
    model.write("socp_example.sol")

except cp.CoptError as e:
    # 捕获COPT特有的错误，例如许可问题、建模错误等。
    print(f"COPT Error: {e.retcode} - {e.message}")
except Exception as e:
    # 捕获其他Python异常。
    print(f"An unexpected error occurred: {e}")
finally:
    # 确保在程序结束时关闭COPT环境，释放所有相关资源。
    if 'env' in locals() and env is not None:
        env.close()
```

# Example 02

## 问题数学定义

假设有 $n$ 种可选资产，我们的目标是确定每种资产的投资权重 $w_i$，以在满足特定风险约束的同时最大化整个投资组合的预期总收益。

**参数定义:**
*   $n$: 资产的总数量。
*   $\mathbf{w} \in \mathbb{R}^n$: 决策变量向量，其中 $w_i$ 是投资于资产 $i$ 的权重。
*   $\mathbf{r} \in \mathbb{R}^n$: 各资产的预期收益率向量。
*   $\mathbf{\Sigma} \in \mathbb{R}^{n \times n}$: 资产收益率的协方差矩阵（半正定）。
*   $\sigma_{max}$: 投资组合能接受的最大风险水平（标准差上限）。

**目标函数：**
最大化投资组合的预期总收益。
$$
\text{最大化} \quad Z = \mathbf{r}^T \mathbf{w} = \sum_{i=1}^{n} r_i w_i
$$

**约束条件：**
1.  **风险约束：** 投资组合的总风险（以收益的标准差衡量）不得超过预设的上限 $\sigma_{max}$。投资组合的方差为 $\mathbf{w}^T \mathbf{\Sigma} \mathbf{w}$，因此标准差为 $\sqrt{\mathbf{w}^T \mathbf{\Sigma} \mathbf{w}}$。
    $$
    \sqrt{\mathbf{w}^T \mathbf{\Sigma} \mathbf{w}} \le \sigma_{max}
    $$
    由于协方差矩阵 $\mathbf{\Sigma}$ 是半正定的，可以通过Cholesky分解得到 $\mathbf{\Sigma} = \mathbf{L}\mathbf{L}^T$，其中 $\mathbf{L}$ 是一个下三角矩阵。因此，约束可以重写为：
    $$
    \sqrt{(\mathbf{L}^T\mathbf{w})^T(\mathbf{L}^T\mathbf{w})} = \|\mathbf{L}^T\mathbf{w}\|_2 \le \sigma_{max}
    $$
    这是一个标准的二阶锥约束。

2.  **预算约束：** 所有资产的投资权重之和必须为1，表示全部资金都被用于投资。
    $$
    \sum_{i=1}^{n} w_i = 1
    $$

**变量范围（边界约束）：**
*   **禁止做空：** 每项资产的投资权重都必须是非负的。
    $$
    w_i \ge 0 \quad \forall i \in \{1, \dots, n\}
    $$

# 求解代码
```python
import coptpy as cp
from coptpy import COPT
import pandas as pd
import numpy as np
from scipy.linalg import cholesky

try:
    # 1. 使用pandas读取并处理数据
    # header: | asset | expected_return | cov_A | cov_B | cov_C | cov_D | cov_E |
    df = pd.read_csv('portfolio_data.csv')
    
    # 提取资产名称、预期收益率和协方差矩阵
    assets = df['asset'].tolist()
    n = len(assets)
    # .values 将pandas Series转换为NumPy数组
    r = df['expected_return'].values
    # 提取以 'cov_' 开头的列，构成协方差矩阵
    cov_cols = [f'cov_{asset.split("_")[1]}' for asset in assets]
    Sigma = df[cov_cols].values

    # 定义模型参数
    sigma_max = 0.12  # 设定最大可接受的投资组合风险（标准差）

    # 2. 对协方差矩阵进行Cholesky分解
    # 这是将 w' * Sigma * w 形式的二次项转换为标准二阶锥约束的关键步骤。
    # L 是一个下三角矩阵，满足 Sigma = L * L'。
    # 因此，w' * Sigma * w = w' * L * L' * w = (L'w)' * (L'w) = ||L'w||^2。
    # cholesky() 函数要求矩阵是正定的。
    try:
        L = cholesky(Sigma, lower=True)
    except np.linalg.LinAlgError:
        print("错误：协方差矩阵不是正定的，无法进行Cholesky分解。")
        exit()

    # 3. 创建COPT求解环境和模型
    env = cp.Envr()
    model = env.createModel("portfolio_optimization_socp")

    # 4. 添加决策变量
    # model.addVars() 批量添加一组变量。
    # n: 变量数量。
    # lb=0.0: 所有变量的下界均为0，代表不允许做空。
    # nameprefix: 变量名称的前缀，COPT会自动添加索引，如 w[0], w[1], ...
    w = model.addVars(n, lb=0.0, nameprefix="w")

    # 5. 设置目标函数
    # 目标是最大化预期收益 r' * w。
    # cp.quicksum() 是一个高效的求和函数，用于构建线性表达式。
    expected_return = cp.quicksum(r[i] * w[i] for i in range(n))
    model.setObjective(expected_return, sense=COPT.MAXIMIZE)

    # 6. 添加约束条件
    # 6.1 添加预算约束：所有权重的总和为1。
    model.addConstr(cp.quicksum(w[i] for i in range(n)) == 1.0, name="budget")
    
    # 原始约束是 ||L'w||_2 <= sigma_max.
    # 由于 model.addCone() 的参数必须是变量(Var)而非表达式(LinExpr)，
    # 我们引入一组辅助变量 y 来代表线性表达式 L'w。
    # 约束被分解为两部分：
    #   a) y = L'w  (一组线性等式约束)
    #   b) ||y||_2 <= sigma_max (一个标准的二阶锥约束)

    # 6.2.a 添加辅助变量 y 和 线性等式约束 y = L'w
    # y的维度与w相同，都是n。我们允许y取任何值，所以不设边界(默认下界为-inf, 上界为+inf)。
    y = model.addVars(n, lb=-COPT.INFINITY, nameprefix="y")
    
    # L.T 是L的转置矩阵。
    # 循环n次，为y的每个分量添加一个等式约束。
    for i in range(n):
        # y[i] == (L.T 的第i行) * w
        lhs_expr = cp.quicksum(L.T[i, j] * w[j] for j in range(n))
        model.addConstr(y[i] == lhs_expr, name=f"aux_y_constr_{i}")

    # 6.2.b 添加二阶锥约束 ||y||_2 <= sigma_max
    # 这个约束等价于 sigma_max >= sqrt(y[0]^2 + y[1]^2 + ...)。
    # addCone的第一个参数是锥的"头部"，其余是锥的"身体"。
    # 注意：第一个参数必须是变量。如果像本例中是常数，需要引入一个辅助变量。
    # 我们引入一个变量 risk_var，并约束它等于 sigma_max。
    risk_var = model.addVar(lb=sigma_max, ub=sigma_max, name="risk_limit_var")
    
    # 构建锥约束的参数列表，第一个是头部变量，后面是身体变量。
    cone_vars = [risk_var]
    cone_vars.extend(y.values()) # y.values()获取tupledict中的所有Var对象
    
    # 添加二阶锥约束，并指定类型为 COPT.CONE_QUAD (标准二阶锥)。
    model.addCone(cone_vars, COPT.CONE_QUAD)

    # 7. 求解模型
    model.solve()

    # 8. 分析求解结果
    if model.status == COPT.OPTIMAL:
        print("\n--- 求解结果 ---")
        print("模型状态: 最优解 (COPT.OPTIMAL)")
        print(f"最大预期收益率: {model.objval:.4%}")
        
        # 从最优解w计算实际风险
        optimal_weights = np.array([v.x for v in w.values()])
        actual_variance = optimal_weights.T @ Sigma @ optimal_weights
        actual_risk = np.sqrt(actual_variance)
        
        print(f"实际投资组合风险 (标准差): {actual_risk:.4f}")
        print(f"风险约束上限: {sigma_max:.4f}")

        print("\n最优资产配置权重:")
        total_weight = 0
        for i in range(n):
            print(f"  {assets[i]}: {w[i].x:.4%}")
            total_weight += w[i].x
        print(f"总权重: {total_weight:.4%}") # 验证权重和为1

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