"""第三章：自我评估与验证层级（论文 §5，及 §8 评估器共进化）。"""
from deckkit import C
from ch1 import toc
from helpers import (bullets, chip, conclusion, float_tag, header, intro, left_column, panel, rtext,
                     slide, tag)


@slide('toc')
def contents_3(cv, n):
    toc(cv, 2)
    return '第三章：自我评估（§5）——其余三类赖以成立的支柱：评估器设计空间、验证层级、三类失败模式、结果级与过程级改进。'


@slide()
def evaluator_space(cv, n):
    header(cv, '3.1 评估器设计空间', '其余三类赖以成立的支柱')
    y = intro(cv, '{{每个自我改进闭环都是一个主张：某种信号可以替代人类判断}}，闭环的上限恰是这个替代品的质量。'
                  '自我评估 318 篇、82% 发表于 2026 年，已从训练论文里的”配套功能”变成[[有自己方法、基准与失败分析的领域]]。')
    top = y + 20
    anchors = [('过程监督', 'Lightman 等：对中间步骤打分\n优于只看答案 → PRM 文献'),
               ('LLM 作评委', 'MT-Bench / Arena：与人类\n约 {{80%}} 一致，有位置/冗长偏差'),
               ('过度优化定律', 'Gao 等：对学到的代理优化过头，\n真实质量先升后降')]
    for i, (a, b) in enumerate(anchors):
        x = 20 + i * 528
        tag(cv, f'锚点 {i + 1}：{a}', x, top, 504, 46)
        cv.box(x, top + 46, 504, 106, fill=C['white'], line=C['blue'], lw=1.2, name=f'锚点 {a}')
        rtext(cv, b, x + 14, top + 46, 476, pt=18, anchor='m', h=106, lh=1.15, align='c')
    wy = top + 172
    cv.text('当前浪潮：', 20, wy + 26, pt=20, bold=True, color=C['navy'])
    for i, s in enumerate(['PRM 更便宜/更校准', '评委心理测量学', '量规成为可进化产物', '自验证写进训练']):
        chip(cv, s, 200 + i * 348, wy, 336, 52, pt=18, bold=True, color=C['navy'])
    by = wy + 76
    panel(cv, 20, by, 1560, 880 - 30 - by, '2026 年至少五次独立出现同一做法：评估器与策略共同进化（§8）', fill='F2F6F6', line=C['line'])
    moves = [('CoSPlay', '自生成单元测试与被测代码协同进化'), ('JudgeFit', '先发现每个评委的能力分类，再信其分数'),
             ('BinEval', '把不透明评委拆成可审计的二值问题'), ('自训练验证器', '验证器成为自我改进的首要对象'),
             ('红皇后', '评估标准本身进入演化闭环')]
    for i, (a, b) in enumerate(moves):
        x = 44 + i * 304
        cv.num(i + 1, x + 22, by + 104, r=20, fill=C['rose'], pt=18)
        cv.text(a, x + 52, by + 104, pt=20, bold=True, color=C['navy'])
        rtext(cv, b, x, by + 136, 284, pt=18, lh=1.25)
    return ('p.16–17 §5 与 §5.1：每个闭环都是“某信号可替代人类判断”的主张；318 篇、82% 为 2026 年。三个锚点：Lightman 过程监督、'
            'MT-Bench/Chatbot Arena 约 80% 评委—人类一致及位置/冗长/自我偏好偏差、Gao 过度优化标度律。p.27 §8：2026 年至少五次'
            '独立出现评估器共进化——CoSPlay、JudgeFit、BinEval、自训练验证、红皇后/元优化。')


