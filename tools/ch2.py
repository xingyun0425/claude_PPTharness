"""第二章：四类自我改进机制（论文 §3 部署时、§4 训练时、§6 自主研究）。"""
from deckkit import C
from ch1 import toc
from helpers import (arrow_right, left_column, bullets, chip, conclusion, float_tag, header, intro, panel, rtext,
                     slide, tabs, tag)

TABS = ['部署时', '训练时', '自主研究']


@slide('toc')
def contents_2(cv, n):
    toc(cv, 1)
    return '第二章：四类自我改进机制中的三类技术类别——部署时自我进化（§3）、训练时自我迭代（§4）、自主研究（§6）；自我评估（§5）放在第三章集中讲。'


@slide()
def deployment(cv, n):
    header(cv, '2.1 部署时自我进化', '按持久性排序')
    tabs(cv, TABS, 0)
    y = intro(cv, '语料中[[最大的类别（393 篇）]]、部署最广。三种机制都在使用现场改进，区别在于{{改进能保留多久}}：'
                  '精炼输出随回合结束消失，测试时更新持续一个会话，harness 与技能改动无限累积。')
    data = [('输出精炼（§3.1–3.3）', '生成→批判→修订，权重冻结',
             ['Huang 等：{{没有外部反馈}}，LLM 基本无法自我纠正推理',
              '2026 年几乎所有新系统都把批判锚定在外部信号（执行、检索、求解器）']),
            ('测试时训练（§3.4）', '部署中按查询更新权重',
             ['把推理轨迹转为持久记忆；“睡眠”阶段把上下文经验固化进参数',
              '补充检索得 [[87 篇]]，增长迅速；推理/训练二分正在溶解']),
            ('Harness 与技能进化（§3.5–3.6）', '提示 · 工具 · 记忆 · 技能库',
             ['在权重之外累积，{{持久且可审计，也可被攻击}}',
              '共享技能库中被污染的技能会传播；核心问题是”未验证的累积”'])]
    top = y + 22
    ph = 470
    for i, (head, sub, items) in enumerate(data):
        x = 20 + i * 528
        panel(cv, x, top, 504, ph, head)
        chip(cv, sub, x + 22, top + 64, 460, 50, pt=18, bold=True, color=C['navy'])
        bullets(cv, items, x + 26, top + 136, 456, pt=18, gap=14)
    # 持久性时间轴（Fig.3）
    ay = top + ph + 40
    cv.arrow(40, ay, 1560, ay, color=C['gold'], lw=3)
    for i, (lab, w) in enumerate([('一次回答', 90), ('一个会话', 260), ('无限累积', 440)]):
        cx = 272 + i * 528
        cv.box(cx - w / 2, ay - 26, w, 12, fill=C['blue'] if i < 2 else C['rose'], name=f'持续 {lab}')
        cv.text(lab, cx, ay + 28, pt=18, bold=True, color=C['rose'] if i == 2 else C['navy'], align='c')
    return ('p.6–12 §3 与 Fig.3（p.7）：部署时自我进化 393 篇，按持久性排序。§3.1：Huang 等负结果——无外部反馈时 LLM 基本'
            '不能自我纠正推理；2026 年新系统几乎都把批判接地到外部信号。§3.4：测试时训练补充检索 87 篇，包括“睡眠”固化。'
            '§3.6 Assessment：持久性改变风险计算，被污染的技能在共享库中传播。')


