"""Academic paper presentation: Recursive Self-Improvement in AI
From the paper: arXiv:2607.07663v1 (Mingguang Chen et al., 2026)
Generates a native, editable PPTX presentation.

Usage:
    python -I tools/build_deck.py output.pptx
"""
import sys
import tempfile
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE

sys.path.insert(0, str(Path(__file__).parent))
from deckkit import (C, SLIDE_H, SLIDE_W, Canvas, IconStore, ICON_LABEL, ICON_SVG,
                     fpx, lighten, measure, notes)

SLIDES = []

def slide(fn):
    """Decorator to register slide functions."""
    SLIDES.append(fn)
    return fn

# Override colors to match power industry PPT theme
C['navy'] = '4874CB'    # Primary blue from reference PPT
C['blue'] = '4874CB'
C['gold'] = 'F2BA02'    # Yellow accent
C['orange'] = 'EE822F'  # Orange for emphasis
C['green'] = '75BD42'   # Green accent
C['pale'] = 'E7E6E6'    # Light grey background

# ================================================================ 1. TITLE
@slide
def s_title(cv, n):
    """Cover slide."""
    cv.text('AI递归自我改进综述', 92, 120, pt=18, bold=True, color=C['blue'])
    cv.box(92, 155, 120, 6, fill=C['gold'], name='标题装饰线')

    cv.text('递归自我改进：从有界自精化', 92, 220, pt=44, bold=True, color=C['navy'])
    cv.text('到自主研究闭环', 92, 290, pt=44, bold=True, color=C['navy'])

    cv.para('系统综述 1250 篇论文 · 2024-2026', 92, 380, 800, pt=20, color=C['grey'])
    cv.para('Mingguang Chen (UCR) · Licheng Wang (AlphaAvatar) · Bo Qu (IIT)',
            92, 440, 800, pt=18, color=C['grey'])
    cv.para('arXiv:2607.07663v1 · July 2026', 92, 490, 800, pt=16, color=C['grey'])

    # Illustration: recursive loop
    g = cv.group('封面插图')
    g.card(950, 200, 550, 500, fill=C['pale'])
    g.circle(1225, 350, 80, fill=lighten(C['blue'], 0.8), line=C['blue'])
    g.icon_c('robot_blue', 1225, 350, 60)
    # Curved arrow suggesting loop
    g.arrow(1225, 450, 1320, 500, color=C['blue'])
    g.arrow(1320, 500, 1320, 600, color=C['blue'])
    g.arrow(1320, 600, 1130, 600, color=C['blue'])
    g.arrow(1130, 600, 1130, 450, color=C['blue'], dash=True)
    g.text('自我改进循环', 1225, 620, pt=16, color=C['navy'], align='c')

    return '开场：AI系统越来越多地参与自身改进——从修正输出到训练数据生成，再到自主研究。本综述梳理2024-2026年间1250篇论文，构建统一分类框架。'


# ================================================================ 2. BACKGROUND
@slide
def s_background(cv, n):
    cv.title('研究背景：AI参与自我改进的浪潮加速')

    # Timeline illustration
    g = cv.group('演进时间线')
    timeline = [
        (200, 'Pre-2023\n人工编写\n所有代码', C['grey']),
        (450, '2023-24\nChatbot\n辅助编码', C['blue']),
        (700, '2025\n自主编码\n代理', lighten(C['blue'], 0.7)),
        (950, '2026 Q2\nClaude写80%\n合并代码', C['orange']),
        (1200, '未来?\n完全闭环\n自主研究', C['gold'])
    ]

    # Draw timeline
    cv.box(150, 300, 1100, 3, fill=C['line'])
    for x, label, col in timeline:
        cv.circle(x, 300, 12, fill=col, line=None)
        cv.para(label, x - 60, 330, 120, pt=16, color=C['text'], align='c')

    # Stats box
    p = cv.group('论文爆发增长')
    p.card(150, 480, 1300, 180, fill=lighten(C['pale'], 0.5))
    p.text('2026年Q2季度产出：~500篇论文', 200, 520, pt=24, bold=True, color=C['navy'])
    p.text('总计综述：1250篇（74%发表于2026年）', 200, 580, pt=20, color=C['text'])

    cv.band('文献爆发式增长，但术语混乱掩盖了本质差异')
    return '讲稿：从2023年前人工编码，到2026年Claude已写80%合并代码。文献季度产出从个位数增至500篇，急需统一框架整理。'


