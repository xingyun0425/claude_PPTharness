"""Chapter 3: the four improvement categories (paper §3–§6). Every number is from paper.txt."""
import math

import art
from deckkit import C, measure
from kit import slide, rp, boxtext, head, lead, concl, rpanel, tag, chip, toc, tabs


@slide('toc')
def toc3(cv, n):
    toc(cv, 2)
    return '目录：第三章 四类自我改进机制（论文 §3 部署时、§4 训练时、§5 自评估、§6 自主科研）。'


@slide()
def deployment(cv, n):
    tabs(cv, '部署时')
    head(cv, '3.1 部署时自进化', '持久性决定风险')
    lead(cv, '最大的一类（**393 篇**），改进发生在部署中、无离线训练阶段；差别在**持久性**：'
             '精炼的输出随回合结束消失，测试时更新持续一个会话，harness 与技能的改动**无限期累积**。')
    cards = [('pen', '输出精炼（§3.1–3.3）', '生成 → 批评 → 修订，权重冻结\n无外部反馈时 LLM 基本无法自我纠正推理\n设计规则：**没有外部信号，就没有可靠改进**'),
             ('bolt', '测试时训练（§3.4）', '部署中按查询更新权重\n补充检索发现该主线增长很快（**87 篇**）\n推理/训练二分正在变成更新时间尺度的连续谱'),
             ('blocks', '技能演化（§3.5–3.6）', '改写提示、工具、记忆、技能库乃至自身代码\n持久且可审计，**也可被攻击**\n共享技能库中被污染的技能会扩散')]
    for i, (ic, t, b) in enumerate(cards):
        x = 20 + i * 527
        rpanel(cv, x, 270, 506, 326, t, icon=ic, pt=22)
        rp(cv, b, x + 22, 338, 466, pt=17, lh=1.25)
    spans = [(130, 370, 10), (620, 900, 16), (1130, 1440, 24)]
    cv.svg(art.persistence_axis2(spans, 1540), 30, 600, 1540, 60, name='持久性时间轴')
    for cx, s in [(273, '一次回答'), (800, '一个会话'), (1323, '无限期累积')]:
        cv.text(s, cx, 676, pt=18, bold=True, color=C['navy'], align='c')
    ev = [('SkillsBench', '人写技能使通过率提升 **16.2 分**；LLM 写的技能**没有可测增益**'),
          ('收益要清醒', '34 种推理扩展配置比 CoT 最多 **+7.1 分**，需约 **20× 算力**；收益多来自工程')]
    for i, (t, b) in enumerate(ev):
        x = 20 + i * 790
        cv.box(x, 706, 770, 100, line=C['blue'], fill=C['white'], r=4, lw=1.5, name=f'证据 {t}')
        rp(cv, b, x + 206, 724, 548, pt=17, lh=1.25)
        tag(cv, t, x + 100, 756, pt=17, w=184)
    concl(cv, '安全文献抓住的核心问题：**未经验证的累积**——同一个验证瓶颈，现在带上了记忆', y=848)
    return ('论文 p.6 §3 引言：最大类 393 篇，按持久性区分；Figure 3（p.7）。p.8–10 §3.1–3.3：Huang 等负结果——无外部反馈 LLM 基本无法自我纠正推理；'
            '设计规则 "no external signal, no reliable improvement"（p.10）。p.10 §3.4：TTT 补充检索 87 篇。p.10–12 §3.5–3.6：Gödel Agent、DGM；'
            'SkillsBench 人写技能 +16.2，LLM 写无可测增益（p.12）；Pareto 分析 34 种配置，比 CoT 峰值 +7.1，约 20× 算力（p.11）；'
            'Assessment（p.12）：accumulation-without-verification 是核心问题。')