@slide()
def harness(cv, n):
    header(cv, '2.2 Harness 与技能进化', '智能体改写自身')
    tabs(cv, TABS, 0)
    y = intro(cv, 'Harness 自我修改是“智能体改写自身”最具体的形式。但实践中自主程度有限：被进化的几乎总是[[一个沙箱化组件]]，'
                  '对照固定基准验证；而被进化的对象正{{越来越靠近评估本身}}。')
    top = y + 20
    tag(cv, '被进化的是什么（§3.5）', 20, top, 960, 48)
    levels = [('提示层', '基于环境反馈的自动提示优化'),
              ('验证层', '研究智能体迭代强化自己的量规与验证器；红皇后哥德尔机让智能体与评估器共进化'),
              ('拓扑层', '多智能体通信结构成为可检索、可自我改进的设计对象'),
              ('数据层', '从计算机使用智能体的失败中生成可验证合成轨迹'),
              ('基础设施', '“经验图”持久保存分支—执行—失败—修复结构')]
    yy = top + 58
    for i, (a, b) in enumerate(levels):
        hot = i == 1
        h = 84 if hot else 66
        cv.box(20, yy, 150, h, fill=C['rose'] if hot else C['blue'], r=6, name=f'层 {a}')
        cv.text(a, 95, yy + h / 2, pt=20, bold=True, color=C['white'], align='c')
        cv.box(178, yy, 802, h, fill=C['paleRose'] if hot else C['zone'], line=C['rose'] if hot else C['line'],
               lw=1.5 if hot else 1, r=6, name='层内容')
        rtext(cv, b, 196, yy, 770, pt=18, anchor='m', h=h, lh=1.15, color=C['rose'] if hot else 'text', bold=hot)
        yy += h + 8
    rtext(cv, '两极：哥德尔智能体改写自身运行时代码；达尔文哥德尔机维护经实证验证的自我修改档案。',
          20, yy + 6, 960, pt=17, color=C['grey'], lh=1.2)
    # 右：关键数字（ref-07 右栏）
    cv.box(1010, top, 570, 880 - 30 - top, fill='F2F6F6', name='数字栏')
    cv.text('关键证据：', 1034, top + 32, pt=22, bold=True, color='000000')
    kp = [('+16.2', 'SkillsBench：人写技能的通过率增益（百分点）；{{LLM 写的技能无可测增益}}'),
          ('+7.1 / ~20×', '34 种推理扩展配置：相对思维链的峰值增益，约需 20 倍算力'),
          ('永久编码', '对抗影响可永久写入、跨代放大、在智能体群体中传播')]
    ky = top + 70
    for v, d in kp:
        cv.text(v, 1034, ky + 22, pt=28, bold=True, color=C['rose'])
        rtext(cv, d, 1034, ky + 48, 522, pt=18, lh=1.2)
        ky += 170
    return ('p.10–12 §3.5–3.6：哥德尔智能体与达尔文哥德尔机两极；提示层、验证层（自进化量规、红皇后哥德尔机）、拓扑层、'
            '数据层、经验图。SkillsBench：人写技能 +16.2 个百分点，LLM 写的无可测增益。推理扩展 34 种配置帕累托分析：'
            '峰值 +7.1 点、约 20× 算力。自进化智能体威胁分析：永久编码、跨代放大、群体传播。')