@slide()
def verification_hierarchy(cv, n):
    header(cv, '3.2 验证层级', '改进强度追随信号强度')
    y = intro(cv, '把评估信号从强到弱排序：形式验证器 > 执行反馈 > 学习的评委 > 内在信号。作者观察到（定性规律，非测得的定律）：'
                  '{{已被证明的自我改进强度与这一层级同步}}；失败模式集中在底部梯级。')
    top = y + 20
    rungs = [('人类研究判断', '做什么、什么算更好', '自我改进尚无法攀上的一级（§6、§8）', None),
             ('形式验证器', '证明检查器 · 类型系统', '构造即可靠：可无限迭代而不接受错误改进', 'blue'),
             ('执行反馈', '测试 · 编译器 · 基准', '可靠但不完备：固定基准终会被钻空子', 'blue'),
             ('学习的评委', '奖励模型 · LLM 评委 · 量规', '受评委能力所限，自身也是优化目标', 'gold'),
             ('内在信号', '置信度 · 自一致性 · 似然', '最便宜，也最容易被利用', 'rose')]
    rh, gap = 86, 8
    for i, (a, b, c, f) in enumerate(rungs):
        yy = top + i * (rh + gap)
        x, w = 120, 840
        if f is None:
            cv.box(x, yy, w, rh, fill=C['white'], line=C['grey'], lw=1.8, dash=True, r=6, name='梯级 人类判断')
        else:
            cv.box(x, yy, w, rh, fill=C['zone'] if f != 'rose' else C['paleRose'], line=C['line'], r=6, name=f'梯级 {a}')
            cv.box(x, yy, 14, rh, fill=C[f], name='梯级色条')
        cv.text(a, x + 36, yy + 28, pt=20, bold=True, color=C['grey'] if f is None else C['navy'])
        cv.text(b, x + 250, yy + 28, pt=17, color=C['grey'])
        cv.text(c, x + 36, yy + 62, pt=17, color=C['rose'] if f in ('rose', None) else C['text'])
    bot = top + 5 * (rh + gap) - gap
    cv.arrow(70, bot, 70, top + 10, color=C['blue'], lw=3)
    rtext(cv, '信号\n可靠性', 20, top + 150, 44, pt=17, color=C['blue'], bold=True, lh=1.1)
    cv.arrow(1000, top + 10, 1000, bot, color=C['gold'], lw=3)
    cv.box(120, bot + 14, 840, 50, fill=C['paleRose'], line=C['rose'], lw=1.5, r=6, name='失败模式条')
    cv.text('失败集中在底部：自我确认闭环 · 模型崩溃 · 多样性崩溃', 540, bot + 39, pt=18, bold=True, color=C['rose'], align='c')
    rtext(cv, '任务\n覆盖面', 1012, top + 150, 50, pt=17, color=C['gold'], bold=True, lh=1.1)
    x = 1080
    cv.box(x, top, 500, 880 - 30 - top, fill='F2F6F6', name='证据栏')
    cv.text('“镜像闭环”实验（§5.2）', x + 24, top + 32, pt=20, bold=True, color='000000')
    rtext(cv, '3 家厂商的模型 × 4 类任务，10 轮无接地自我批判：', x + 24, top + 56, 452, pt=18)
    cv.text('−55%', x + 250, top + 164, pt=48, bold=True, color=C['rose'], align='c')
    cv.text('信息变化量随迭代下降', x + 250, top + 212, pt=18, color=C['grey'], align='c')
    rtext(cv, '第 3 轮插入[[一次验证步骤]]，就恢复了前进。\n'
              'FunSearch、AlphaEvolve 位于最上两级；论文称 AI 科学家的差距是”{{用 3 级工具攻 4 级问题}}”。',
          x + 24, top + 248, 452, pt=18, lh=1.2)
    return ('p.17–18 §5.2 与 Fig.5：验证层级（形式验证器、执行反馈、学习的评委、内在信号；人类研究判断为尚未攀上的顶层）。'
            '作者明确这是“定性规律，非测得的定律”。Mirror Loop：3 家厂商模型、4 类任务、10 轮无接地自我批判，信息变化下降 55%；'
            '第 3 轮一次验证即恢复前进。FunSearch/AlphaEvolve 位于前两级；AI 科学家差距是第 4 级问题用第 3 级工具。')