# ================================================================ 3. PROBLEM
@slide
def s_problem(cv, n):
    cv.title('核心问题："self-X"术语遍地开花但含义不清')

    # Messy terminology cloud
    g = cv.group('术语混乱')
    g.card(100, 180, 680, 500, fill=C['pale'])
    terms = [
        ('self-refine', 180, 220, 18),
        ('self-reward', 320, 260, 20),
        ('self-play', 480, 230, 18),
        ('self-distill', 200, 320, 17),
        ('self-evolve', 420, 340, 19),
        ('self-verify', 250, 400, 18),
        ('self-improve', 360, 470, 22),
        ('self-train', 520, 390, 17),
    ]
    for term, x, y, sz in terms:
        g.text(term, x, y, pt=sz, color=C['grey'], bold=True)
    g.text('?', 400, 550, pt=64, color=C['orange'], bold=True, align='c')

    # Real differences
    p = cv.group('实际差异巨大')
    p.card(820, 180, 680, 500, fill=C['white'])
    p.text('同一术语，不同含义：', 870, 220, pt=20, bold=True, color=C['navy'])
    items = [
        '推理时输出修正（Self-Refine）',
        '训练循环用自生成数据（STaR）',
        '代理重写自身工具链（G代码Agent）',
        '自主进行AI研究（AI Scientist）'
    ]
    p.bullets(items, 870, 280, 580, pt=18)

    p.text('风险等级和技术复杂度相差数个量级', 870, 540, pt=18, color=C['orange'], bold=True)

    cv.band('需要明确区分有界改进与开放式递归自我改进（RSI）')
    return '讲稿：文献中"self-X"术语混用，从简单的输出修正到完全自主研究都叫"自我改进"，但技术实现和风险完全不同。'


# ================================================================ 4. TAXONOMY
@slide
def s_taxonomy(cv, n):
    cv.title('二维分类法：改进对象 × 闭环程度')

    # Axes explanation
    g = cv.group('分类轴')
    g.text('改进对象（What to improve）', 120, 190, pt=20, bold=True, color=C['navy'])
    items_what = [
        '部署时行为（输出、权重、工具链）',
        '训练策略（通过离线训练迭代）',
        '评估器（定义"更好"的信号）',
        '研究过程（自主科研）'
    ]
    g.bullets(items_what, 140, 240, 600, pt=17)

    p = cv.group('闭环程度')
    p.text('闭环程度（Loop closure）', 850, 190, pt=20, bold=True, color=C['navy'])
    items_how = [
        '人在环中：每步人工决策',
        '人工审核：自动生成+人工批准',
        '完全闭环：无人干预'
    ]
    p.bullets(items_how, 870, 240, 600, pt=17)

    # Matrix preview
    cv.card(120, 460, 1360, 200, fill=C['pale'])
    cv.text('4类改进 × 3级闭环 = 统一分类框架', 140, 500, pt=24, bold=True, color=C['navy'])
    cv.text('本综述将1250篇论文分入4大类别（下页展开）', 140, 560, pt=20, color=C['text'])

    cv.band('首次构建跨越全谱系的分类法，从有界到开放式RSI')
    return '讲稿：我们提出二维分类法——纵轴是改进对象（4类），横轴是闭环程度（3级）。这个框架清晰区分工业实践的有界改进与理论讨论的开放式RSI。'


# ================================================================ 5. CATEGORY 1
@slide
def s_cat1_deploy(cv, n):
    cv.title('类别1：部署时自我改进（393篇，74%发表于2026）')

    # Three sub-types
    boxes = [
        ('输出精化', 150, 200, 'Self-Refine\n推理时修正', C['blue']),
        ('测试时训练', 580, 200, '动态调整权重\n适应当前查询', lighten(C['blue'], 0.7)),
        ('工具链进化', 1010, 200, '代理重写自身\n脚手架代码', lighten(C['blue'], 0.5))
    ]

    for title, x, y, desc, col in boxes:
        cv.card(x, y, 380, 220, fill=lighten(col, 0.85), line=col)
        cv.text(title, x + 20, y + 20, pt=22, bold=True, color=col)
        cv.para(desc, x + 20, y + 80, 340, pt=18, color=C['text'])

    # Characteristics
    cv.card(150, 480, 1300, 180, fill=C['white'])
    cv.text('特点：', 180, 510, pt=20, bold=True, color=C['navy'])
    traits = [
        '✓ 快速收敛：数步内达到最优',
        '✓ 可评估性：改进可验证',
        '✓ 工业实践：已广泛部署'
    ]
    x_offset = 180
    for trait in traits:
        cv.text(trait, x_offset, 560, pt=18, color=C['text'])
        x_offset += 420

    cv.band('有界自精化 = 已成熟的工业技术')
    return '讲稿：部署时改进是最成熟的类别。输出精化如Self-Refine在几轮内收敛，测试时训练动态适配任务，工具链进化让代理自我优化脚手架。这些都是有界的、可控的改进。'