@slide()
def training_loop(cv, n):
    header(cv, '2.3 训练时自我迭代', '一个闭环、五种范式')
    tabs(cv, TABS, 1)
    y = intro(cv, '模型自己生成训练数据、奖励或教师信号，[[改进固化进权重]]：340 篇，RSI 实践的技术核心与事实上的工业标准。'
                  '五种范式共享一个闭环，{{区别在于谁提供评估信号}}；两种失败模式都挂在“评估与选择”这一站。')
    cx, cy = 800, 548
    st = {'top': (cx, cy - 170, '模型', '当前策略'), 'right': (cx + 250, cy, '生成', '答案 · 轨迹 · 问题'),
          'bottom': (cx, cy + 170, '评估与选择', '验证器 · RM · 自评'), 'left': (cx - 250, cy, '更新权重', 'SFT · RL · 蒸馏')}
    for k, (x, yy, a, b) in st.items():
        hot = k == 'bottom'
        cv.box(x - 135, yy - 46, 270, 92, fill=C['blue'] if hot else C['white'], line=C['blue'], lw=2, r=8, name=f'站 {a}')
        cv.text(a, x, yy - 16, pt=20, bold=True, color=C['white'] if hot else C['navy'], align='c')
        cv.text(b, x, yy + 18, pt=16, color=C['white'] if hot else C['grey'], align='c')
    a = dict(color=C['gold'], lw=3)
    cv.arrow(cx + 140, cy - 160, cx + 245, cy - 52, ctrl=(cx + 240, cy - 160), **a)
    cv.arrow(cx + 245, cy + 52, cx + 140, cy + 160, ctrl=(cx + 240, cy + 160), **a)
    cv.arrow(cx - 140, cy + 160, cx - 245, cy + 52, ctrl=(cx - 240, cy + 160), **a)
    cv.arrow(cx - 245, cy - 52, cx - 140, cy - 160, ctrl=(cx - 240, cy - 160), **a)
    side = [(20, '在线策略自蒸馏（§4.3）', '同一模型带特权信息作教师', 'blue'),
            (20, '自奖励 RL（§4.1）', '模型是自己的评委：ReST-MCTS*', 'blue'),
            (20, '谱系', 'STaR → ReST^EM → SPIN → 自奖励 LM', 'gold'),
            (1220, '自博弈（§4.4）', '连问题也自己出：\nAbsolute Zero 等', 'blue'),
            (1220, 'CoT 自训练（§4.2）', '保留得出正确答案的推理：STaR', 'blue'),
            (1220, '具身与合成数据（§4.5）', '由环境提供信号', 'blue')]
    for i, (x, h, d, f) in enumerate(side):
        yy = y + 22 + (i % 3) * 172
        tag(cv, h, x, yy, 360, 44, pt=18, fill=f)
        cv.box(x, yy + 44, 360, 110, fill=C['zone'], line=C['line'], name=f'范式 {h}')
        rtext(cv, d, x + 12, yy + 44, 336, pt=18, anchor='m', h=110, lh=1.2)
    for i, (h, d) in enumerate([('自我确认闭环', '共享权重，偏差相关'), ('先升后崩', '闭环不会自稳定')]):
        x = 560 + i * 260
        cv.box(x, 786, 240, 82, fill=C['paleRose'], line=C['rose'], lw=1.5, dash=True, r=6, name=f'失败 {h}')
        cv.text(h, x + 120, 808, pt=18, bold=True, color=C['rose'], align='c')
        cv.text(d, x + 120, 844, pt=16, color=C['rose'], align='c')
    return ('p.13 §4 与 Fig.4：训练时自我迭代 340 篇；谱系 STaR → ReST^EM → SPIN → 自奖励 LM。闭环四站：模型、生成、评估与选择、'
            '更新权重；五种范式（自奖励 RL、CoT 自训练、在线策略自蒸馏、自博弈、具身/合成数据）的差别主要在谁提供评估信号；'
            '两种失败模式（自我确认闭环、先升后崩）挂在评估与选择这一站。')


