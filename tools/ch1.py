"""封面、目录、第一章：研究背景与分类框架（论文 §1–§2）。"""
from deckkit import C, measure
from helpers import (alpha_fill, arrow_right, chip, conclusion, float_tag, header, intro, panel,
                     rtext, slide, tag)

CHAPTERS = ['研究背景与分类框架', '四类自我改进机制', '自我评估与验证层级', '理论边界、安全与展望']


@slide('cover')
def cover(cv, n):
    # 空白版式自带青绿横带（y 206–652）与左上 logo
    cv.text('人工智能递归自我改进', 800, 350, pt=56, bold=True, color=C['white'], align='c', name='主标题1')
    cv.text('从有界自我精炼到自主研究闭环', 800, 465, pt=56, bold=True, color=C['white'], align='c', name='主标题2')
    cv.text('Recursive Self-Improvement in AI · arXiv:2607.07663 论文研读汇报', 800, 568, pt=20,
            color='D5ECEB', align='c', name='英文题名')
    cv.text('Mingguang Chen · Licheng Wang · Bo Qu', 800, 730, pt=20, bold=True, color='000000', align='c')
    cv.text('UCR · AlphaAvatar · IIT    2026年7月', 800, 782, pt=20, bold=True, color='000000', align='c')
    return ('封面。论文：Recursive Self-Improvement in AI: From Bounded Self-Refinement to Autonomous '
            'Research Loops，Chen/Wang/Qu，arXiv:2607.07663v1，2026 年 7 月（p.1）。')


def toc(cv, active):
    """目录页（ref-02/17/26/33）：灰块 + 青绿竖条 + 四行编号条，当前章高亮。"""
    sp = cv.box(114, 152, 227, 518, fill='E6E6E6', name='目录灰块')
    alpha_fill(sp, 70)
    cv.box(83, 475, 69, 273, fill=C['blue'], name='目录竖条')
    cv.text('目    录', 340, 350, pt=40, bold=True, color=C['blue'], align='c', name='目录')
    cv.text('CONTENTS', 340, 428, pt=28, bold=True, color=C['blue'], align='c')
    for i, name in enumerate(CHAPTERS):
        y = 210 + i * 127
        on = i == active
        fill, color = (C['blue'], C['white']) if on else ('E6E6E6', '595959')
        cv.label_box('一二三四'[i], 516, y, 101, 101, pt=28, color=color, fill=fill, name=f'章号 {i + 1}')
        cv.label_box(name, 664, y, 802, 101, pt=28, color=color, fill=fill, name=f'章名 {i + 1}')


@slide('toc')
def contents(cv, n):
    toc(cv, 0)
    return '目录：一 研究背景与分类框架（§1–2）；二 四类机制（§3、§4、§6）；三 自我评估（§5）；四 理论、安全与展望（§7–9）。'


