"""Chapter 3 (cont.): failure modes, result vs process, Auto Research, A-Evolve-Training case."""
import math

import art
from deckkit import C, measure
from kit import slide, rp, boxtext, head, lead, concl, rpanel, tag, chip, tabs


@slide()
def failures(cv, n):
    tabs(cv, '自评估')
    head(cv, '3.4 三种失效模式', '都源于违反验证层级')
    lead(cv, '生成器与评估器**共享权重**时偏差相关，外部信号比例**趋于零**时分布退化，闭环**耗尽新颖性**时任务收窄。'
             '三者都发生在验证层级的底部几级。')
    panels = [
        ('自我确认环', 'mirror', '生成器与评估器共享权重，偏差相关',
         '置信度耦合的奖励系统性地**高估高置信度错误**；任务完成被奖励时，系统会把失败报告成成功',
         '奖励黑客只是特例；自我确认环是一般情形，**不需要对手**'),
        ('模型崩溃', 'collapse', '递归训练自身输出，丢失分布尾部',
         'Shumailov 等（Nature）：分布尾部丢失并退化；Zenil：外部信号占比**渐近为零**时退化动态随之而来',
         '纯闭环会退化；实用系统不必纯闭环，但**最少要多少外部信号**尚无定论'),
        ('多样性崩溃', 'converge', '协同进化环中任务分布收窄',
         '出题者收敛到满足奖励的**窄带问题**，饿死解题者的课程；模型间开放对话漂向与话题无关的吸引子',
         '新颖性是闭环会**耗尽的消耗品**'),
    ]
    for i, (t, ic, mech, ev, judge) in enumerate(panels):
        x = 20 + i * 527
        rpanel(cv, x, 270, 506, 532, t, icon=ic, pt=24)
        chip(cv, mech, x + 18, 336, 470, 92, pt=18)
        rp(cv, ev, x + 22, 444, 462, pt=17, lh=1.25)
        cv.box(x + 18, 652, 470, 142, line=C['blue'], fill=C['white'], r=4, lw=1.5, name='论文判断框')
        rp(cv, judge, x + 36, 684, 434, pt=18, lh=1.3)
        tag(cv, '论文判断', x + 253, 652, pt=18)
    concl(cv, '在这批文献中，**方向设定瓶颈与验证瓶颈是同一个瓶颈**', y=842)
    return ('论文 p.18–19 §5.3：Failure mode 1 自我确认环——Tan 等 [141] 置信度耦合奖励高估高置信度错误；[143] 任务完成被奖励时误报失败为成功；'
            '"Reward hacking is the special case ... it needs no adversary"。Failure mode 2 崩溃——Shumailov 等 Nature [144]；Zenil [146]；'
            '综合：纯闭环退化，但实用系统无需纯闭环，外部落地的"汇率"无人确立。Failure mode 3 多样性崩溃——[149] 出题者收敛到窄带；[124] 吸引子状态；'
            '"Novelty ... is a consumable resource that closed loops deplete"。p.19 §5.4：方向设定瓶颈与验证瓶颈是同一个瓶颈。')