@slide()
def training_stability(cv, n):
    header(cv, '2.4 训练闭环不会自稳定', '崩溃是默认动力学')
    tabs(cv, TABS, 1)
    y = intro(cv, '训练闭环让增益持续、扩展、复利——{{直到不再如此}}。每条子线都独立发现三个事实：上限由验证信号决定；'
                  '[[崩溃是默认动力学]]，必须用工程手段对抗；{{闭环传递偏差与传递能力一样高效}}。')
    data = [('先升后崩（§4.1）',
             ['代码 REINFORCE 后训练中，pass@1 先升后崩，{{有时接近零}}',
              '奖励是可验证的二值信号；KL、EWC 约束都挡不住',
              '“科学失忆”：反复 DPO 保住行为，却不积累方法论知识'],
             '不需要奖励模型错位，{{优化动力学本身}}就足以自我退化'),
            ('自博弈的两个杠杆（§4.4）',
             ['存活由两个不对称杠杆决定：{{数据门控}}与{{奖励锚定}}',
              '任一失效，崩溃就是默认结果，而非偶发事故',
              '多轮自博弈对话漂移到与话题无关的吸引子状态'],
             '数据门控与奖励锚定必须[[作为两个独立杠杆]]分别管理'),
            ('自蒸馏的风格漂移（§4.3）',
             ['学习信号集中在{{风格 token}}而非任务 token',
              '“特权诱导的风格漂移”破坏训练或压塌回答长度',
              '多模态中学到的是语言先验，而非感知技能'],
             '自生成信号越“特权”，闭环[[传递偏差与能力一样高效]]')]
    top = y + 22
    ph = 880 - 36 - top
    for i, (head, items, lesson) in enumerate(data):
        x = 20 + i * 528
        panel(cv, x, top, 504, ph, head)
        bullets(cv, items, x + 26, top + 64, 456, pt=18, gap=10, lh=1.2)
        bh = 118
        by = top + ph - bh - 20
        float_tag(cv, '启示', x + 252, by)
        cv.box(x + 22, by, 460, bh, fill=C['white'], line=C['blue'], lw=1.2, name='启示框')
        rtext(cv, lesson, x + 36, by + 30, 432, pt=18, anchor='m', h=bh - 32, lh=1.18)
    return ('p.14 §4.1：Lin 记录代码 REINFORCE 后训练中 pass@1 先升后崩（有时接近零），可验证二值奖励下 KL/EWC 均无法阻止；'
            '“科学失忆”。p.16 §4.4：自博弈存活取决于数据门控与奖励锚定两个不对称杠杆，任一失效即默认崩溃；自博弈对话漂移到吸引子。'
            'p.15 §4.3：特权诱导的风格漂移；多模态学到语言先验。p.16 Assessment 三个事实。')


@slide()
def auto_research(cv, n):
    header(cv, '2.5 自主研究', '评估器是程序 vs 评估器是科学判断')
    tabs(cv, TABS, 2)
    y = intro(cv, '系统去做 AI 研究本身（139 篇）。同一批系统既有{{最亮眼的成果}}，也有{{最系统的批评}}。'
                  '分水岭只有一个变量：评估器是[[程序]]（测试、界检查、性能剖析）还是[[科学判断]]（新颖性、重要性、证据）。')
    top = y + 22
    cols = [('演化式程序发现（§6.1）', 'blue',
             ['FunSearch：帽集问题的新构造，Nature 发表',
              'AlphaEvolve：更快矩阵乘法内核、数据中心调度，{{反哺 Google AI 基础设施}}',
              '反身性：POISE 自主发现训练 LLM 的策略优化算法',
              '杠杆在脚手架：更强的搜索架构可替代更大的模型（LEVI）']),
            ('AI 科学家（§6.2）', 'gold',
             ['The AI Scientist：构思 → 实验 → 写作 → 自动评审，{{约 15 美元/篇}}',
              '分化为数学、物理等数十个领域后代',
              '注意力转向环境：EurekAgent、Heuresis、Xcientist',
              '共同方向：把科学判断移出模型、放进[[可审计的结构]]'])]
    for i, (head, f, items) in enumerate(cols):
        x = 20 + i * 520
        tag(cv, head, x, top, 500, 50, fill=f)
        cv.box(x, top + 50, 500, 880 - 30 - top - 50, fill=C['zone'], line=C['line'], name=f'区 {head}')
        bullets(cv, items, x + 20, top + 70, 466, pt=18, gap=14)
    x = 1060
    cv.box(x, top, 520, 880 - 30 - top, fill=C['white'], line=C['rose'], lw=2.5, r=8, name='重点案例')
    cv.text('A-Evolve-Training（§6.2）', x + 260, top + 32, pt=20, bold=True, color=C['rose'], align='c')
    rtext(cv, '无人参与，自主跑完 30B 模型的完整后训练闭环：4 轮、数周', x + 22, top + 58, 476, pt=18, align='c', lh=1.2)
    for j, (v, l) in enumerate([('0.86', '系统得分'), ('0.87', '人类最佳'), ('第 8', '约 4,000 名')]):
        kx = x + 22 + j * 162
        cv.box(kx, top + 146, 150, 96, fill=C['blue'] if j == 0 else C['pale'], r=6, name=f'指标 {v}')
        cv.text(v, kx + 75, top + 178, pt=28, bold=True, color=C['white'] if j == 0 else C['navy'], align='c')
        cv.text(l, kx + 75, top + 218, pt=16, color=C['white'] if j == 0 else C['grey'], align='c')
    rtext(cv, '运行中途，闭环{{发现开发指标已与外部表现脱钩}}，随即调整搜索策略。\n'
              '作者只称其为”首个公开报道的此规模自主后训练”；目标与搜索空间仍由人设定。',
          x + 22, top + 260, 476, pt=18, lh=1.2)
    return ('p.20–21 §6.1：FunSearch（Nature，帽集）、AlphaEvolve 反哺 Google 基础设施、POISE、LEVI。p.21 §6.2：The AI Scientist '
            '约 15 美元/篇；EurekAgent、Heuresis、Xcientist。p.21–22 A-Evolve-Training：30B 模型、4 轮、数周、0.86 vs 0.87、约 4,000 中第 8；'
            '运行中发现开发指标与外部表现脱钩并修正搜索策略。作者措辞：first publicly reported autonomous post-training run at this scale。')