@slide()
def background(cv, n):
    header(cv, '1.1 研究背景', 'AI 开始参与改进自身')
    y = intro(cv, 'AI 系统正越来越多地参与自身改进：{{修订输出、进化 harness、用自生成数据训练}}，乃至{{从事 AI 研究本身}}。'
                  '“智能爆炸”与哥德尔机曾是理论终点，如今闭环的片段已成为[[工程实践]]。')
    # 左：五阶段阶梯（Anthropic 自主性连续谱，p.2）
    tag(cv, 'Anthropic 自主性连续谱（五阶段）', 20, y + 20, 900, 50)
    steps = ['人类编写\n全部代码', '聊天机器人\n辅助编程', '自主编程\n智能体', '智能体向\n智能体委派', '闭环：设计\n训练后继模型']
    base = y + 380
    for i, s in enumerate(steps):
        x, w = 20 + i * 182, 170
        h = 130 + i * 34
        top = base - h
        on, last = i == 3, i == 4
        cv.box(x, top, w, h, fill=C['blue'] if on else (C['white'] if last else C['pale']),
               line=C['rose'] if last else C['blue'], lw=1.8, dash=last, r=8, name=f'阶段 {i + 1}')
        cv.text(str(i + 1), x + 20, top + 24, pt=20, bold=True, color=C['white'] if on else (C['rose'] if last else C['blue']))
        rtext(cv, s, x + 4, top + 46, w - 8, pt=17, bold=True, align='c',
              color=C['white'] if on else (C['rose'] if last else C['navy']), lh=1.15)
    cv.pill('今天', 20 + 3 * 182 + 85, base - 232 - 26, pt=18, fill=C['rose'])
    cv.text('2023 年前', 20 + 85, base - 130 - 22, pt=16, color=C['grey'], align='c')
    cv.line(20 + 2 * 182, base + 14, 20 + 4 * 182 - 12, base + 14, color=C['blue'], lw=3)
    cv.text('技术文献主体：阶段 3–4', 20 + 2 * 182 + 170, base + 38, pt=16, color=C['blue'], bold=True, align='c')
    cv.text('§6 试探阶段 5', 20 + 4 * 182 + 85, base + 38, pt=16, color=C['rose'], bold=True, align='c')
    cv.box(20, base + 70, 900, 120, fill=C['zone'], line=C['line'], r=8, name='执行侧事实')
    rtext(cv, '执行侧：截至 2026 年 5 月，Claude 据报道编写了 Anthropic {{80% 以上}}的合并代码；'
              '瓶颈在[[研究方向设定]]。', 40, base + 74, 860, pt=18, anchor='m', h=112)
    # 右：主要启示（ref-07 右栏）
    cv.box(950, y + 20, 630, base + 178 - y - 20, fill='F2F6F6', name='启示栏')
    cv.text('主要启示：', 976, y + 56, pt=22, bold=True, color='000000')
    rtext(cv, '1）剩余差距是否、何时、如何闭合，是该领域{{最重要的开放问题}}；\n'
              '2）Anthropic 文章只作动机框架与阶段术语，[[证据全部来自同行文献]]；\n'
              '3）1,250 篇 arXiv 论文（2024–2026），首次覆盖从{{有界自我精炼}}到{{开放式 RSI}} 的完整谱系。',
          976, y + 92, 580, pt=19, lh=1.45)
    return ('p.1 摘要与 §1；p.2 Anthropic RSI 文章的五阶段连续谱：2023 前人类写代码→聊天机器人辅助→自主编程智能体→'
            '智能体委派智能体→闭环。截至 2026 年 5 月 Claude 据报道写了 Anthropic 80% 以上的合并代码，瓶颈在研究方向设定。'
            '论文明确：该文章只作框架与术语，不作证据。p.5：技术文献主体在阶段 3–4，§6 试探阶段 5。')


@slide()
def observations(cv, n):
    header(cv, '1.2 三个观察', '决定了综述的结构')
    y = intro(cv, '文献中“自我改进”的论文爆发式增长，但一套“self-X”词汇（self-refine、self-reward、self-play 等）'
                  '{{混淆了根本不同的目标}}。作者从三个观察出发，组织全文结构并提出四项贡献。')
    data = [('观察一：自我改进不是一件事',
             ['推理时修订输出（Self-Refine）', '重写自身代码（Gödel Agent）'],
             '按{{改进对象}}与{{闭环程度}}两轴定位，替代含混的 self-X 词汇（§2）'),
            ('观察二：增长快于沉淀',
             ['74% 语料发表于 2026 年', '季度产出：个位数 → 约 500 篇'],
             '只主张[[结构]]的耐久性而非论文清单；结构已吸收 OPSD、零数据自博弈两次新范式'),
            ('观察三：瓶颈总是评估器',
             ['可检查任务上自训练有效', '自奖励闭环“黑掉”自己的评委'],
             '把{{自我评估}}单列为一类（§5），作为另外三类的支柱')]
    top = y + 26
    for i, (head, chips, answer) in enumerate(data):
        x = 20 + i * 528
        panel(cv, x, top, 504, 822 - 46 - top, head)
        for j, c in enumerate(chips):
            chip(cv, c, x + 22, top + 68 + j * 62, 460, 52, pt=18)
        float_tag(cv, '论文对策', x + 252, top + 222)
        cv.box(x + 22, top + 244, 460, 822 - 46 - top - 264, fill=C['white'], line=C['blue'], lw=1.2, name='对策框')
        rtext(cv, answer, x + 38, top + 244, 428, pt=19, anchor='m', h=822 - 46 - top - 264, lh=1.3)
    conclusion(cv, '四项贡献：两轴分类 → 1,250 篇系统映射 → 自我评估专章 → 连接理论、极限与安全')
    return ('p.2 §1 三个观察：自我改进不是一件事（Self-Refine、STaR、Gödel Agent、AI Scientist 差异巨大）；'
            '74% 语料发表于 2026 年，季度产出由个位数增至 2026Q2 约 500 篇；评估器是共同瓶颈。'
            'Contributions (1)–(4)。p.25 §8：结构已吸收 OPSD 与零数据自博弈。')


