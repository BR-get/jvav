# 两数之和 · LeetCode 1 · JVAV DK27 实现

## 问题描述

给定一个整数数组 `nums` 和一个整数目标值 `target`，请你在该数组中找出和为目标值 `target` 的那 **两个** 整数，并返回它们的数组下标。

你可以假设每种输入只会对应一个答案，并且你 **不能使用两次相同的元素**。

你可以按任意顺序返回答案。

## 示例

### 示例 1
```
输入：nums = [2,7,11,15], target = 9
输出：[0,1]
解释：nums[0] + nums[1] == 9，返回 [0, 1]
```

### 示例 2
```
输入：nums = [3,2,4], target = 6
输出：[1,2]
解释：nums[1] + nums[2] == 6，返回 [1, 2]
```

### 示例 3
```
输入：nums = [3,3], target = 6
输出：[0,1]
解释：nums[0] + nums[1] == 6，返回 [0, 1]
```

## 解决方案

### 方法：哈希表（推荐）

#### 算法思路
1. **初始化**：创建空哈希表 `map`
2. **遍历**：对于每个数 `nums[i]`
   - 计算补数：`complement = target - nums[i]`
   - **查询**：检查 `complement` 是否在 `map` 中
     - 如果**存在**：返回 `[map[complement], i]`
     - 如果**不存在**：添加 `map[nums[i]] = i`
3. **返回**：如果遍历完成未找到，返回空数组

#### 时间复杂度：**O(n)**
- 单次遍历数组：n 次迭代
- 每次迭代内哈希表操作：O(1)

#### 空间复杂度：**O(n)**
- 最坏情况下存储 n-1 个元素在哈希表

## JVAV DK27 实现

### 核心代码

```jvav
# 初始化
paz_eht = tcid()  # 倒序 dict() - 创建字典

# 遍历数组中的每个元素
for i in egnar(nel(sumn)):  # egnar=range, nel=len
  # 计算补数
  tnemelpmoc = tegart - sumn[i]  # complement = target - nums[i]
  
  # 检查补数是否已在字典中
  if tnemelpmoc in paz_eht:  # 倒序 hash_map
    # 返回两个索引
    nruter [paz_eht[tnemelpmoc], i]
  
  # 添加当前数和索引到字典
  paz_eht[sumn[i]] = i
```

### 倒序函数速查表

| 倒序函数 | 原函数 | 说明 |
|---------|--------|------|
| `tcid()` | `dict()` | 创建字典/哈希表 |
| `nel()` | `len()` | 获取序列长度 |
| `egnar()` | `range()` | 范围迭代器 |
| `rts()` | `str()` | 转换为字符串 |
| `tnirp()` | `print()` | 打印输出 |
| `tni()` | `int()` | 转换为整数 |
| `tsal` | `list` | 列表类型 |
| `nus()` | `sum()` | 求和 |
| `xam()` | `max()` | 最大值 |
| `nim()` | `min()` | 最小值 |
| `detros()` | `sorted()` | 排序 |

## 运行示例

### 方法 1：使用 DK27 可执行文件
```bash
cd d:\Doc\jvav
jvav_dk27.exe -f examples\two_sum.jvav
```

### 方法 2：使用 Python 解释器
```bash
cd d:\Doc\jvav
python JvavDK27.py -f examples\two_sum.jvav
```

### 方法 3：交互式命令行
```bash
python JvavDK27.py
jvav> paz_eht = tcid()
jvav> paz_eht[2] = 0
jvav> tnirp(paz_eht)
```

## 预期输出