@slide()
def training(cv, n):
    tabs(cv, '训练时')
    head(cv, '3.2 训练时自迭代', '一个环，五种范式')
    lead(cv, '**340 篇**把改进内化进权重：模型自己生成训练数据、奖励或教师信号。五种范式的区别主要在**谁提供评估信号**；'
             '两种失效模式都挂在**"评估与筛选"**这一站（Figure 4）。')
    OX, OY, W, H = 20, 284, 960, 560
    cx, cy, rx, ry = 480, 250, 330, 180
    cv.svg(art.ring_gaps(cx, cy, rx, ry, [16, 24, 16, 24], W, H), OX, OY, W, H, name='训练环')
    nodes = [('模型', '当前策略'), ('生成', '答案·轨迹·问题'), ('评估与筛选', '验证器·奖励模型·自我判断'), ('更新权重', 'SFT·RL·蒸馏')]
    for k, (t, s) in enumerate(nodes):
        a = math.radians(-90 + k * 90)
        nx, ny = OX + cx + rx * math.cos(a), OY + cy + ry * math.sin(a)
        w = 290 if k == 2 else 220
        cv.box(nx - w / 2, ny - 44, w, 88, fill=C['white'], line=C['rose'] if k == 2 else C['blue'], lw=2.5, r=10, name=f'节点 {t}')
        cv.box(nx - w / 2, ny - 44, w, 8, fill=C['rose'] if k == 2 else C['blue'], name=f'节点条 {t}')
        cv.text(t, nx, ny - 8, pt=20, bold=True, color=C['navy'], align='c')
        cv.text(s, nx, ny + 24, pt=16, color=C['grey'], align='c')
    # legend sits inside the ring, between the top/bottom nodes and clear of the side nodes
    rp(cv, '**五种范式与信号来源**\n自博弈：模型也生成问题\nCoT 自训练：保留答对轨迹\n自奖励 RL：自己当裁判\n'
           '在线自蒸馏：特权自我当老师\n具身环：环境提供信号', OX + cx - 190, OY + cy - 116, 380, pt=16, lh=1.2, align='c', color=C['text'])
    # the two failure modes hang off the evaluate-and-select node (bottom), as in Figure 4
    ex, ey = OX + cx, OY + cy + ry + 50
    for k, (t, dx) in enumerate([('自我确认环：共享权重，偏差相关', -240), ('上升后崩溃：环不会自稳定', 240)]):
        cv.line(ex + (-100 if dx < 0 else 100), ey - 6, ex + dx * 0.7, ey + 4, color=C['rose'], lw=2, dash=True)
        tw = measure(t, 16, True) + 58
        cv.box(ex + dx - tw / 2, ey + 4, tw, 40, fill=C['paleRose'], line=C['rose'], lw=1.5, r=8, name=f'失效 {t}')
        cv.icon_c('alert', ex + dx - tw / 2 + 24, ey + 24, 26, name='失效图标')
        cv.text(t, ex + dx - tw / 2 + 44, ey + 24, pt=16, bold=True, color=C['rose'])
    cv.card(1000, 262, 580, 540, fill='ECF6F6', line=None, r=6, shadow=False, name='主要启示')
    cv.text('主要启示：', 1022, 296, pt=22, bold=True, color='1A1A1A')
    rp(cv, '1）环的**上限由验证信号决定**：执行与证明最高，内在信号最低\n'
           '2）**崩溃是默认动态**：可验证奖励下 pass@1 也会先升后崩\n'
           '3）环**传递偏差和传递能力一样高效**\n'
           '4）自博弈存活取决于**数据门控与奖励锚定**',
       1022, 332, 536, pt=18, lh=1.35)
    concl(cv, '每条子主线都独立重新发现了：**验证信号定上限，崩溃要靠工程去对抗**', y=842)
    return ('论文 p.13 §4：340 篇；谱系 STaR → ReST^EM → SPIN → Self-Rewarding LMs。Figure 4（p.13）：一个环五种范式，区别在谁提供评估信号，'
            '两种失效挂在 evaluate-and-select 站。p.14 Lin [92]：可验证二元奖励下 pass@1 先升后崩，KL/EWC 约束无法阻止。'
            'p.16 §4.4 [120]：自博弈存活由数据门控与奖励锚定两个杠杆决定。p.16 Assessment：(i) 上限由验证信号决定；(ii) 崩溃是默认动态；(iii) 环传递偏差与能力一样高效。')