# ================================================================ 6. CATEGORY 2
@slide
def s_cat2_train(cv, n):
    cv.title('类别2：训练时自我迭代（340篇，69%发表于2026）')

    # Four sub-threads
    threads = [
        ('自奖励RL', 200, 'Self-Rewarding\nLM', C['blue']),
        ('CoT自训练', 500, 'STaR\n思维链迭代', lighten(C['blue'], 0.7)),
        ('自蒸馏', 800, '知识蒸馏\n到自身', lighten(C['blue'], 0.5)),
        ('自博弈', 1100, 'AlphaGo式\n零数据训练', lighten(C['blue'], 0.3))
    ]

    for title, cx, desc, col in threads:
        cv.circle(cx, 260, 60, fill=lighten(col, 0.85), line=col)
        cv.icon_c('gear_blue', cx, 260, 40)
        cv.text(title, cx, 350, pt=18, bold=True, color=col, align='c')
        cv.para(desc, cx - 70, 390, 140, pt=16, color=C['text'], align='c')

    # Key insight
    cv.card(150, 500, 1300, 160, fill=lighten(C['orange'], 0.9))
    cv.text('核心依赖：可验证的改进信号', 180, 530, pt=22, bold=True, color=C['orange'])
    cv.para('代码/数学等有明确正确答案的领域表现优异；开放域任务易出现退化',
            180, 580, 1240, pt=18, color=C['text'])

    cv.band('训练时迭代 = 需要强验证信号才能避免坍塌')
    return '讲稿：训练时迭代包括自奖励RL、思维链自训练等。关键发现：在代码、数学等可验证领域效果好，但开放域任务容易出现模型坍塌和多样性丢失。'


# ================================================================ 7. CATEGORY 3 INTRO
@slide
def s_cat3_eval_intro(cv, n):
    cv.title('类别3：自我评估——改进循环的支柱（318篇，82%发表于2026）')

    # Central position of evaluator
    g = cv.group('评估器中心地位')
    cv.circle(800, 350, 120, fill=lighten(C['gold'], 0.85), line=C['gold'])
    cv.text('评估器', 800, 340, pt=28, bold=True, color=C['gold'], align='c')

    # Four dependent loops
    loops = [
        ('输出精化', 300, 250, 'arrow_right'),
        ('训练迭代', 300, 450, 'arrow_right'),
        ('研究自动化', 1300, 250, 'arrow_left'),
        ('方向设定', 1300, 450, 'arrow_left')
    ]

    for label, x, y, direction in loops:
        if 'right' in direction:
            cv.arrow(x + 120, y, 670, 350, color=C['blue'])
        else:
            cv.arrow(930, 350, x - 120, y, color=C['blue'])
        cv.card(x - 90, y - 40, 180, 80, fill=C['white'], line=C['line'])
        cv.text(label, x, y, pt=18, bold=True, color=C['navy'], align='c')

    # Bottom message
    cv.card(200, 560, 1200, 100, fill=lighten(C['orange'], 0.9))
    cv.text('每个改进循环都是一个断言：某个信号可以替代人类判断',
            220, 590, pt=20, bold=True, color=C['orange'])

    cv.band('评估器可靠性 = 自我改进的上限')
    return '讲稿：自我评估是所有改进类别的共同依赖。无论输出精化、训练迭代还是自动研究，都需要可靠的评估器。每个"自我改进"声明本质上是说某个信号可以替代人类判断。'


