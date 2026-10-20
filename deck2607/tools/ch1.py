"""Cover, contents and chapter 1: background and the problem."""
import art
from deckkit import C, measure
from kit import slide, rp, boxtext, head, lead, concl, rpanel, tag, chip, toc


@slide('blank')
def cover(cv, n):
    cv.text('AI 递归自我改进：', 800, 360, pt=54, bold=True, color=C['white'], align='c', name='封面标题1')
    cv.text('从有界自我精炼到自主科研闭环', 800, 460, pt=54, bold=True, color=C['white'], align='c', name='封面标题2')
    cv.text('Recursive Self-Improvement in AI: From Bounded Self-Refinement to Autonomous Research Loops',
            800, 560, pt=18, color='DDEFEE', align='c', name='英文题名')
    cv.text('Mingguang Chen（UCR）· Licheng Wang（AlphaAvatar）· Bo Qu（IIT）', 800, 735, pt=20, bold=True, color='1A1A1A', align='c')
    cv.text('arXiv:2607.07663v1 · 2026年7月 · 论文解读汇报', 800, 790, pt=20, bold=True, color='1A1A1A', align='c')
    return '封面。论文 p.1：题名、作者与单位、July 2026、arXiv:2607.07663v1 [cs.AI]。'


@slide('toc')
def toc1(cv, n):
    toc(cv, 0)
    return '目录：四章。第一章研究背景与问题（论文 §1、§2.1）。'


@slide()
def background(cv, n):
    head(cv, '1.1 研究背景', 'AI 正在参与改进自己')
    y = lead(cv, 'AI 系统正越来越多地**参与自身改进**：修订输出、演化自身 harness、用自生成数据训练，乃至开展 AI 研究本身。'
                 'Anthropic 的五阶段连续谱给出了位置：截至 2026 年 5 月，Claude 据报道编写了 Anthropic **超过 80% 的合并代码**，'
                 '但**科研方向设定**——选择哪些问题重要——仍是瓶颈。')
    # staircase (left): treads rise left to right; labels are native text inside each tread
    X0, W, base = 30, 1000, 740
    hs = [200 + 40 * i for i in range(5)]
    cv.svg(art.stairs(hs, W), X0, base - max(hs), W, max(hs), name='五阶段阶梯')
    stages = [('人写全部代码', '2023 年以前'), ('聊天机器人辅助编码', '人主导'), ('自主编码智能体', '执行编码任务'),
              ('智能体委派智能体', '今日所处阶段'), ('闭环', '设计并训练后继模型')]
    sw = W / 5
    for i, (name, desc) in enumerate(stages):
        x, top = X0 + i * sw, base - hs[i]
        cv.num(i + 1, x + 34, top + 34, r=18, fill=C['blue'] if i < 4 else C['grey'], pt=18)
        yb = rp(cv, name, x + 12, top + 62, sw - 24, pt=18, bold=True, color=C['navy'] if i < 4 else C['grey'])
        rp(cv, desc, x + 12, yb + 6, sw - 24, pt=16, color=C['rose'] if i == 3 else C['grey'], bold=i == 3)
    px = X0 + 3.5 * sw
    cv.icon_c('pin', px, base - hs[3] - 36, 44, name='今日位置')
    cv.text('今日位置：执行侧 >80% 合并代码', px - 30, base - hs[3] - 36, pt=18, bold=True, color=C['rose'], align='r')
    tag(cv, '文献主体位于第 3–4 阶段，§6 的工作在试探第 5 阶段边界', X0 + W / 2, base + 34, pt=18, fill=C['gold'])
    # key points (right)
    cv.card(1050, 330, 530, 466, fill='ECF6F6', line=None, r=6, shadow=False, name='主要启示')
    cv.text('主要启示：', 1072, 364, pt=22, bold=True, color='1A1A1A')
    rp(cv, '1）**执行**环节已高度自动化：编码、实验执行正被智能体接管。\n'
           '2）**方向设定**仍由人完成：决定什么问题值得做，是剩余的缺口。\n'
           '3）论文只把连续谱当作**阶段词汇与动机框架**，证据来自 1,250 篇同行文献。',
       1072, 400, 490, pt=18, lh=1.35)
    concl(cv, '核心问题：**"方向设定"这一缺口是否、何时、如何闭合**', y=842)
    return ('论文 p.1 摘要；p.2 §1：Anthropic 关于递归自我改进的文章 [5] 把 AI 参与改进的自主程度分为五阶段：'
            '人写全部代码（2023 前）、聊天机器人辅助编码、自主编码智能体、智能体委派智能体（今日）、闭环（设计并训练后继模型）。'
            '截至 2026 年 5 月 Claude 据报道编写 Anthropic 超过 80% 的合并代码；瓶颈在科研方向设定。p.5：技术文献主体位于第 3–4 阶段，§6 试探第 5 阶段。'
            '论文明确只把该文作为动机框架和阶段词汇，不作为证据。')


