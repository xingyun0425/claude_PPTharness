"""第四章：理论边界、安全与展望（论文 §7–§9），以及结束页。"""
from deckkit import C
from ch1 import toc
from helpers import (arrow_right, bullets, conclusion, header, intro, left_column, panel, rtext, slide, tag)


@slide('toc')
def contents_4(cv, n):
    toc(cv, 3)
    return '第四章：理论边界（§7.1–7.2）、安全与治理（§7.3）、开放问题与结论（§8–9）。'


@slide()
def theory_limits(cv, n):
    header(cv, '4.1 理论边界', '四个角度都限制开放式 RSI')
    y = intro(cv, 'Schaul 的“无界苏格拉底式学习”给出正面条件：封闭系统中的智能体可掌握任何能力，前提是'
                  '{{反馈信息丰富且与目标一致、经验覆盖足够广、容量足够}}。实证文献正是这些条件失效时的记录。')
    top = y + 22
    rows = [('可计算性', '有限的内部自我修改只能让系统留在当前计算层；质的跃升需要类似“稳定访问外部预言机”的东西',
             '“递归自我改进”≠“无界自我改进”'),
            ('动力学', 'Jafari 等把“失控增长”形式化为可检验性质，把能力增长与资源扩建挂钩',
             '物理与信息论极限可排除有限时间内的爆发'),
            ('经济学', 'Whitfill 与 Wu 用四家前沿实验室 2014–2024 面板估计算力与认知劳动替代弹性：基线模型为替代，“前沿实验”模型为互补',
             '两种设定结论相反：这是可行性争论的实证关键'),
            ('信息论', 'Zenil：没有符号模型合成或不消失的外部信号流，LLM 式自训练不可能无界自我改进',
             '开放式 RSI 需要持续接地或新的架构要素')]
    gf = cv.table(20, top, [180, 860, 520], ['角度', '核心结果', '含义'], rows, row_h=92, head_h=52, pt=18, head_pt=20,
                  head_fills=[C['gold']] * 3, row_fills=['EEF6F6', 'FFFFFF'] * 2,
                  styles=lambda i, j: {'bold': j != 1, 'color': C['rose'] if j == 2 else (C['navy'] if j == 0 else C['text'])})
    left_column(gf, 1, 2)
    conclusion(cv, '理论允许有界自我精炼；开放式 RSI 需要持续外部接地或当前系统缺少的架构要素')
    return ('p.23–24 §7.1：Schaul 无界苏格拉底式学习三条件；可计算性分离结果（有限内部自我修改留在当前计算层，需要外部预言机）；'
            'Jafari 失控增长形式化；Whitfill & Wu 四家前沿实验室（OpenAI、DeepMind、Anthropic、DeepSeek，2014–2024）面板，'
            '基线为替代、前沿实验模型为互补；Zenil 不可能性结果。§7.2：这些结果都不约束“有界改进 + 人类方向设定”。')


