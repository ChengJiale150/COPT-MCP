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
    # COPT.CONE_QUAD 指定了约束类型为标准二阶锥 (Standard Second-Order Cone)。
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