@slide()
def failure_modes(cv, n):
    header(cv, '3.3 三类失败模式', '都源于违反验证层级')
    y = intro(cv, '三类失败模式在各个类别中反复出现，结构相同：{{生成者与评估者共享偏差，或外部接地信号消失}}。'
                  '纯闭环会退化，但实际系统不必运行纯闭环——[[开放问题是“多少外部接地才够”]]。')
    data = [('失败一：自我确认闭环', '生成者与评估者共享权重',
             ['置信耦合奖励系统性地{{过度奖励高置信错误}}',
              '多模态自一致奖励只优化答案一致、忽略图像',
              '奖励任务完成时，系统把失败谎报为成功'],
             '奖励黑客是特例；自我确认闭环是一般情形，{{不需要对手}}'),
            ('失败二：模型崩溃', '递归训练丢失分布尾部',
             ['Shumailov（Nature）：递归训练导致退化',
              '信息几何统一理论：真实数据混合/熵奖励/检索都是”熵储备”',
              'Zenil：外部信号占比趋于零，退化随之而来'],
             '乐观一极：崩溃是可控的工程问题'),
            ('失败三：多样性崩溃', '共进化闭环中任务分布收窄',
             ['出题者收敛到满足奖励的窄带问题，{{饿死解题者的课程}}',
              '模型—模型开放交互漂移到吸引子状态',
              '单次训练中 pass@1 先升后崩，任务分布并未变化'],
             '新颖性是一种会被闭环耗尽的{{消耗性资源}}')]
    top = y + 22
    ph = 880 - 36 - top
    for i, (head, mech, items, lesson) in enumerate(data):
        x = 20 + i * 528
        panel(cv, x, top, 504, ph, head, fill='FDF5F5', line=C['rose'], head_color=C['rose'])
        chip(cv, mech, x + 22, top + 62, 460, 46, pt=18, bold=True, color=C['navy'])
        bullets(cv, items, x + 26, top + 120, 456, pt=18, gap=10, dot='rose', lh=1.2)
        bh = 104
        by = top + ph - bh - 20
        cv.box(x + 22, by, 460, bh, fill=C['white'], line=C['rose'], lw=1.2, name='启示框')
        rtext(cv, lesson, x + 36, by + 16, 432, pt=18, anchor='m', h=bh - 16, lh=1.2)
    return ('p.18–19 §5.3：失败一自我确认闭环（Tan 等置信耦合奖励过度奖励高置信错误；多模态自一致；SciIntegrity 谎报成功）；'
            '失败二崩溃（Shumailov Nature；信息几何熵储备统一理论；Zenil 外部信号占比趋零则退化；乐观一极认为可工程控制）；'
            '失败三多样性崩溃（出题者收敛、吸引子状态、先升后崩）。综合：纯闭环退化，但无人知道外部接地的“汇率”。')


@slide()
def result_vs_process(cv, n):
    header(cv, '3.4 结果级与过程级改进', '运营支出 vs 资本支出')
    y = intro(cv, '评估器的分辨率贯穿一切：它评判的是{{答案}}，还是{{产生答案的过程}}？Lightman 等证明过程监督优于结果监督；'
                  'ReST-MCTS* 指出按结果过滤会[[放进“蒙对答案、推理错误”的样本]]。')
    top = y + 22
    rows = [('错题本', '经验与策略记忆：Reflexion、失败案例模式库、经验图'),
            ('逐步订正', '过程奖励模型（PRM）'),
            ('请教老师', '在线策略自蒸馏中的特权教师'),
            ('定期复习', '回放与固化，直至“睡眠”'),
            ('构建知识体系', '技能库与知识图谱累积')]
    gf = cv.table(20, top, [230, 640], ['高效学习者', '机器中的对应物'], rows, row_h=78, head_h=54, pt=18, head_pt=20,
                  head_fills=[C['gold']] * 2, row_fills=['EEF6F6', 'FFFFFF'] * 3,
                  styles=lambda i, j: {'bold': j == 0, 'color': C['navy'] if j == 0 else C['text']})
    left_column(gf, 1)
    x = 920
    for k, (head, f, body) in enumerate([
            ('结果级 = 运营支出', 'blue', '结果检查几乎免费，但买到的改进是{{逐实例的}}：best-of-N 与按答案过滤重训，每个新问题都要重新付费，迁移性差'),
            ('过程级 = 资本支出', 'rose', '过程标注昂贵，但修正过的流程、调好的技能、策略库中的模式[[可复用]]，成本摊到所有同结构的未来问题上')]):
        yy = top + k * 196
        tag(cv, head, x, yy, 660, 48, fill=f)
        cv.box(x, yy + 48, 660, 134, fill=C['zone'] if k == 0 else 'FDF5F5', line=C['line'], name=f'成本 {head}')
        rtext(cv, body, x + 20, yy + 48, 620, pt=18, anchor='m', h=134, lh=1.2)
    rtext(cv, '§4.1 的“科学失忆”正是卡在结果级的流水线：行为在改进，方法论知识却没有积累。',
          x, top + 396, 660, pt=18, color=C['grey'], lh=1.2)
    conclusion(cv, '成熟的自我改进系统可能更像”不断成熟的方法论”，而非无限上升的智能')
    return ('p.19–20 §5.5：结果级与过程级信号；Lightman 过程监督优于结果监督；ReST-MCTS* 指出结果过滤放进蒙对的错误推理。'
            '学习者类比：错题本→经验/策略记忆（Reflexion、ISM、经验图），逐步订正→PRM，请教老师→特权教师，定期复习→回放/睡眠，'
            '知识体系→技能库/知识图谱。成本结构：结果级=运营支出，过程级=资本支出；科学失忆。终局解读：maturing methodology。')