# ================================================================ 8. VERIFICATION HIERARCHY
@slide
def s_verification_hierarchy(cv, n):
    cv.title('验证层级：从形式证明到内在自评（强→弱）')

    # Hierarchy pyramid
    levels = [
        (800, 200, '形式验证器', 'Coq证明检查器', C['green'], 500),
        (800, 300, '执行反馈', '单元测试+编译器', lighten(C['green'], 0.7), 650),
        (800, 400, '过程奖励模型', 'PRM-style标注', lighten(C['blue'], 0.7), 800),
        (800, 500, 'LLM判别器', 'GPT-4-as-judge', lighten(C['orange'], 0.7), 950),
        (800, 600, '内在自评', '模型评估自身', C['orange'], 1100)
    ]

    for i, (cx, y, label, example, col, w) in enumerate(levels):
        cv.box(cx - w // 2, y - 35, w, 70, fill=lighten(col, 0.85), line=col, r=8)
        cv.text(f'{5 - i}. {label}', cx - w // 2 + 20, y - 15, pt=20, bold=True, color=col)
        cv.text(f'例：{example}', cx - w // 2 + 20, y + 15, pt=16, color=C['grey'])

    # Correlation annotation
    cv.arrow(1380, 220, 1380, 580, color=C['navy'])
    # cv.text('改进强度', 1420, 390, pt=18, bold=True, color=C['navy'])  # Vertical text not supported

    cv.band('验证强度 ↑ = 可证明改进 ↑（代码/数学优于开放域）')
    return '讲稿：我们总结出验证层级：最强的是形式验证（Coq等），然后是执行反馈，再到过程奖励模型，LLM判别器，最弱的是内在自评。论文证据显示：验证强度越高，自我改进效果越稳定。'


# ================================================================ 9. FAILURE MODES
@slide
def s_failure_modes(cv, n):
    cv.title('三大失效模式：验证层级被违反时的典型故障')

    # Three failure boxes
    failures = [
        ('自我确认循环', 180, 200,
         ['评估器被优化目标劫持', '模型学会"讨好"判别器', '改进信号失去独立性'],
         C['orange']),
        ('模型坍塌', 580, 200,
         ['自训练导致多样性丢失', '输出趋同、创造力下降', 'Mode collapse典型表现'],
         lighten(C['orange'], 0.7)),
        ('方向设定瓶颈', 980, 200,
         ['人类仍需定义研究方向', '评估器无法判断问题价值', '验证层级的顶层断裂'],
         lighten(C['orange'], 0.5))
    ]

    for title, x, y, points, col in failures:
        cv.card(x, y, 380, 260, fill=lighten(col, 0.85), line=col)
        cv.text(title, x + 20, y + 20, pt=20, bold=True, color=col)
        for i, pt in enumerate(points):
            cv.text(f'• {pt}', x + 20, y + 80 + i * 50, pt=17, color=C['text'])

    # Evidence note
    cv.card(180, 520, 1200, 140, fill=C['pale'])
    cv.text('文献证据：所有三种失效都与弱验证信号强关联', 220, 550, pt=20, bold=True, color=C['navy'])
    cv.para('318篇自评估论文中，使用内在自评或弱判别器的研究报告更高的坍塌率和奖励黑客现象',
            220, 595, 1120, pt=18, color=C['text'])

    cv.band('失效模式追溯到评估器设计缺陷')
    return '讲稿：当验证不够强时，出现三种典型失效：自我确认循环（判别器被劫持）、模型坍塌（多样性丢失）、方向设定瓶颈（人类仍需把控问题选择）。文献显示这些失效与弱验证信号强关联。'


# ================================================================ 10. CATEGORY 4
@slide
def s_cat4_research(cv, n):
    cv.title('类别4：自动化研究（139篇，76%发表于2026）')

    # Two main approaches
    g = cv.group('AI科学家')
    g.card(150, 200, 620, 280, fill=lighten(C['blue'], 0.85), line=C['blue'])
    g.text('AI Scientist', 180, 230, pt=24, bold=True, color=C['blue'])
    g.para('端到端生成研究论文\n包括假设、实验、写作\n输出流畅但声明难审计',
           180, 290, 560, pt=18, color=C['text'])
    g.icon_c('doc_blue', 450, 390, 60)

    p = cv.group('进化式发现')
    p.card(830, 200, 620, 280, fill=lighten(C['green'], 0.85), line=C['green'])
    p.text('FunSearch / AlphaEvolve', 860, 230, pt=24, bold=True, color=C['green'])
    p.para('进化算法搜索新算法\n发现优于人类的解法\n成果可验证（代码执行）',
           860, 290, 560, pt=18, color=C['text'])
    p.icon_c('code', 1130, 390, 60)

    # Current limitation
    cv.card(150, 540, 1300, 120, fill=lighten(C['orange'], 0.9))
    cv.text('现状：执行能力强，方向设定仍需人类', 180, 570, pt=22, bold=True, color=C['orange'])
    cv.para('Claude已写80%合并代码，但"选择做什么"仍是人类决策的堡垒',
            180, 610, 1240, pt=18, color=C['text'])

    cv.band('自动研究 = 最接近"完全闭环"但尚未到达')
    return '讲稿：自动研究包括AI科学家和进化式程序发现。前者生成完整论文但难审计，后者在可验证领域（代码）表现突出。关键瓶颈：方向设定（研究问题选择）仍需人类。'


# ================================================================ 11. ANTHROPIC FRAMEWORK
@slide
def s_anthropic_stages(cv, n):
    cv.title('闭环进展：Anthropic的五阶段自主性框架')

    # Five stages as progression
    stages = [
        (1, '人工编码', 'Pre-2023\n人类写所有代码', 220, C['grey']),
        (2, 'Chatbot辅助', '2023-24\nCopilot式工具', 420, lighten(C['blue'], 0.8)),
        (3, '自主代理', '2025\nClaude Code', 620, lighten(C['blue'], 0.6)),
        (4, '代理协作', '2026\n多代理委派', 820, lighten(C['blue'], 0.4)),
        (5, '完全闭环', '未来\n设计+训练后继', 1020, C['orange'])
    ]

    for num, title, desc, cx, col in stages:
        cv.card(cx - 80, 220, 160, 200, fill=lighten(col, 0.85), line=col)
        cv.text(f'阶段{num}', cx, 250, pt=20, bold=True, color=col, align='c')
        cv.para(f'{title}\n\n{desc}', cx - 60, 295, 120, pt=16, color=C['text'], align='c')

    # Current position arrow
    cv.arrow(780, 460, 780, 500, color=C['navy'], lw=3)
    cv.text('← 我们在这里', 700, 520, pt=18, bold=True, color=C['navy'])
    cv.text('Claude写80%代码，方向仍需人类', 580, 555, pt=16, color=C['grey'])

    cv.band('执行自主性高，研究方向设定仍是人类堡垒')
    return '讲稿：Anthropic提出五阶段框架。当前处于阶段3-4之间：Claude写80%合并代码（执行层面），但研究方向选择仍需人类。最后的"完全闭环"（代理设计并训练后继模型）尚未到达。'


# ================================================================ 12. THREE CONSTRAINTS
@slide
def s_constraints(cv, n):
    cv.title('三重约束限制开放式RSI')

    # Three constraint blocks
    constraints = [
        ('接地需求', 250, 'Grounding\nRequirement',
         ['改进需要可验证信号', '无接地 → 幻觉循环', '人类评估是最终锚点'],
         C['blue']),
        ('坍塌动力学', 650, 'Collapse\nDynamics',
         ['自训练易失去多样性', 'Mode collapse风险', '需外部注入新颖性'],
         lighten(C['blue'], 0.7)),
        ('计算约束', 1050, 'Compute\nConstraints',
         ['每轮改进成本递增', '评估成本 > 生成成本', '经济可行性边界'],
         lighten(C['blue'], 0.5))
    ]

    for title, cx, en_label, points, col in constraints:
        cv.card(cx - 160, 200, 320, 320, fill=lighten(col, 0.85), line=col)
        cv.text(title, cx, 230, pt=22, bold=True, color=col, align='c')
        cv.text(en_label, cx, 265, pt=16, color=C['grey'], align='c')
        for i, pt in enumerate(points):
            cv.text(f'• {pt}', cx - 140, 320 + i * 50, pt=17, color=C['text'])

    # Summary
    cv.card(150, 580, 1300, 80, fill=C['pale'])
    cv.text('当前证据表明：三重约束在所有可测量侧面都限制着开放式RSI',
            180, 605, pt=20, bold=True, color=C['navy'])

    cv.band('RSI理论 vs. 实证：约束明显强于加速')
    return '讲稿：开放式RSI面临三重约束：接地需求（改进需可验证）、坍塌动力学（自训练失去多样性）、计算约束（评估比生成更贵）。当前所有可测证据显示这些约束强于加速效应。'


# ================================================================ 13. GOVERNANCE GAP
@slide
def s_governance_gap(cv, n):
    cv.title('治理缺口：缺少可测量的RSI指标')

    # Imbalance illustration
    g = cv.group('技术 vs 治理')
    # Left: abundant technical papers
    g.card(150, 220, 550, 360, fill=lighten(C['blue'], 0.85), line=C['blue'])
    g.text('技术文献', 180, 250, pt=24, bold=True, color=C['blue'])
    g.text('1250篇论文', 180, 300, pt=48, bold=True, color=C['blue'])
    g.para('方法、算法、实验\n评估器、训练循环\n代理架构、研究自动化',
           180, 380, 490, pt=18, color=C['text'])
    g.icon_c('chart', 420, 490, 60)

    # Right: sparse governance tools
    p = cv.group('治理工具')
    p.card(760, 220, 700, 360, fill=lighten(C['orange'], 0.85), line=C['orange'])
    p.text('治理工具', 790, 250, pt=24, bold=True, color=C['orange'])
    p.text('??? 篇', 790, 300, pt=48, bold=True, color=C['orange'])
    p.para('如何测量RSI能力？\n如何监管闭环系统？\n如何审计改进声明？\n\n→ 最欠缺的研究领域',
           790, 380, 640, pt=18, color=C['text'])
    p.icon_c('warn_rose', 1100, 490, 60)

    cv.band('技术加速 >> 治理准备度')
    return '讲稿：文献呈现巨大不平衡：1250篇技术论文详细描述方法，但治理级别的RSI测量工具几乎空白。如何测量系统的自我改进能力、如何监管完全闭环系统——这是最欠缺的研究方向。'


# ================================================================ 14. SAFETY CONSIDERATIONS
@slide
def s_safety(cv, n):
    cv.title('安全考量：闭环的双刃剑')

    # Two sides
    g = cv.group('加速能力')
    g.card(150, 200, 620, 280, fill=lighten(C['green'], 0.85), line=C['green'])
    g.text('✓ 潜在收益', 180, 230, pt=22, bold=True, color=C['green'])
    items_pro = [
        '加速AI研究进程',
        '降低研发成本',
        '探索人类难触及的方向',
        '规模化科研生产力'
    ]
    for i, item in enumerate(items_pro):
        g.text(f'• {item}', 180, 290 + i * 45, pt=18, color=C['text'])

    p = cv.group('失控风险')
    p.card(830, 200, 620, 280, fill=lighten(C['orange'], 0.85), line=C['orange'])
    p.text('✗ 潜在风险', 860, 230, pt=22, bold=True, color=C['orange'])
    items_con = [
        '能力增长超出预期',
        '目标函数被黑客攻击',
        '对齐难度随能力增长',
        '人类退出循环后难介入'
    ]
    for i, item in enumerate(items_con):
        p.text(f'• {item}', 860, 290 + i * 45, pt=18, color=C['text'])

    # Key insight
    cv.card(150, 540, 1300, 120, fill=lighten(C['navy'], 0.9))
    cv.text('关键：评估器对齐 = 自我改进对齐', 180, 570, pt=22, bold=True, color=C['navy'])
    cv.para('如果评估器与人类价值对齐，自我改进可能安全；如果评估器被误指定，改进会放大错误',
            180, 610, 1240, pt=18, color=C['text'])

    cv.band('评估器是安全与失控的分水岭')
    return '讲稿：闭环RSI是双刃剑。收益：加速研究、降低成本。风险：能力超预期增长、对齐难度递增、人类退出后难介入。关键在于评估器对齐——它定义"更好"，如果误指定，改进会放大错误。'


# ================================================================ 15. KEY FINDINGS
@slide
def s_findings_summary(cv, n):
    cv.title('核心发现总结')

    # Three main findings
    findings = [
        ('1. 有界 vs 开放式', 260,
         '有界自精化（输出修正、测试时训练）已是成熟工业实践；'
         '开放式RSI（自主研究、完全闭环）仍受评估器可靠性限制',
         C['blue']),
        ('2. 验证层级定律', 540,
         '自我改进强度与验证强度正相关：形式验证最强，内在自评最弱；'
         '代码/数学优于开放域，根源在验证可靠性',
         lighten(C['blue'], 0.7)),
        ('3. 方向设定堡垒', 820,
         '执行层面自主性已高（Claude写80%代码），但研究方向选择'
         '（"做什么问题"）仍需人类——这是验证层级的最顶层',
         lighten(C['blue'], 0.5))
    ]

    for title, y, text, col in findings:
        cv.card(150, y - 30, 1300, 220, fill=lighten(col, 0.85), line=col)
        cv.text(title, 180, y, pt=22, bold=True, color=col)
        cv.para(text, 180, y + 50, 1240, pt=18, color=C['text'])

    cv.band('1250篇论文证据收敛于：评估器是瓶颈')
    return '讲稿：三大核心发现。第一，有界改进已成熟，开放式RSI仍受限。第二，验证强度决定改进上限，形式化领域成功率高。第三，方向设定（问题选择）是人类最后的堡垒，因其位于验证层级顶端。'


# ================================================================ 16. OUTLOOK
@slide
def s_outlook(cv, n):
    cv.title('研究展望与行动建议')

    # Three priority areas
    g = cv.group('优先方向')
    g.text('技术优先级', 180, 200, pt=20, bold=True, color=C['navy'])
    g.card(150, 240, 680, 180, fill=C['white'], line=C['blue'])
    priorities_tech = [
        '构建更强的评估器（形式验证方向）',
        '研究防坍塌机制（多样性保持）',
        '开发可解释的过程奖励模型'
    ]
    for i, pr in enumerate(priorities_tech):
        g.text(f'{i + 1}. {pr}', 180, 270 + i * 50, pt=18, color=C['text'])

    p = cv.group('治理优先级')
    p.text('治理优先级', 880, 200, pt=20, bold=True, color=C['navy'])
    p.card(850, 240, 610, 180, fill=C['white'], line=C['orange'])
    priorities_gov = [
        '开发RSI能力测量标准',
        '建立闭环系统审计框架',
        '制定评估器对齐指南'
    ]
    for i, pr in enumerate(priorities_gov):
        p.text(f'{i + 1}. {pr}', 880, 270 + i * 50, pt=18, color=C['text'])

    # Balance message
    cv.card(150, 480, 1300, 180, fill=lighten(C['gold'], 0.85), line=C['gold'])
    cv.text('平衡自主性与可控性', 180, 520, pt=24, bold=True, color=C['gold'])
    cv.para('自我改进技术能加速AI研发，但需同步发展治理工具。'
            '评估器设计是技术与安全的交汇点——既是能力瓶颈，也是对齐关键。'
            '\n\n下一步：从"能否自我改进"转向"如何可控地改进"',
            180, 570, 1240, pt=18, color=C['text'])

    cv.band('治理先行，技术跟进')
    return '讲稿：行动建议分技术与治理两线。技术侧：构建强评估器、防坍塌机制、可解释奖励模型。治理侧：RSI测量标准、审计框架、对齐指南。关键是平衡自主性与可控性，评估器是交汇点。'


# ================================================================ MAIN
def main():
    if len(sys.argv) != 2:
        print('Usage: python -I tools/build_deck.py output.pptx')
        sys.exit(1)

    output = sys.argv[1]
    prs = Presentation()
    prs.slide_width = SLIDE_W
    prs.slide_height = SLIDE_H

    with tempfile.TemporaryDirectory() as tmp:
        icon_store = IconStore(prs, tmp)

        for i, slide_fn in enumerate(SLIDES, 1):
            blank_layout = prs.slide_layouts[6]
            sld = prs.slides.add_slide(blank_layout)
            cv = Canvas(sld.shapes, icon_store)
            note_text = slide_fn(cv, i)
            notes(sld, note_text)

        # Add icon library slide (hidden)
        icon_slide = prs.slides.add_slide(prs.slide_layouts[6])
        cv_icons = Canvas(icon_slide.shapes, icon_store)
        cv_icons.title('图标库（隐藏页，供参考）')
        icon_names = list(ICON_LABEL.keys())
        x, y = 100, 180
        for name in icon_names:
            cv_icons.icon_c(name, x + 40, y + 40, 50)
            cv_icons.text(ICON_LABEL[name], x + 40, y + 100, pt=16, align='c', color=C['grey'])
            x += 120
            if x > 1400:
                x = 100
                y += 150

        prs.save(output)
        print(f'✓ Generated: {output}')
        print(f'  {len(SLIDES)} slides + 1 icon library')
        print(f'\n可用 PowerPoint 打开编辑所有元素')


if __name__ == '__main__':
    main()