@slide()
def observations(cv, n):
    head(cv, '1.2 三个观察', '决定了论文的结构')
    y = lead(cv, '论文收集 **1,250 篇 arXiv 论文（2024–2026）**，分为四类技术类别加一个基础族。三个观察决定了全文结构：'
                 '概念混用需要**新坐标系**，增长过快需要**持久框架**，**评估器瓶颈**需要单列。')
    panels = [
        ('观察一：概念混用', 'fork',
         ('修订输出、自训练、改写代码、自主研究', '同一套 self-X 词汇掩盖了差异'),
         '提出**两轴分类**：改进什么 × 闭环程度，替代模糊的 self-X 词汇（§2）'),
        ('观察二：增长快于沉淀', 'growth',
         ('74% 的语料发表于 2026 年', '季度产出从个位数涨到约 500 篇'),
         '现有综述只覆盖单一切片；本文首次覆盖**从有界精炼到开放式 RSI 的全谱**'),
        ('观察三：瓶颈是评估器', 'gauge',
         ('代码、数学可检验，自训练才有效', '自奖励环会"黑掉"自己的裁判'),
         '把自评估**单列为一类**（§5），视为其余三类的支柱'),
    ]
    for i, (t, ic, (a, b), sol) in enumerate(panels):
        x = 20 + i * 527
        rpanel(cv, x, 288, 506, 512, t, icon=ic, pt=24)
        chip(cv, a, x + 18, 352, 228, 138, pt=18)
        chip(cv, b, x + 260, 352, 228, 138, pt=18)
        boxtext(cv, sol, x + 18, 544, 470, 234, pt=18, line=C['blue'], fill=C['white'], r=4, lw=1.5, align='l', pad=18, lh=1.3)
        tag(cv, '论文做法', x + 253, 544, pt=18)
    concl(cv, '构建 **"两轴分类 → 系统映射 1,250 篇 → 单列自评估 → 连接理论与安全"** 的综述结构', y=834)
    return ('论文 p.2 §1 Three observations 与 Contributions：(1) "self-improvement is not one thing"——输出修订（Self-Refine）、'
            '自生成数据训练（STaR、Self-Rewarding LMs）、改写自身代码（Gödel Agent、DGM）、自主 AI 研究；(2) 74% 语料发表于 2026，'
            '季度产出从 2024 初的个位数到 2026Q2 约 500 篇（Figure 6），现有综述只覆盖单一切片；(3) 评估器是共同瓶颈，因此自评估单列（§5）。'
            '四项贡献：两轴分类、1,250 篇映射、自评估专题、理论/极限/安全综合。')


@slide()
def core_cut(cv, n):
    head(cv, '1.3 核心区分', '有没有固定的外部锚点')
    lead(cv, '同样叫"自我改进"，**重读草稿改一个错**与**智能体改写自己的代码库**是两类事。论文的中心切分是：'
             '改进时有没有一个**固定的外部评估器**作为锚点。')
    for i, (t, col, svg, mid, pts) in enumerate([
        ('有界自我精炼', C['blue'], art.converge_loop(), '外部评估器',
         '对照**固定外部**评估器\n**收敛**且**可评估**\n已是工业实践\n文献主体所在'),
        ('开放式递归自我改进（RSI）', C['rose'], art.diverge_spiral(), '',
         '连**改进标准**一起修改\n无固定锚点，原则上**发散**\n闭环改评估器的研究极少\n安全风险集中于此（§7）')]):
        x = 20 + i * 800
        rpanel(cv, x, 262, 760, 368, t, pt=24, color=col)
        cv.svg(svg, x + 24, 326, 300, 220, name='收敛环' if i == 0 else '发散螺旋')
        if mid:
            cv.text(mid, x + 174, 436, pt=16, bold=True, color=C['white'], align='c')
        else:
            cv.text('评估器也在环内', x + 174, 570, pt=16, bold=True, color=C['rose'], align='c')
        rp(cv, pts, x + 340, 350, 404, pt=19, lh=1.4)
    cv.block_arrow(770, 418, 60, 56, fill=C['gold'])
    terms = [('Agent', '感知—行动循环中带工具与记忆的模型'), ('Harness', '提示、工具、记忆、技能库等外围'),
             ('Evaluator', '把产物映射为质量信号的机制'), ('TTT', '部署中按查询更新权重'),
             ('Self-play', '模型自己生成任务或对手')]
    for i, (k, v) in enumerate(terms):
        x = 20 + i * 316
        cv.label_box(k, x, 646, 300, 40, pt=18, fill=C['blue'], name=f'术语 {k}')
        boxtext(cv, v, x, 686, 300, 92, pt=16, fill=C['pale'], line=C['blue'], r=0, lw=1, pad=12)
    concl(cv, '"self-X"词汇相同，**收敛性、可评估性与风险**完全不同', y=830)
    return ('论文 p.3–4 §2.1 定义：Agent、Harness（脚手架）、Evaluator（verifier 有可靠性保证，judge 没有）、Self-improvement、'
            'TTT、Self-play。Bounded self-refinement 对照固定外部评估器，收敛、可评估；open-ended RSI 修改系统以及改进的标准或机制本身，'
            '无固定外部锚点，原则上发散——"The distinction is the survey\'s central cut."')
