# 文字格式修复总结

## 问题
当前 PPT 生成器存在三类文字布局问题：
1. 文字被截断（要点框高度不足，多行文字显示不完全）
2. 文字超出框线（横向或纵向溢出文本框边界）
3. 同级要点间距不一致且互相遮挡

## 根本原因
- **高度估算偏小**：`deckkit.py` 的文本高度估算系数对中文多行文本不足
- **要点间距不统一**：`bullets()` 方法按实际高度紧凑排列，长短要点的间隙不一致
- **检测阈值过宽松**：`render_review.py` 的溢出容差对中文文本太大

## 修复方案

### 1. deckkit.py - 提高高度估算安全系数
- **`text()` 方法**：单行文字高度从 `fpx(pt) * 1.5` 增至 `1.6`
- **`para()` 方法**：多行段落高度从 `n * fpx(pt) * lh * 1.2` 增至 `1.3`
- **`bullets()` 方法**：改为统一行高布局
  - 预先计算所有要点的最大高度
  - 每个要点分配相同的垂直空间（max_h + gap）
  - 确保长短要点间距一致

### 2. render_review.py - 收紧溢出检测
- 横向容差从 16px 降至 12px
- 纵向容差从 `tol+4` (7px) 降至 `tol+2` (5px)
- 报告信息更明确（"wider than box" 替代 "wider than its box"）

### 3. validate_deck.py - 增加密度预警
- 检查文本框字符密度（字符数 / 面积）
- 超过 200 字且密度 > 8 chars/100px² 时发出 NOTE
- 不阻断构建，仅提示可能的排版问题

### 4. WORKFLOW.md - 加入检查清单
在第 9 步 Review loop 增加：
- **Clipped text**：底部截断
- **Overflow**：超出边界
- **Uneven spacing**：间距不一致或重叠
- **Misaligned elements**：元素偏移

## 修改文件
- `C:/Users/16947/.claude/skills/paper-ppt/tools/deckkit.py`
- `C:/Users/16947/.claude/skills/paper-ppt/tools/render_review.py`
- `C:/Users/16947/.claude/skills/paper-ppt/tools/validate_deck.py`
- `C:/Users/16947/.claude/skills/paper-ppt/WORKFLOW.md`

## 测试建议
用当前出问题的 PPT 重新构建，检查：
1. 要点列表的垂直间距是否均匀
2. 多行文字是否完整显示
3. `review/audit.json` 中的 `auto_issues` 是否减少

## 后续优化（可选）
1. 从 harnessdev-deck-native.pptx 实测要点间距，替换当前 gap=12 的魔数
2. 如果问题仍存在，可进一步提高系数至 1.35 或 1.4
3. 对特殊场景（公式、代码）可以单独加更大的安全边距