@slide()
def hierarchy(cv, n):
    tabs(cv, '自评估')
    head(cv, '3.3 验证层级', '改进强度跟着信号走')
    lead(cv, '自评估是其余三类的**支柱**（**318 篇**，82% 发表于 2026）。每个自我改进环都在主张某个信号能**替代人的判断**，'
             '环的上限恰好就是这个替代品的质量。')
    rows = [('人类科研判断', '做什么、什么算更好：尚未登上的一级'),
            ('形式验证器', '证明检查器、类型系统：构造上可靠'),
            ('执行反馈', '测试、编译器、基准：可靠但不完备，固定基准终会被博弈'),
            ('学习型裁判', '奖励模型、LLM-as-judge、量规：受裁判能力限制'),
            ('内在信号', '置信度、自洽性、似然：最便宜，也最易被博弈')]
    widths = [600, 700, 800, 880, 960]
    PX0, PY0, PW, RH, G = 70, 308, 960, 76, 9
    cv.svg(art.pyramid(widths, PW, RH, G), PX0, PY0, PW, 5 * RH + 4 * G, name='验证层级')
    for i, (t, s) in enumerate(rows):
        x0 = PX0 + (PW - widths[i]) / 2
        y = PY0 + i * (RH + G)
        cv.text(t, x0 + 34, y + 22, pt=20, bold=True, color=C['navy'])
        cv.text(s, x0 + 34, y + 52, pt=16, color=C['grey'])
    cv.svg(art.vline_arrow(5 * RH + 4 * G, up=True), 28, PY0, 26, 5 * RH + 4 * G, name='可靠性箭头')
    cv.text('可靠性 ↑', 66, PY0 - 14, pt=16, bold=True, color=C['blue'], align='c')
    cv.svg(art.vline_arrow(5 * RH + 4 * G, up=False), PX0 + PW + 14, PY0, 26, 5 * RH + 4 * G, name='覆盖面箭头')
    cv.text('覆盖面 ↓', PX0 + PW + 4, PY0 - 14, pt=16, bold=True, color=C['blue'], align='c')
    boxtext(cv, '失效模式集中在底部几级', PX0, PY0 + 5 * RH + 4 * G + 14, PW, 46,
            pt=18, fill=C['paleRose'], line=C['rose'], r=8, pad=12)
    cv.card(1100, 280, 480, 248, fill=C['white'], line=C['blue'], r=10, shadow=True, name='证据 Mirror Loop')
    tag(cv, 'Mirror Loop 实验', 1340, 280, pt=18)
    rp(cv, '三家模型、四类任务、十轮无落地批评：信息变化**下降 55%**；'
           '第三轮插入**一步验证**即恢复前进', 1122, 300, 436, pt=18, lh=1.3)
    cv.card(1100, 554, 480, 248, fill=C['white'], line=C['blue'], r=10, shadow=True, name='证据 定位')
    tag(cv, '强度与层级对应', 1340, 554, pt=18)
    rp(cv, 'FunSearch、AlphaEvolve 位于**最上两级**；'
           'AI 科学家的差距是用第 3 级工具解第 4 级问题', 1122, 594, 436, pt=18, lh=1.35)
    concl(cv, '会改进的环与原地打转的环，差的是**一级外部验证**', y=842)
    return ('论文 p.16 §5 引言：自评估 318 篇、82% 发表于 2026；"Every self-improvement loop is a claim that some signal can substitute for human judgment"。'
            'p.17–18 §5.2 与 Figure 5：形式验证器 → 执行反馈 → 学习型裁判 → 内在信号，顶部为人类科研判断；可靠性向上、覆盖面向下；'
            '失效集中在底部几级。强度随层级是定性观察，不是测量规律。FunSearch/AlphaEvolve 在最上两级；AI 科学家差距是用 level-3 工具做 level-4 问题。'
            'p.18 Mirror Loop [140]：三家模型、四类任务、十轮，信息变化下降 55%，第三轮一步验证即恢复。')
