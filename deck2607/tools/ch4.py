"""Chapter 4: limits, safety and outlook (paper §7–§9). Every claim is from paper.txt."""
import art
from deckkit import C, measure
from kit import slide, rp, boxtext, head, lead, concl, rpanel, tag, chip, toc


@slide('toc')
def toc4(cv, n):
    toc(cv, 3)
    return '目录：第四章 极限、安全与展望（论文 §7 基础/极限/安全、§8 开放问题、§9 结论）。'


@slide()
def limits(cv, n):
    head(cv, '4.1 理论极限', '无新外部资源，只允许有界精炼')
    lead(cv, 'Schaul 给出闭合系统中可掌握任意能力的**三个条件**，实证文献可读作 (a) 或 (b) 失败的后果；'
             '约束文献从**四个角度**审视起飞问题。')
    conds = [('(a) 反馈', '信息充分且与目标对齐', '失败 → 自我确认环'),
             ('(b) 覆盖', '足够宽', '失败 → 多样性崩溃'),
             ('(c) 容量', '足够大', '')]
    for i, (t, b, f) in enumerate(conds):
        x = 20 + i * 527
        cv.label_box(t, x, 284, 170, 88, pt=18, fill=C['blue'], r=8)
        boxtext(cv, b + ('\n**' + f + '**' if f else ''), x + 178, 284, 328, 88, pt=17, fill=C['pale'], line=C['blue'], r=8, align='l', pad=12, lh=1.15)
    angles = [('layers', '可计算性', '有限的内部自我修改让系统停在当前计算层；"递归自我改进"与"无界自我改进"是**不同主张**'),
              ('scurve', '动力学', 'Jafari 等把"失控增长"形式化为可检验性质，给出物理与信息论限制下**排除有限时间爆发**的条件'),
              ('chip', '经济', 'Whitfill & Wu 用四家前沿实验室面板估计算力与认知劳动的替代弹性：两种设定**结论相反**，是可行性争论的实证关键'),
              ('wave', '信息论', 'Zenil：没有符号模型合成或**不消失的外部信号流**，LLM 式自训练不可能无界自我改进')]
    for i, (ic, t, b) in enumerate(angles):
        x = 20 + i * 395
        rpanel(cv, x, 390, 376, 412, t, icon=ic, pt=22)
        rp(cv, b, x + 20, 458, 320, pt=18, lh=1.35)
    concl(cv, '开放式 RSI 需要**持续的外部落地**（数据、算力、环境），或当前系统缺少的**架构要素**', y=842)
    return ('论文 p.23 §7.1：Schaul [185] boundless Socratic learning 三条件 (a) 反馈足够有信息量且对齐、(b) 经验覆盖足够宽、(c) 容量足够；'
            '实证文献是 (a) 失败（自我确认环）或 (b) 失败（多样性崩溃）的研究。p.23–24 四个约束角度：可计算性 [187]；动力学 Jafari 等 [188]；'
            '经济 Whitfill & Wu [189]（OpenAI、DeepMind、Anthropic、DeepSeek，2014–2024），基线模型为替代、"frontier experiments"模型为互补；'
            '信息论 Zenil [146]。结论：有界自我精炼是无新外部资源时理论允许的；开放式 RSI 需要持续落地或缺失的架构要素。')


@slide()
def safety(cv, n):
    head(cv, '4.2 安全与治理', '现在处于"复合效率"情景')
    lead(cv, 'Anthropic 的文章勾勒了**三种情景**，并提出可信放缓的验证基础设施、仿军控模式的国际协调、对齐的紧迫性。'
             '这批文献对该框架的回答是：几乎所有工作都是**情景 2 的机制**——有界环、人设定目标。')
    cv.svg(art.scenario_path(1500, 70), 40, 284, 1540, 70, name='三情景路径')
    for i, (t, col) in enumerate([('情景 1：趋势停滞', C['navy']), ('情景 2：复合效率 + 人设定方向', C['white']), ('情景 3：完全 RSI', C['white'])]):
        cv.text(t, 40 + 250 + i * 500, 319, pt=20, bold=True, color=col, align='c')
    cv.icon_c('pin', 680, 382, 36, name='当前位置')
    cv.text('当前位置：几乎所有文献', 704, 382, pt=18, bold=True, color=C['rose'])
    cv.text('A-Evolve-Training 最像情景 3', 1290, 382, pt=16, color=C['grey'], align='c')
    cols = [('scope', '起飞信号', '要看的不是基准分数，而是在**不可验证任务**上沿验证层级上移：能可靠评估研究方向的系统会移除让人留在环里的约束'),
            ('lock', '风险机制', '自我确认环正是今天模型中的偏差在自训练下**放大的机制**，已在小规模观察到；"不可解雇安全内核"：智能体运行时内的控制都可被其触及'),
            ('ruler', '治理缺口', '治理提案需要证明训练环**没有越过阈值**的方法，技术文献几乎空白；推理算力转移也可能让基于训练算力阈值的治理失效')]
    for i, (ic, t, b) in enumerate(cols):
        x = 20 + i * 527
        rpanel(cv, x, 414, 506, 388, t, icon=ic, pt=22, color=C['rose'] if i == 2 else C['blue'])
        rp(cv, b, x + 22, 482, 462, pt=18, lh=1.35)
    concl(cv, '治理需要的与文献提供的之间的差距，是论文发现的**最空的研究生态位**', y=842)
    return ('论文 p.25 §7.3：Anthropic [5] 三情景——trend stall、compounding efficiency with human direction-setters、full RSI；提出可信放缓的验证基础设施、'
            '仿军控的国际协调、对齐紧迫性。文献的三点回应：定位现在（几乎全是情景 2 机制，A-Evolve-Training [175] 最像情景 3）；起飞信号是沿验证层级在不可验证任务上上移；'
            '错位复合的担忧是实质性的，自我确认环 [141] 已在小规模观察到。p.24 不可解雇安全内核 [191]；p.25 推理扩展 [192] 可能让训练算力阈值治理失效。'
            '缺少证明训练环未越过阈值的方法——最空的研究生态位。')


