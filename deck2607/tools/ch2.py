"""Chapter 2: taxonomy and corpus."""
import art
from deckkit import C, measure
from kit import slide, rp, boxtext, head, lead, concl, rpanel, tag, chip, toc


@slide('toc')
def toc2(cv, n):
    toc(cv, 1)
    return '目录：第二章 分类框架与语料（论文 §2.2–§2.3、Table 1、Figure 1、§8 语料形态）。'


@slide()
def taxonomy(cv, n):
    head(cv, '2.1 两轴分类', '文献主体在"人在环上"一行')
    lead(cv, '**轴一：改进什么**——部署时行为、训练中的策略、评估器、研究过程本身；**轴二：闭环程度**——谁来验证改进。'
             '1,250 篇几乎都在研究**有界自我精炼**，**开放式 RSI** 极少。')
    X, CW, RH = 250, 290, 128        # grid origin x, column width, row height
    cv.svg(art.hline_arrow(4 * CW), X, 276, 4 * CW, 22, name='轴一箭头')
    cv.text('改进什么 →', 146, 322, pt=18, bold=True, color=C['navy'], align='c')
    cv.text('谁来验证 ↓', 146, 372, pt=18, bold=True, color=C['navy'], align='c')
    cv.line(48, 347, 244, 347, color=C['line'], lw=1.5)
    cols = [('部署时自进化', '§3 · 393 篇', 'gearchat_w'), ('训练时自迭代', '§4 · 340 篇', 'weights_w'),
            ('自评估', '§5 · 318 篇', 'gauge_w'), ('自主科研', '§6 · 139 篇', 'flask_w')]
    HY = 306
    for j, (t, sub, ic) in enumerate(cols):
        x = X + j * CW
        cv.box(x + 3, HY, CW - 6, 88, fill=C['blue'], name=f'列头 {t}')
        cv.icon_c(ic, x + 44, HY + 44, 46, name=f'图标 {t}')
        cv.text(t, x + 78, HY + 28, pt=20, bold=True, color=C['white'])
        cv.text(sub, x + 78, HY + 64, pt=16, color='DDEFEE')
    rows = [('人在环中', '人审每次改动'), ('人在环上', '自动信号+人审'), ('闭环', '系统自己验证')]
    cells = [['AI 辅助编码、手工提示、人工设计的智能体', '人工整理数据、RLHF 基线', '专家量规、人工基准设计', '人主导、AI 辅助的研究'],
             ['Self-Refine、执行修复、测试时训练、技能库', 'STaR、自奖励 LM、在线策略自蒸馏', '过程奖励、LLM-as-judge、经审计的分类', 'FunSearch、AlphaEvolve、AI Scientist'],
             ['Darwin Gödel Machine、沙箱内自我修改', '零数据自博弈：Absolute Zero、R-Zero、Agent0', '自奖励裁判、元评估、评估器协同进化', 'A-Evolve-Training 自主后训练闭环']]
    GY = HY + 94
    cv.svg(art.vline_arrow(3 * RH, up=False), 16, GY, 24, 3 * RH, name='轴二箭头')
    for i, (rt, rs) in enumerate(rows):
        y = GY + i * RH
        mid = i == 1
        cv.box(46, y + 3, 200, RH - 6, fill=C['pale'] if mid else 'F4F6F6', line=C['line'], lw=1, name=f'行头 {rt}')
        cv.text(rt, 146, y + 44, pt=20, bold=True, color=C['rose'] if i == 2 else C['navy'], align='c')
        cv.text(rs, 146, y + 86, pt=16, color=C['grey'], align='c')
        for j, s in enumerate(cells[i]):
            x = X + j * CW
            hot = i == 2 and j == 2
            boxtext(cv, s, x + 3, y + 3, CW - 6, RH - 6, pt=16, fill=C['pale'] if mid else C['white'],
                    line=C['rose'] if hot else C['line'], lw=3 if hot else 1, r=6, lh=1.2, pad=12)
    # right-hand brackets
    BX = X + 4 * CW + 14
    cv.line(BX, GY + 6, BX, GY + 2 * RH - 6, color=C['blue'], lw=3)
    rp(cv, '有界\n自我精炼\n§3–6 主体', BX + 14, GY + 60, 150, pt=18, bold=True, color=C['blue'])
    cv.line(BX, GY + 2 * RH + 6, BX, GY + 3 * RH - 6, color=C['rose'], lw=3)
    rp(cv, '开放式\nRSI 稀少', BX + 14, GY + 2 * RH + 18, 150, pt=18, bold=True, color=C['rose'])
    concl(cv, '最关键的格子是**"自评估 × 闭环"**：系统改写自己对"更好"的定义，有界精炼由此滑向开放式 RSI', y=836)
    return ('论文 p.4–5 §2.2 两轴分类与 Figure 1（4×3 网格与代表系统）。轴一四类：部署时自进化（§3）、训练时自迭代（§4）、自评估（§5）、'
            '自主科研（§6）；轴二：human-in-the-loop / human-on-the-loop / closed loop。密度集中在中间一行；闭环行处处稀疏且越往右越薄，'
            '最关键格子是自评估 × 闭环。论文数取自 Table 1。格内代表系统按 Figure 1 转写。')