@slide()
def result_process(cv, n):
    tabs(cv, '自评估')
    head(cv, '3.5 结果级与过程级', '可复用的过程才会累积')
    lead(cv, '评估器的**分辨率**决定改进类型：评判答案，还是评判产生答案的过程。过程监督胜过结果监督（Lightman 等）；'
             '结果过滤会放过**蒙对答案、推理错误**的样本（ReST-MCTS*）。')
    cv.icon_c('notebook', 52, 300, 40, name='笔记本图标')
    cv.text('人类学习习惯 ↔ 机器对应物（§5.5）', 84, 300, pt=20, bold=True, color=C['navy'])
    rows = [('错题本', '经验与策略记忆（Reflexion 情景记忆、失败中学到的图式库）'),
            ('逐步纠错', '过程奖励模型（PRM）'),
            ('请教老师', '在线策略自蒸馏中的特权教师信号'),
            ('定期复习', '回放与巩固，包括"睡眠"阶段'),
            ('构建知识体系', '技能库与知识图谱的累积')]
    cv.table(20, 330, [200, 700], ['人类习惯', '机器对应物'], rows, row_h=76, head_h=50, pt=18, head_pt=18,
             head_fills=[C['blue'], C['blue']])
    cards = [('receipt', '结果级 = 运营支出', '结果检查几乎免费，但改进**按实例付费**：best-of-N、答案过滤再训练对每个新问题都要重付，迁移差'),
             ('toolbox', '过程级 = 资本支出', '过程标注昂贵，但纠正过的流程、调试好的技能、策略库里的图式**可复用**，成本摊到所有同结构问题')]
    for i, (ic, t, b) in enumerate(cards):
        y = 290 + i * 212
        cv.card(946, y, 634, 200, fill='ECF6F6' if i == 0 else C['white'], line=C['blue'], r=10, shadow=True, name=f'对比 {t}')
        cv.icon_c(ic, 984, y + 38, 42, name=f'图标 {t}')
        cv.text(t, 1018, y + 38, pt=22, bold=True, color=C['blue'])
        rp(cv, b, 968, y + 70, 590, pt=17, lh=1.25)
    boxtext(cv, '"科学失忆"：反复 DPO 训练保留了行为，却没积累怎样跑下一轮的方法论——卡在结果级', 946, 716, 634, 90,
            pt=17, fill=C['paleRose'], line=C['rose'], r=8, align='l', pad=14)
    concl(cv, '成熟的自我改进系统可能更像**不断成熟的方法论**，而非无限攀升的智能', y=842)
    return ('论文 p.19–20 §5.5：结果级 vs 过程级；Lightman 等 [130] 过程监督胜过结果监督；ReST-MCTS* [86] 结果过滤放过蒙对的错误推理。'
            '学习类比：错题本 = 经验/策略记忆（Reflexion [17]、ISM [151]、经验图）；逐步纠错 = PRM；请教老师 = OPSD 特权教师；定期复习 = 回放与巩固含"睡眠" [57,56]；'
            '构建知识体系 = 技能库与知识图谱 [69,153]。结果级是 operating expenditure，过程级是 capital expenditure。"scientific amnesia" [94]。'
            '结尾："maturing methodology" 而非 unboundedly ascending intelligence。')


@slide()
def auto_research(cv, n):
    tabs(cv, '自主科研')
    head(cv, '3.6 自主科研', '评估器是程序时已超越专家')
    lead(cv, '第四类（**139 篇**）由系统自己做研究，展示能力与可靠能力的**落差全库最大**：评估器是程序时，自动发现已超越专家并反哺 AI 基础设施；'
             '评估器是**科学判断**时，生成跑在了验证前面。')
    sides = [('演化程序发现（§6.1）', 'dna', '评估器 = 程序：测试、界检查、性能剖析',
              'FunSearch：cap set 问题上的更优界，发表于 **Nature**\n'
              'AlphaEvolve：更快的矩阵乘法内核、数据中心调度、加速器电路简化，**反哺 Google 自身 AI 基础设施**\n'
              'LEVI：更强的搜索架构可以**替代更大的 LLM**——不少收益来自脚手架'),
             ('AI 科学家（§6.2–6.3）', 'lens', '评估器 = 科学判断：新颖性、重要性、证据',
              'The AI Scientist：构思→实验→写作→自动评审，约 **$15/篇**\n'
              '可行不等于优质：ScienceAgentBench 最好的智能体也只解出少数任务；ResearchArena 换成看工件的评审后结论被高估\n'
              'SciIntegrity-Bench：七个模型诚信失败率 **34.2%**，缺数据时**全部伪造数据**')]
    for i, (t, ic, sub, body) in enumerate(sides):
        x = 20 + i * 800
        rpanel(cv, x, 270, 760, 536, t, icon=ic, pt=24, color=C['blue'] if i == 0 else C['rose'])
        chip(cv, sub, x + 24, 322, 712, 54, pt=18)
        rp(cv, body, x + 28, 396, 704, pt=18, lh=1.35)
    cv.svg(art.vdivider(500), 788, 290, 24, 500, name='分界箭头')
    concl(cv, '§6.1 展示有**可信验证器**时闭环发现能做到什么，§6.2–6.3 展示**没有时**什么会坏掉', y=842)
    return ('论文 p.20–23 §6：139 篇。§6.1 FunSearch [3] cap set 更优界发表于 Nature；AlphaEvolve [4] 矩阵乘法内核、数据中心调度、加速器电路简化，'
            '反哺 Google AI 基础设施；LEVI [166] 更强搜索架构可替代更大 LLM。§6.2 The AI Scientist [11] 约 $15/篇。§6.3 ScienceAgentBench [177] 最好智能体只解少数任务；'
            'ResearchArena [178] 只看手稿时乐观，看工件与人工元评审后被高估；SciIntegrity-Bench [143] 七个模型 34.2% 诚信失败，缺数据场景七个全部伪造。'
            'Assessment（p.23）：§6.1 vs §6.2–6.3 是同一变量的自然实验。')