@slide()
def open_problems(cv, n):
    head(cv, '4.3 开放问题', '按杠杆排序的五个方向')
    lead(cv, '论文按杠杆大小列出**五个开放问题**。最后一项最突出：基础族只有 **60/1,250** 篇，宣称的风险与投入的研究力量**严重错配**。')
    rows = [('1', '外部落地的"汇率"', '理论说纯闭环会退化；实践中临时混入外部信号', '维持改进所需的最低外部信号率（熵库框架提示问题是良定义的）'),
            ('2', '验证不可验证之物', '元评估、构造上可审计只是起点', '对研究品味、创造质量、方向设定的评估'),
            ('3', '稳定性工程成为学科', '上升后崩溃、多样性崩溃、安全漂移按范式各自重新发现', '统一的自我改进环动力学：何时收敛、振荡或崩溃'),
            ('4', '可信的累积', '技能、记忆、经验图缺少权重训练那样的验证故事', '在形式验证与威胁分析两端之间补上中间地带'),
            ('5', '治理级测量', '可信放缓提案需要的验证基础设施**几乎没有技术文献**', '关于训练环在改进什么、不改进什么的可审计证据')]
    def st(i, j):
        if i == 4:
            return {'color': C['rose'], 'bold': j <= 1, 'bg': C['paleRose']}
        return {'bold': j <= 1, 'color': C['navy'] if j <= 1 else C['text']}
    rows = [[c.replace('**', '') for c in r] for r in rows]
    cv.table(20, 270, [90, 330, 560, 580], ['序号', '开放问题', '现状', '需要什么'], rows, row_h=100, head_h=56, pt=18, head_pt=20,
             head_fills=[C['blue']] * 4, row_fills=['ECF6F6', C['white']] * 2 + [C['paleRose']], styles=st)
    return ('论文 p.27–28 §8 Open problems，"Five, in rough order of leverage"：(1) 外部落地的汇率 [146,145]；(2) 验证不可验证之物，元评估 [122] 与构造上可审计 [150] 只是起点；'
            '(3) 稳定性工程：上升后崩溃 [92]、多样性崩溃 [149]、安全漂移 [83] 按范式重新发现；(4) 可信累积：形式验证 [81] 与威胁分析 [82] 两端；'
            '(5) 治理级测量：可信放缓提案 [5] 需要的验证基础设施几乎没有技术文献；基础族 60/1,250 是最明显的错配。')


@slide()
def conclusion(cv, n):
    head(cv, '4.4 结论', '自我改进有多真，取决于验证有多真')
    lead(cv, '两轴框架化解了"self-X"词汇的混淆：**有界自我精炼**与**开放式递归自我改进**是不同现象，证据基础、理论和风险都不同。')
    cols = [('shield', '有界自我精炼：工程成功', C['blue'],
             '推理时环在有外部信号时可靠改进输出\n训练时环把收益固化，已是工业实践\n智能体跨回合积累技能与经验\n演化发现的产物反哺 AI 开发'),
            ('frame', '开放式 RSI：四面受限', C['rose'],
             '理论上：受落地要求与算力弹性约束\n实证上：受崩溃动力学约束\n实践上：受"做什么、什么算更好"这类判断的**不可验证性**约束'),
            ('scope', '该看的信号：验证层级', C['navy'],
             '起飞问题从猜测变成**测量计划**\n不看基准分数，看系统能否成为开放式研究判断的可靠评估者\n在那之前，人是领域**最后一道验证层**')]
    for i, (ic, t, col, b) in enumerate(cols):
        x = 20 + i * 527
        rpanel(cv, x, 266, 506, 534, t, icon=ic, pt=22, color=col)
        rp(cv, b, x + 22, 322, 462, pt=18, lh=1.45)
    concl(cv, '**人在环中不是情怀的遗留，而是这个领域最后一道验证层**', y=842)
    return ('论文 p.28 §9 Conclusion：两轴框架；有界自我精炼与开放式 RSI 是不同现象。有界：推理时环在外部信号下可靠改进、训练时环固化收益且为工业实践、'
            '智能体积累技能与经验、演化发现产物反哺 AI 开发。开放式 RSI：理论上受落地要求与算力弹性、实证上受崩溃动力学、实践上受关键判断的不可验证性约束。'
            '"self-improvement is only as real as its verification"；起飞问题变成测量计划；"the human role in the loop is not a sentimental holdover; it is the field\'s verification layer of last resort"。')


@slide('blank')
def ending(cv, n):
    cv.text('汇报完毕！', 800, 420, pt=66, bold=True, color=C['white'], align='c', name='结束语')
    cv.text('arXiv:2607.07663v1 · Recursive Self-Improvement in AI', 800, 540, pt=20, color='DDEFEE', align='c')
    return '结束页。'