@slide()
def corpus(cv, n):
    head(cv, '2.2 语料与方法', '1,250 篇 = 种子 871 + 补充 379')
    lead(cv, '语料分两阶段构建：**种子采集**沿七条主线检索 arXiv（2024–2026），**定向补充**覆盖自评估方法、测试时训练、零数据自博弈三个'
             '种子检索欠覆盖的方向；全部论文映射到**四类技术类别 + 基础族**。')
    # left: harvest flow
    cv.label_box('采集流程', 20, 290, 380, 46, pt=20, fill=C['blue'], r=4)
    cv.icon_c('docs_w', 372, 313, 34, name='文档图标')
    nodes = [('arXiv 检索 7 条主线 + OpenAlex 元数据', False), ('种子语料 871 篇', True),
             ('分类对齐：规则 + 人工纠正，89 篇改类', False), ('定向补充 379 篇', True), ('合并语料 1,250 篇', True)]
    y = 352
    for k, (s, strong) in enumerate(nodes):
        h = 88 if not strong else 50
        boxtext(cv, s, 40, y, 340, h, pt=18, bold=strong, color=C['white'] if strong else C['text'],
                fill=C['gold'] if strong else C['pale'], line=None if strong else C['blue'], r=8, pad=12)
        if k < len(nodes) - 1:
            cv.arrow(210, y + h + 1, 210, y + h + 15, color=C['blue'], lw=2.5)
        y += h + 16
    # middle: category bars (Table 1)
    cv.label_box('五类语料分布（Table 1）', 430, 290, 700, 46, pt=20, fill=C['blue'], r=4)
    cats = [('部署时自进化', 393, '74%'), ('训练时自迭代', 340, '69%'), ('自评估', 318, '82%'),
            ('自主科研', 139, '76%'), ('基础、极限与安全', 60, '57%')]
    cv.text('论文数', 900, 362, pt=16, color=C['grey'], align='c')
    cv.text('2026 年占比', 1070, 362, pt=16, color=C['grey'], align='c')
    for k, (t, v, pc) in enumerate(cats):
        cy = 408 + k * 66
        cv.text(t, 640, cy, pt=18, bold=True, color=C['navy'], align='r')
        cv.box(656, cy - 16, 260 * v / 393, 32, fill=C['blue'] if k != 2 else C['gold'], name=f'条 {t}')
        cv.text(str(v), 656 + 260 * v / 393 + 10, cy, pt=18, bold=True, color=C['text'])
        cv.label_box(pc, 1030, cy - 18, 80, 36, pt=18, color=C['rose'] if k == 2 else C['navy'],
                     fill=C['paleRose'] if k == 2 else C['pale'], r=18)
    rp(cv, '自评估 2026 占比最高（**82%**），正成为独立研究方向', 440, 724, 680, pt=17, color=C['grey'])
    # right: limitations
    cv.card(1160, 290, 420, 510, fill='ECF6F6', line=None, r=6, shadow=False, name='局限')
    cv.text('局限：', 1180, 322, pt=22, bold=True, color='1A1A1A')
    rp(cv, '1）是样本不是普查：检索深度上限偏向近期高产主线\n'
           '2）**74%** 发表于 2026，引用数接近 0，**不能当作影响力**\n'
           '3）约 **54/379** 篇补充论文为检索溢出，计入总数但不作证据\n'
           '4）前沿实验室内部实践只能通过其公开发表观察',
       1180, 352, 384, pt=17, lh=1.3)
    concl(cv, '部署时与训练时两类合计 **733 篇，占 58.6%**；增长统计只用种子语料，避免补充检索的近期偏差', y=836)
    return ('论文 p.3 Table 1：部署时自进化 393 篇（2026 占 74%）、训练时自迭代 340（69%）、自评估 318（82%）、自主科研 139（76%）、'
            '基础/极限/安全 60（57%）。p.5–6 §2.3：种子采集 7 条主线得 871 篇；规则分类使 89 篇种子论文离开默认类，另有 3 处在写作中纠正；'
            '定向补充 379 篇。Limitations：样本非普查、74% 发表于 2026、约 54/379 为检索溢出、前沿实验室审查效应；Figure 6 增长统计只用种子语料。'
            '733/1,250 = 58.6% 为由 Table 1 计算。')