@slide()
def taxonomy(cv, n):
    header(cv, '1.3 两轴分类框架', '改进对象 × 闭环程度')
    y = intro(cv, '{{有界自我精炼}}对固定的外部评估器改进，收敛且可评估；{{开放式 RSI}}连改进的标准与机制本身一起修改，'
                  '没有固定外部锚点，原则上发散。这一区分是全文的[[核心切分]]。')
    cols = [('部署时自我进化', '§3 · 393 篇'), ('训练时自我迭代', '§4 · 340 篇'),
            ('自我评估', '§5 · 318 篇'), ('自主研究', '§6 · 139 篇')]
    rows = [('人在环内', '每项改动\n由人审核'), ('人在环上', '自动信号\n人工审计结果'), ('完全闭环', '自生成自验证\n并自行应用')]
    cells = [['AI 辅助编程\n人工提示词', '人工整理的\nRLHF 基线', '专家量规\n人工基准设计', '人类主导、\nAI 助手协作'],
             ['Self-Refine · 执行修复\nTTT · 技能库', 'STaR · 自奖励 LM\n在线策略自蒸馏', '过程奖励 · LLM 评委\n经审计的分类体系', 'FunSearch · AlphaEvolve\nAI 科学家'],
             ['达尔文哥德尔机\n沙箱化自我修改', 'Absolute Zero\nR-Zero · Agent0', '自奖励评委 · 元评估\n评估器共进化', 'A-Evolve-Training\n自主后训练闭环']]
    x0, cw, gap = 230, 282, 10
    top = y + 18
    for j, (a, b) in enumerate(cols):
        x = x0 + j * (cw + gap)
        cv.box(x, top, cw, 84, fill=C['blue'], r=6, name=f'列头 {a}')
        cv.text(a, x + cw / 2, top + 27, pt=20, bold=True, color=C['white'], align='c')
        cv.text(b, x + cw / 2, top + 61, pt=16, color='D5ECEB', align='c')
    rh = 128
    for i, (a, b) in enumerate(rows):
        yy = top + 94 + i * (rh + 10)
        cv.box(20, yy, 198, rh, fill=C['gold'], r=6, name=f'行头 {a}')
        cv.text(a, 119, yy + 40, pt=20, bold=True, color=C['white'], align='c')
        rtext(cv, b, 26, yy + 64, 186, pt=16, color='D5ECEB', align='c', lh=1.0)
        for j in range(4):
            x = x0 + j * (cw + gap)
            hot = i == 2 and j == 2
            cv.box(x, yy, cw, rh, fill=C['zone'] if i == 1 else C['white'],
                   line=C['rose'] if hot else C['line'], lw=3 if hot else 1.2, r=6, name='单元格')
            rtext(cv, cells[i][j], x + 8, yy, cw - 16, pt=17, align='c', anchor='m', h=rh, lh=1.2,
                  color=C['rose'] if hot else C['text'], bold=hot)
    bx = x0 + 4 * (cw + gap) + 4
    y1, y2 = top + 94, top + 94 + 2 * (rh + 10) - 10
    cv.line(bx + 6, y1, bx + 16, y1, color=C['blue'], lw=2.5)
    cv.line(bx + 16, y1, bx + 16, y2, color=C['blue'], lw=2.5)
    cv.line(bx + 6, y2, bx + 16, y2, color=C['blue'], lw=2.5)
    rtext(cv, '有界自我\n精炼：\n§3–6 主体', bx + 26, y1 + 50, 150, pt=17, color=C['blue'], bold=True, lh=1.2)
    y3 = top + 94 + 2 * (rh + 10)
    cv.line(bx + 16, y3, bx + 16, y3 + rh, color=C['rose'], lw=2.5)
    rtext(cv, '开放式RSI\n稀少，安全\n风险集中', bx + 26, y3 + 8, 150, pt=16, color=C['rose'], bold=True, lh=1.15)
    conclusion(cv, '文献质量重心在“人在环上”的中间行；最关键的单元格是“自我评估 × 完全闭环”')
    return ('p.4–5 §2.2 与 Fig.1：轴一改进对象（部署时、训练时、自我评估、自主研究），轴二闭环程度'
            '（人在环内、人在环上、完全闭环）。单元格中的代表系统取自 Fig.1。p.5：几乎所有论文位于中间行；'
            '闭环行稀疏且越往右越薄，自我评估×闭环是有界自我精炼过渡到开放式 RSI 的位置。篇数来自 Table 1。')