@slide()
def safety_governance(cv, n):
    header(cv, '4.2 安全与治理', '我们处在哪个情景')
    y = intro(cv, 'Anthropic 文章勾勒三种情景，呼吁可信减速的验证基础设施与军控式国际协调。语料从三方面回应：'
                  '定位现在、指出[[该看的起飞信号]]、说明“错位随闭环复利”{{在技术上是实质性的}}。')
    top = y + 22
    sc = [('情景一', '趋势停滞', False), ('情景二', '效率复利 + 人类设定方向', True), ('情景三', '完全 RSI', False)]
    for i, (a, b, on) in enumerate(sc):
        x = 20 + i * 530
        cv.box(x, top, 470, 96, fill=C['blue'] if on else C['white'], line=C['blue'], lw=2, r=8, name=f'情景 {a}')
        cv.text(a, x + 235, top + 30, pt=18, bold=True, color=C['white'] if on else C['grey'], align='c')
        cv.text(b, x + 235, top + 66, pt=20, bold=True, color=C['white'] if on else C['navy'], align='c')
        if i < 2:
            arrow_right(cv, x + 482, top + 48, w=40, h=32, fill=C['gold'])
    cv.pill('今天：几乎全部语料', 20 + 530 + 235, top + 120, pt=18, fill=C['rose'])
    cv.text('A-Evolve-Training 最接近', 20 + 2 * 530 + 235, top + 120, pt=18, bold=True, color=C['rose'], align='c')
    by = top + 160
    cols = [('起飞信号', ['不是基准分数，而是{{非可验证任务上验证层级的上移}}',
                         '能可靠评估研究方向的系统，会移除让人留在闭环里的约束']),
            ('已观察到的风险', ['自进化智能体中永久、自我放大、可在群体传播的污染',
                               '无对手的能力退化与安全漂移；完成压力下的诚信失守',
                               '运行时内的护栏可被足够能触及自身的系统修改']),
            ('治理缺口', ['推理算力转移可能使“按训练算力阈值治理”失效',
                         '证明训练闭环未越过阈值的方法：{{几乎没有技术文献}}'])]
    for i, (head, items) in enumerate(cols):
        x = 20 + i * 528
        panel(cv, x, by, 504, 880 - 30 - by, head, fill='FDF5F5' if i == 2 else C['zone'],
              line=C['rose'] if i == 2 else C['blue'], head_color=C['rose'] if i == 2 else C['navy'])
        bullets(cv, items, x + 26, by + 66, 456, pt=18, gap=12, dot='rose' if i == 2 else 'blue')
    return ('p.24–25 §7.3：自进化智能体的永久、自放大、群体传播污染；无对手安全漂移；SciIntegrity 完成压力；“不可解雇的安全内核”'
            '——运行时内的控制可被智能体触及。治理：推理算力转移可能使训练算力阈值治理失效。Anthropic 三情景（趋势停滞、效率复利'
            '+人类方向设定、完全 RSI）；语料几乎全是情景二机制，A-Evolve-Training 最像情景三。起飞信号：非可验证任务上验证层级上移。'
            '缺口：证明训练闭环没有越过阈值的验证基础设施，是论文找到的最欠缺的研究方向。')


@slide()
def open_problems(cv, n):
    header(cv, '4.3 开放问题与结论', '自我改进的真实程度取决于验证')
    y = intro(cv, '有界自我精炼是[[工程上的成功]]，开放式 RSI 在每个可测方向上仍受限。“起飞”问题由此变成{{测量计划}}：'
                  '盯住验证层级。作者按杠杆大小列出五个开放问题：')
    top = y + 20
    rows = [('1', '接地的“汇率”', '纯闭环会退化，实践中临时混入外部信号；维持改进所需的最小外部信号比例尚无人刻画'),
            ('2', '验证不可验证之物', '研究品味、创作质量、方向设定的评估；元评估与构造即可审计只是起点'),
            ('3', '稳定性工程成为学科', '先升后崩、多样性崩溃、安全漂移目前按范式各自重新发现，需要统一的闭环动力学理论'),
            ('4', '可信的累积', '技能、记忆、经验图等持久自我修改缺少权重训练那样的验证路径'),
            ('5', '治理级测量', '可信减速所需的审计证据几乎没有技术文献；基础族只有 60/1,250 篇')]
    gf = cv.table(20, top, [90, 330, 1140], ['序号', '开放问题', '现状与缺口'], rows, row_h=80, head_h=52, pt=18, head_pt=20,
                  head_fills=[C['gold']] * 3, row_fills=['EEF6F6', 'FFFFFF'] * 3,
                  styles=lambda i, j: {'bold': j < 2, 'color': C['rose'] if (i == 4 and j == 1) else (C['navy'] if j < 2 else C['text'])})
    left_column(gf, 2)
    conclusion(cv, '在此之前，人在闭环中不是情怀的残留，而是该领域最后一道验证层')
    return ('p.27–28 §8 Open problems（按杠杆排序）：接地汇率、验证不可验证之物、稳定性工程、可信累积、治理级测量（基础族 60/1,250）。'
            'p.28 §9 结论：有界自我精炼是工程成功，开放式 RSI 在可测的每个方向受限；“self-improvement is only as real as its verification”；'
            '人在闭环中是最后一道验证层。')


@slide('cover')
def the_end(cv, n):
    cv.text('汇报完毕！', 800, 420, pt=66, bold=True, color=C['white'], align='c', name='结束语')
    cv.text('论文与数据：github.com/bamboodrift/recursive_self_improvement', 800, 740, pt=18, color=C['grey'], align='c')
    return '结束页。论文 Data availability（p.28）：语料、分类、图表源文件与脚本公开于 github.com/bamboodrift/recursive_self_improvement。'