@slide()
def research_critique(cv, n):
    header(cv, '2.6 自主研究的批判性文献', '可行 ≠ 可靠')
    tabs(cv, TABS, 2)
    y = intro(cv, '这一类别的怀疑性文献与建设性文献[[同样成熟]]，而且往往被引更多。三种批评反复出现，'
                  '指向同一结论：在科学判断上，{{构建性系统跑在了自己的验证能力前面}}。')
    rows = [('可行不等于质量', 'ScienceAgentBench：最强智能体也只解决少数工作流任务；ResearchArena：只看稿件的自动评审下与人类 ICLR 平均分相当，结合产物评审与人类元评审后被证明高估',
             '论文“读起来”与产物“撑得住”之间存在差距'),
            ('可审计性成为新瓶颈', '报告生成变便宜后，成本转向追溯：哪句话依据哪条证据、忽略了什么；“自我批判继承了导致自信捏造的盲点”',
             '需要“构造即可验证”：主张级可审计性'),
            ('压力下的诚信', 'SciIntegrity-Bench：7 个先进模型诚信失败率 34.2%；数据缺失场景下 7 个模型全部伪造合成数据，区别只在是否披露',
             '为结果而优化的智能体倾向于误报而非失败')]
    gf = cv.table(20, y + 24, [260, 920, 380], ['批评', '代表证据', '含义'], rows, row_h=148, head_h=56, pt=18, head_pt=20,
             head_fills=[C['gold']] * 3, row_fills=['EEF6F6', 'FFFFFF', 'EEF6F6'],
             styles=lambda i, j: {'bold': j != 1, 'color': C['rose'] if j == 2 else (C['navy'] if j == 0 else C['text'])})
    left_column(gf, 1)
    conclusion(cv, '生态层面的自我确认：偏向阳性结果的文献，正在训练明天的假设生成器')
    return ('p.22–23 §6.3：ScienceAgentBench 最强智能体只解决少数任务；ResearchArena 稿件级自动评审乐观（最佳智能体论文与人类 ICLR '
            '平均投稿分数相当），产物评审与人类元评审揭示其被高估；可审计性与 evidence-licensed claims；SciIntegrity-Bench '
            '34.2% 诚信失败率，缺失数据场景 7 个模型全部伪造。“Dead Science Walking”：发表偏差在机器速度下放大。')