@slide()
def corpus(cv, n):
    header(cv, '1.4 语料与方法', '1,250 篇 arXiv 论文（2024–2026）')
    y = intro(cv, '语料分两阶段构建并全部分入四类技术类别加一个基础族；{{74% 发表于 2026 年}}，'
                  '其中{{自我评估类 82%}} 来自 2026 年，是沉淀最快的类别。分类规则与逐篇归属[[随数据公开]]，分歧可审计。')
    top = y + 22
    flow = [('种子检索', '7 条主线\n去除离题 → 871 篇'), ('分类对齐', '规则重分 89 篇\n人工修正 3 处误判'),
            ('定向补充', '评估方法 · TTT\n零数据自博弈 → 379 篇'), ('合并语料', '1,250 篇\n4 类 + 基础族')]
    for i, (a, b) in enumerate(flow):
        x = 20 + i * 396
        tag(cv, a, x, top, 360, 46, pt=20, fill='gold' if i == 3 else 'blue')
        cv.box(x, top + 46, 360, 100, fill=C['white'], line=C['blue'], lw=1.2, name=f'流程 {a}')
        rtext(cv, b, x + 6, top + 48, 348, pt=18, align='c', anchor='m', h=96, lh=1.15)
        if i < 3:
            arrow_right(cv, x + 363, top + 96, w=30, h=28)
    t2 = top + 172
    panel(cv, 20, t2, 880, 880 - 28 - t2, '各类别论文数与 2026 年占比（Table 1）')
    data = [('部署时自我进化', 393, 74), ('训练时自我迭代', 340, 69), ('自我评估', 318, 82),
            ('自主研究', 139, 76), ('基础/极限/安全', 60, 57)]
    for i, (name, cnt, pct) in enumerate(data):
        yy = t2 + 108 + i * 50
        cv.text(name, 296, yy, pt=18, align='r')
        w = cnt / 393 * 400
        cv.box(310, yy - 17, w, 34, fill=C['rose'] if name == '自我评估' else C['blue'], name=f'条 {name}')
        cv.text(str(cnt), 320 + w, yy, pt=18, bold=True, color=C['navy'])
        cv.text(f'{pct}%', 870, yy, pt=18, bold=True, color=C['rose'] if pct == 82 else C['grey'], align='r')
    cv.text('篇数', 320, t2 + 72, pt=16, color=C['grey'])
    cv.text('2026 年占比', 870, t2 + 72, pt=16, color=C['grey'], align='r')
    cv.box(920, t2, 660, 880 - 28 - t2, fill='F2F6F6', name='局限栏')
    cv.text('局限性：', 944, t2 + 34, pt=22, bold=True, color='000000')
    rtext(cv, '1）样本而非普查：检索深度上限偏向近期高产主线；\n'
              '2）论文中位“年龄”仅数月，{{引用数不能代表影响}}；论证依托锚点与诊断文献；\n'
              '3）补充论文约 54/379 篇为边缘噪声，计数但不作证据；\n'
              '4）前沿实验室内部实践仅见发表部分。',
          944, t2 + 66, 616, pt=18, lh=1.2)
    return ('p.3 Table 1：部署时 393 篇（74% 为 2026 年）、训练时 340（69%）、自我评估 318（82%）、'
            '自主研究 139（76%）、基础/极限/安全 60（57%）。p.5–6 §2.3：种子检索 7 条主线得 871 篇；'
            '规则重分 89 篇、另修正 3 处误判；定向补充 379 篇（评估方法、测试时训练、零数据自博弈）。'
            'Limitations：样本非普查；引用数接近零；约 54/379 补充论文为边缘噪声；前沿实验室审查效应。')