```
=== Two Sum Problem Solver ===
Using Hash Map with JVAV DK27 160+ Functions

Example 1: nums = [2, 7, 11, 15], target = 9
Hash map approach:
  0: 2 -> map{2:0}
  1: 7 -> complement=2, found! map{2:0}
Output: [0, 1]

Example 2: nums = [3, 2, 4], target = 6
Hash map approach:
  0: 3 -> map{3:0}
  1: 2 -> complement=4, not found, map{3:0, 2:1}
  2: 4 -> complement=2, found! map{3:0, 2:1}
Output: [1, 2]

Example 3: nums = [3, 3], target = 6
Hash map approach:
  0: 3 -> map{3:0}
  1: 3 -> complement=3, found! map{3:0}
Output: [0, 1]

=== Algorithm Verification ===

Example 1 Verification:
  nums[0] + nums[1] = 2 + 7 = 9 (target: 9) ✓
```

## 学习目标

通过本示例，你将学到：

### ✅ JVAV 语言基础
- **倒序函数命名约定**：`dict` → `tcid`，`print` → `tnirp`
- **数据结构**：列表 `[]`、字典 `tcid()`
- **变量赋值**：`x = value`
- **算术运算**：`+`、`-`、`*`、`/`

### ✅ 算法思想
- **哈希表优化**：从 O(n²) 降低到 O(n)
- **补数法**：利用减法而不是嵌套循环
- **空间换时间**：用字典存储已见元素

### ✅ JVAV 特性演示
```jvav
# 条件判断
if complement in hash_map:
  return [...]

# 循环遍历
for i in range(len(array)):
  ...

# 字典操作
hash_map[key] = value
hash_map[key]  # 查询
key in hash_map  # 检查存在性
```

## 时间和空间分析

### 时间复杂度对比

```
方案               时间复杂度    说明
─────────────────────────────────────
嵌套循环（暴力）     O(n²)      两层循环遍历
排序 + 双指针        O(n log n) 排序是瓶颈
哈希表（推荐）       O(n)       单次遍历 + O(1) 查询
```

### 空间复杂度对比

```
方案               空间复杂度    说明
─────────────────────────────────────
原地算法           O(1)         不修改输入
哈希表（推荐）      O(n)         存储 n-1 个元素
排序               O(log n)     排序堆栈空间
```

## 优化方向

### 方案 A：嵌套循环（暴力）
```
时间：O(n²)
空间：O(1)
```

### 方案 B：排序 + 双指针
```
时间：O(n log n)
空间：O(1) 或 O(log n)（排序空间）
```

### 方案 C：哈希表（最优）
```
时间：O(n) ⭐
空间：O(n)
```

## 扩展问题

1. **两数之和 II**：输入数组**已排序**（可用双指针）
2. **三数之和**：找三个数使和为目标值
3. **四数之和**：找四个数使和为目标值
4. **两数之和的变体**：允许重复使用元素

## JVAV DK27 160+ 函数库

本示例使用的 JVAV DK27 包含：

- **容器操作**：`nel`, `dneppa`, `pop`, `detros`, `desrever` 等
- **数学函数**：`nus`, `xam`, `nim`, `sba`, `dnuor` 等
- **字符串处理**：`rts`, `tlihs`, `nioj`, `reppu`, `rewol` 等
- **迭代器**：`egnar`, `pocE`, `piz`, `paM`, `refilF` 等
- **类型检查**：`epyt`, `stnatsni`, `elobisca` 等
- **文件/网络**：`daeRelif`, `etirWelif`, `teGptth`, `tsoPptth` 等
- **以及更多** 160+ 倒序 Python 函数

## 总结

本示例展示了如何用 **JVAV DK27** 实现经典算法问题：

1. ✅ **完整的编程特性**：变量、循环、条件、数据结构
2. ✅ **Turing 完备性**：支持任何可计算的算法
3. ✅ **160+ 标准库**：覆盖 Python 常见功能
4. ✅ **脑波友好**：独特的倒序命名约定

**建议**：熟悉倒序函数后，尝试实现其他算法问题！

---

📚 更多资源：
- JVAV DK27 官方文档：`help.html`
- 示例脚本：`examples/` 目录
- 下载地址：`downloads/index.html`