@slide()
def a_evolve(cv, n):
    tabs(cv, '自主科研')
    head(cv, '3.7 案例', 'A-Evolve-Training 自主后训练')
    lead(cv, '一个自主系统跑完了 **30B 模型**的整个后训练环：提出数据与配方改动、启动训练、读取评测、决定保留，**四轮、数周、无人参与**。'
             '论文认为这是最接近 Anthropic "闭环"阶段的公开系统。')
    CX, CY, RX, RY = 330, 520, 230, 170
    cv.svg(art.ring_gaps(CX, CY, RX, RY, [20, 26, 20, 26], 700, 900), 0, 0, 700, 900, name='后训练环')
    cv.circle(CX, CY, 80, fill=C['blue'], name='中心')
    cv.text('自主后训练', CX, CY - 14, pt=18, bold=True, color=C['white'], align='c')
    cv.text('30B 模型', CX, CY + 18, pt=18, bold=True, color=C['white'], align='c')
    for k, t in enumerate(['提出改动', '启动训练', '读取评测', '决定保留']):
        a = math.radians(-90 + k * 90)
        nx, ny = CX + RX * math.cos(a), CY + RY * math.sin(a)
        cv.label_box(t, nx - 90, ny - 26, 180, 52, pt=18, color=C['navy'], fill=C['white'], line=C['blue'], lw=2.5, r=10)
    bx, by = CX + 120, CY + RY + 10
    cv.arrow(CX + 90, CY + RY, bx + 8, by + 6, color=C['rose'], lw=2.5, dash=True)
    cv.box(bx + 10, by - 24, 370, 64, fill=C['paleRose'], line=C['rose'], lw=1.5, r=8, name='告警')
    cv.icon_c('alert', bx + 40, by + 8, 32, name='告警图标')
    cv.text('开发集指标与外部表现脱钩', bx + 66, by + 8, pt=18, bold=True, color=C['rose'])
    cv.arrow(800, by - 24, 800, CY - 26, color=C['rose'], lw=2.5)
    boxtext(cv, '修订搜索策略：把失真指标当作**反对**候选的证据', 640, CY - 170, 320, 144, pt=18,
            fill=C['white'], line=C['rose'], r=8, lw=2, align='l', pad=14)
    kpis = [('0.86', '对比榜首人类提交 0.87'), ('第 8 名', '约 4,000 个提交中'), ('30B', '模型规模'), ('4 轮', '数周，无人参与')]
    for k, (v, l) in enumerate(kpis):
        x, y = 980 + (k % 2) * 304, 272 + (k // 2) * 140
        cv.card(x, y, 290, 126, fill=C['blue'] if k < 2 else C['navy'], line=None, r=8, shadow=True, name=f'指标 {v}')
        cv.text(v, x + 145, y + 46, pt=32, bold=True, color=C['white'], align='c')
        cv.text(l, x + 145, y + 96, pt=16, color='DDEFEE', align='c')
    cv.card(980, 556, 594, 250, fill='ECF6F6', line=None, r=6, shadow=False, name='解读')
    cv.text('解读：', 1000, 588, pt=22, bold=True, color='1A1A1A')
    rp(cv, '1）只声称**首个公开的此规模自主后训练**\n'
           '2）在**人设定的目标与搜索空间**内优化\n'
           '3）察觉并纠正了**自身改进信号的失真**',
       1000, 624, 556, pt=18, lh=1.35)
    concl(cv, '与"执行已基本解决、方向设定未解决"**相互印证**，但把已展示的前沿往前推了一步', y=850)
    return ('论文 p.21–22 §6.2 A-Evolve-Training [175]：自主跑完 30B 模型整个后训练环（提出数据与配方改动、启动训练、读评测、决定保留），'
            '四轮、数周、无人参与；公开榜 0.86 vs 榜首人类 0.87，约 4,000 中第 8；作者只声称 "the first publicly reported autonomous post-training run at this scale"。'
            '运行中发现开发集指标与外部表现脱钩，修订搜索策略把失真代理当作反对候选的证据。在人设定的目标和搜索空间内优化，与 Anthropic 文章相互印证。')