@slide()
def growth(cv, n):
    head(cv, '2.3 领域形态', '增长快于沉淀，分布不均')
    lead(cv, '种子语料的季度产出从 2024 年初的**个位数**增长到 2026Q2 的**约 500 篇**；部署时与训练时工作在每个季度都占主导，'
             '自主科研少 2–3 倍，基础族最小。论文给出**四个可检验的假设**解释这种不均。')
    kpis = [('74%', '语料发表于 2026 年'), ('≈500 篇', '2026Q2 单季产出（种子语料）'), ('56 篇', 'OPSD 主线：18 个月前尚不存在')]
    for k, (v, l) in enumerate(kpis):
        y = 298 + k * 172
        cv.card(20, y, 500, 156, fill=C['blue'] if k != 1 else C['navy'], line=None, r=8, shadow=True, name=f'指标 {v}')
        cv.text(v, 48, y + 58, pt=40, bold=True, color=C['white'])
        rp(cv, l, 48, y + 98, 466, pt=18, color='DDEFEE')
        if k == 1:
            cv.icon_c('trend_w', 450, y + 60, 76, name='增长趋势')
    hyp = [('steps', '可验证性梯度', '两大类集中在有廉价验证器的代码、数学：实验快、易发表——§5.2 的方法梯度也在左右选题'),
           ('coins', '入门成本梯度', '推理时精炼只需 API 额度，训练环要 GPU，自主科研要实验室级算力：论文数随成本下降'),
           ('herd', '羊群效应', 'OPSD 几个月内从零到几十篇：可读、可基准化决定注意力流向，而非重要性'),
           ('institution', '机构分工', '评估长期是方法论文里的"管道"；理论与治理既无基准也无产品路线奖励，基础族仅 60/1,250')]
    for k, (ic, t, b) in enumerate(hyp):
        x, y = 548 + (k % 2) * 522, 298 + (k // 2) * 260
        cv.card(x, y, 502, 244, fill=C['white'], line=C['blue'], r=10, shadow=True, name=f'假设 {t}')
        cv.icon_c(ic, x + 46, y + 44, 48, name=f'图标 {t}')
        cv.text(t, x + 84, y + 44, pt=22, bold=True, color=C['blue'])
        rp(cv, b, x + 24, y + 86, 440, pt=18, lh=1.3)
    concl(cv, '论文主张的耐久性在于**结构（两轴 + 验证层级）**，而非论文清单', y=836)
    return ('论文 p.2 §1 与 p.25 §8：74% 语料发表于 2026；种子语料季度产出从 2024 初个位数到 2026Q2 约 500 篇（Figure 6，2026Q3 不完整已略去）；'
            'OPSD 主线 56 篇，18 个月前不存在。p.25–27 四个假设：verifiability gradient、cost-of-entry gradient、herd dynamics、'
            'institutional role assignment；论文明确说明是假设而非结论，并提醒原始比例部分反映了采样设计。基础族 60/1,250。')
